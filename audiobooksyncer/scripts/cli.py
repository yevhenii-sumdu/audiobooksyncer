import click
from pathlib import Path
from ..core.texts_aligner import *
from ..core.text_audio_aligner import *
from ..core.chapter_locator import *
from ..core.output_generator import *
from ..core.utils import *
from ..core.constants import *

@click.command()
@click.argument('src_path', type=click.Path(exists=True, dir_okay=False))
@click.argument('tgt_path', type=click.Path(exists=True, dir_okay=False))
@click.argument('audio_dir', type=click.Path(exists=True, file_okay=False))
@click.option('--use-cache', is_flag=True)
def cli(src_path, tgt_path, audio_dir, use_cache):
    global align_texts
    global locate_chapters
    global align_text_with_audio

    align_texts = cache(TEXTS_ALIGNMENT_RES, use_cache)(align_texts)
    locate_chapters = cache(CHAPTER_LOCATION_RES, use_cache)(locate_chapters)
    align_text_with_audio = cache(AUDIO_ALIGNMENT_RES, use_cache)(align_text_with_audio)

    Path(WORKDIR).mkdir(exist_ok=True)

    os.environ['TOKENIZERS_PARALLELISM'] = 'true'

    aligned_texts = align_texts(src_path, tgt_path)
    src_fragments = [i['src'] for i in aligned_texts['data']]

    split_indexes = locate_chapters(src_fragments, audio_dir)

    aligned_audio = align_text_with_audio(src_fragments, split_indexes, audio_dir, aligned_texts['src_lang_code'])

    save_to_json(get_sync_map(aligned_texts['data'], aligned_audio), SYNC_MAP)