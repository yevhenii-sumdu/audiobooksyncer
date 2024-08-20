import click
import warnings
from pathlib import Path
from ..core.texts_aligner import *
from ..core.text_audio_aligner import *
from ..core.chapter_locator import *
from ..core.output_generator import *
from ..core.utils import *
from ..core.constants import *

warnings.filterwarnings('ignore')

def ask_to_continue(skip_confirmation):
    if skip_confirmation:
        return
    if not click.confirm('Done. Continue?', default=True):
        exit(0)

@click.command()
@click.argument('src_path', type=click.Path(exists=True, dir_okay=False))
@click.argument('tgt_path', type=click.Path(exists=True, dir_okay=False))
@click.argument('audio_dir', type=click.Path(exists=True, file_okay=False))
@click.option('--use-cache', is_flag=True)
@click.option('--yes', '-y', is_flag=True)
def cli(src_path, tgt_path, audio_dir, use_cache, yes):
    global align_texts
    global locate_chapters
    global align_text_with_audio

    align_texts = cache(TEXTS_ALIGNMENT_RES, use_cache)(align_texts)
    locate_chapters = cache(CHAPTER_LOCATION_RES, use_cache)(locate_chapters)
    align_text_with_audio = cache(AUDIO_ALIGNMENT_RES, use_cache)(align_text_with_audio)

    ac = lambda: ask_to_continue(yes)

    Path(WORKDIR).mkdir(exist_ok=True)

    os.environ['TOKENIZERS_PARALLELISM'] = 'true'

    print('STEP 1: Aligning text and translation')
    aligned_texts = align_texts(src_path, tgt_path)
    src_fragments = [i['src'] for i in aligned_texts['data']]

    ac()

    print('\nSTEP 2: Locating where each audio file starts')
    split_indexes = locate_chapters(src_fragments, audio_dir)

    ac()

    print('\nSTEP 3: Aligning text and audio')
    aligned_audio = align_text_with_audio(src_fragments, split_indexes, audio_dir, aligned_texts['src_lang_code'])

    ac()

    print(f'\nSTEP 4: Saving result to {SYNC_MAP}')
    save_to_json(get_sync_map(aligned_texts['data'], aligned_audio), SYNC_MAP)
