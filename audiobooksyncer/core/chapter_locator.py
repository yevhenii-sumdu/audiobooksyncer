import re
from itertools import accumulate
from tempfile import NamedTemporaryFile
from typing import Optional

import ffmpeg
from loguru import logger
from thefuzz import fuzz
from tqdm import tqdm
from whisper import Whisper

from .utils import PathLikeType, get_audio_duration, run_in_subprocess


def _trim_audiofile(input_path: PathLikeType, output_path: PathLikeType, duration: int):
    (
        ffmpeg.input(input_path)
        .output(output_path, to=duration, f='wav')
        .run(overwrite_output=True, quiet=True)
    )

    logger.debug(
        f'Trimmed {input_path}, result saved to {output_path}, duration: {duration}s'
    )


def _transcribe_beginning(
    audio_path: PathLikeType, model: Whisper, lang: Optional[str]
) -> str:
    duration = 60

    with NamedTemporaryFile() as temp_file:
        _trim_audiofile(audio_path, temp_file.name, duration)

        result = model.transcribe(temp_file.name, language=lang)

        logger.debug(f'Transcribed {audio_path}')

    return result['text']


def _get_anchor_fragment_indexes(text_fragments: list[str], audio_files: list[str]):
    audio_durations = [get_audio_duration(f) for f in audio_files]

    total_audio_duration = sum(audio_durations)
    total_characters = sum(len(fragment) for fragment in text_fragments)

    cumulative_fragment_lengths = list(
        accumulate(len(fragment) for fragment in text_fragments)
    )

    cumulative_audio_fractions = [
        cum_duration / total_audio_duration
        for cum_duration in accumulate(audio_durations[:-1])
    ]

    anchor_char_indexes = [
        round((total_characters - 1) * fraction)
        for fraction in cumulative_audio_fractions
    ]

    anchor_fragment_indexes = [
        next(
            index
            for index, cum_length in enumerate(cumulative_fragment_lengths)
            if char_pos < cum_length
        )
        for char_pos in anchor_char_indexes
    ]

    return anchor_fragment_indexes


def _clean_string(string: str):
    string = re.sub(r'\W', '', string)
    return string.lower()


def _find_start_fragment(
    text_fragments: list[str], anchor_fragment_index: int, transcription: str
):
    # margin is set to 3% but no less than 20 fragments
    # this would allow for almost an hour of deviation
    # on a 30-hour book
    window_margin = max(20, int(len(text_fragments) * 0.03))
    window_start = max(anchor_fragment_index - window_margin, 0)
    window_end = min(anchor_fragment_index + window_margin, len(text_fragments) - 1)

    window = text_fragments[window_start : window_end + 1]

    best_match_score = 0
    best_match_index = 0

    transcription = _clean_string(transcription)

    for i in range(len(window)):
        concatenated_fragment = ''
        j = i

        while len(concatenated_fragment) < len(transcription) and j < len(window):
            concatenated_fragment += _clean_string(window[j])
            j += 1

        if len(concatenated_fragment) >= len(transcription):
            score = fuzz.ratio(
                concatenated_fragment[: len(transcription)], transcription
            )

            if score > best_match_score:
                best_match_score = score
                best_match_index = i

    return window_start + best_match_index


@run_in_subprocess
def locate_chapters(
    text_fragments: list[str], audio_files: list[str], lang: Optional[str] = None
):
    """
    Locate where each audio file (chapter) starts in a list of text fragments.

    :param text_fragments: List of text fragments.
    :param audio_files: List of audio file paths.
    :param lang: Language.
    :return: List of fragment indexes corresponding to chapter locations.
    """
    import whisper

    model_name = 'base'
    model = whisper.load_model(model_name)

    logger.debug(f'Loaded whisper {model_name} model')

    anchor_fragment_indexes = _get_anchor_fragment_indexes(text_fragments, audio_files)

    logger.debug(f'Located {len(anchor_fragment_indexes)} anchor fragments')

    transcriptions = []
    for af in tqdm(audio_files[1:], desc='Audio files'):
        transcriptions.append(_transcribe_beginning(af, model, lang))

    logger.debug(f'Transcribed {len(transcriptions)} audio files')

    return [
        _find_start_fragment(text_fragments, *i)
        for i in zip(anchor_fragment_indexes, transcriptions)
    ]
