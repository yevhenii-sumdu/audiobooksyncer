import re
from itertools import accumulate
from tempfile import NamedTemporaryFile

import ffmpeg
from thefuzz import fuzz
from tqdm import tqdm

from .utils import get_audio_duration


def _trim_audiofile(input_path, output_path, duration):
    (
        ffmpeg
        .input(input_path)
        .output(output_path, to=duration, f='wav')
        .run(overwrite_output=True, quiet=True)
    )


def _transcribe_beginning(audio_path):
    import whisper

    duration = 60
    model_name = 'base'

    with NamedTemporaryFile() as temp_file:
        _trim_audiofile(audio_path, temp_file.name, duration)

        model = whisper.load_model(model_name)
        result = model.transcribe(temp_file.name)

    return result['text']


def _get_anchor_fragment_indexes(text_fragments, audio_files):
    audio_durations = [get_audio_duration(f) for f in audio_files]

    total_audio_duration = sum(audio_durations)
    total_characters = sum(len(fragment) for fragment in text_fragments)

    cumulative_fragment_lengths = list(accumulate(len(fragment) for fragment in text_fragments))

    cumulative_audio_fractions = [
        cum_duration / total_audio_duration
        for cum_duration in accumulate(audio_durations[:-1])
    ]

    anchor_char_indexes = [
        round((total_characters - 1) * fraction)
        for fraction in cumulative_audio_fractions
    ]

    anchor_fragment_indexes = [
        next(i for i, cum_length in enumerate(cumulative_fragment_lengths) if char_pos < cum_length)
        for char_pos in anchor_char_indexes
    ]

    return anchor_fragment_indexes


def _clean_string(string):
    string = re.sub(r'\W', '', string)
    return string.lower()


def _find_start_fragment(text_fragments, anchor_fragment_index, transcription):
    window_margin = 20
    window_start = max(anchor_fragment_index - window_margin, 0)
    window_end = min(anchor_fragment_index + window_margin, len(text_fragments) - 1)

    window = text_fragments[window_start:window_end + 1]

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
            score = fuzz.ratio(concatenated_fragment[:len(transcription)], transcription)

            if score > best_match_score:
                best_match_score = score
                best_match_index = i

    return window_start + best_match_index


def locate_chapters(text_fragments, audio_files):
    anchor_fragment_indexes = _get_anchor_fragment_indexes(text_fragments, audio_files)

    transcriptions = []
    for af in tqdm(audio_files[1:], desc='Audio files'):
        transcriptions.append(_transcribe_beginning(af))

    return [
        _find_start_fragment(text_fragments, *i)
        for i in zip(anchor_fragment_indexes, transcriptions)
    ]
