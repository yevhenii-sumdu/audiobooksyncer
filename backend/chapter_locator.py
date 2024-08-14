import ffmpeg
from itertools import accumulate
from tempfile import NamedTemporaryFile
from mutagen.mp3 import MP3
from backend.utils import get_sorted_files_in_dir

def _trim_audiofile(input_path, output_path, duration):
    (
        ffmpeg
        .input(input_path)
        .filter('atrim', duration=duration)
        .output(output_path, f=ffmpeg.probe(input_path)['format']['format_name'])
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

def _get_anchor_fragment_indexes(text_fragments, audio_dir):
    audio_files = get_sorted_files_in_dir(audio_dir)
    audio_durations = [MP3(f).info.length for f in audio_files]

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
        next(i for i, cum_length in enumerate(cumulative_fragment_lengths) if char_pos <= cum_length)
        for char_pos in anchor_char_indexes
    ]
    
    return anchor_fragment_indexes
