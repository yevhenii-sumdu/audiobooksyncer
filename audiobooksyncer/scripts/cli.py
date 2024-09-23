import warnings

import click

from ..core.chapter_locator import locate_chapters
from ..core.output_generator import get_sync_map
from ..core.text_audio_aligner import align_text_with_audio
from ..core.texts_aligner import align_texts
from ..core.utils import get_sorted_files_in_dir
from ..pathstore import PathStore
from ..utils import cache, hash_files, save_to_json

warnings.filterwarnings('ignore')


def _ask_to_continue(skip_confirmation):
    if skip_confirmation:
        return
    if not click.confirm('Done. Continue?', default=True):
        exit(0)


@click.command()
@click.argument('src_path', type=click.Path(exists=True, dir_okay=False))
@click.argument('tgt_path', type=click.Path(exists=True, dir_okay=False))
@click.argument('audio_dir', type=click.Path(exists=True, file_okay=False))
@click.option('--yes', '-y', is_flag=True)
def main(src_path, tgt_path, audio_dir, yes):
    audio_files = get_sorted_files_in_dir(audio_dir)

    paths = PathStore(hash_files(src_path, tgt_path, *audio_files))

    c_align_texts = cache(paths.aligned_texts)(align_texts)
    c_locate_chapters = cache(paths.chapter_locations)(locate_chapters)
    c_align_text_with_audio = cache(paths.aligned_audio)(align_text_with_audio)

    def ac():
        _ask_to_continue(yes)

    print(f'Saving results to {paths.results_dir}/')
    paths.results_dir.mkdir(exist_ok=True)

    print('\nSTEP 1: Aligning text and translation')
    aligned_texts = c_align_texts(src_path, tgt_path)
    src_fragments = [i['src'] for i in aligned_texts['data']]
    src_lang = aligned_texts['src_lang_code']

    ac()

    print('\nSTEP 2: Locating where each audio file starts')
    split_indexes = c_locate_chapters(src_fragments, audio_files, src_lang)

    ac()

    print('\nSTEP 3: Aligning text and audio')
    aligned_audio = c_align_text_with_audio(
        src_fragments, split_indexes, audio_files, src_lang
    )

    ac()

    print(f'\nSTEP 4: Saving result to {paths.sync_map}')
    save_to_json(get_sync_map(aligned_texts['data'], aligned_audio), paths.sync_map)
