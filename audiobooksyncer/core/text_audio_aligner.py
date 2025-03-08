import multiprocessing as mp

from aeneas.executetask import ExecuteTask
from aeneas.runtimeconfiguration import RuntimeConfiguration
from aeneas.syncmap import SyncMapFragment
from aeneas.task import Task
from aeneas.textfile import TextFile, TextFragment
from tqdm import tqdm

from . import config
from .utils import PathLikeType
from .utils import get_audio_duration


def _split_into_chapters(text_fragments: list[str], split_indexes: list[int]):
    split_indexes = [0] + split_indexes + [len(text_fragments)]

    return [
        text_fragments[split_indexes[i] : split_indexes[i + 1]]
        for i in range(len(split_indexes) - 1)
    ]


def _create_task(audio_file: PathLikeType, chapter: list[str], lang: str):
    task = Task(config_string=f'task_language={lang}')
    task.audio_file_path_absolute = audio_file

    textfile = TextFile()

    id_digits = len(str(len(chapter)))
    for i, sent in enumerate(chapter, 1):
        id = 'f' + str(i).zfill(id_digits)

        textfile.add_fragment(TextFragment(id, lang, [sent], [sent]))

    task.text_file = textfile

    return task


def _process_chapter(args):
    idx, audio_file, chapter, lang = args

    task = _create_task(audio_file, chapter, lang)
    rconf = RuntimeConfiguration()
    rconf[RuntimeConfiguration.DTW_MARGIN] = config.aeneas_dtw_margin
    ExecuteTask(task, rconf=rconf).execute()

    intervals = [
        {
            'begin': int(float(fr.interval.begin) * 1000),
            'end': int(float(fr.interval.end) * 1000),
        }
        for fr in task.sync_map.fragments
        if fr.fragment_type == SyncMapFragment.REGULAR
    ]

    return idx, intervals


def align_text_with_audio(
    text_fragments: list[str],
    split_indexes: list[int],
    audio_files: list[str],
    lang: str,
) -> list[dict]:
    chapters = _split_into_chapters(text_fragments, split_indexes)

    if len(chapters) != len(audio_files):
        raise Exception('Chapters != audio files')

    with mp.Pool(config.aeneas_processes) as pool:
        processing_results = pool.imap_unordered(
            _process_chapter,
            [
                (idx, af, ch, lang)
                for idx, (af, ch) in enumerate(zip(audio_files, chapters))
            ],
        )

        chapter_results = []

        for pr_res in tqdm(processing_results, total=len(chapters), desc='Chapters'):
            chapter_results.append(pr_res)

        chapter_results.sort(key=lambda x: x[0])

    result = []

    timeshift = 0

    for idx, intervals in chapter_results:
        for interval in intervals:
            interval['begin'] += timeshift
            interval['end'] += timeshift

        result += intervals

        timeshift += int(get_audio_duration(audio_files[idx]) * 1000)

        # remove a gap between chapters
        result[-1]['end'] = timeshift

    return result
