import ffmpeg
from tempfile import NamedTemporaryFile

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
