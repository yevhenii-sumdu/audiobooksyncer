from .utils import PathLikeType, run_in_subprocess


@run_in_subprocess
def align_texts(src_path: PathLikeType, tgt_path: PathLikeType):
    """
    Align text and translation using Bertalign.

    :param src_path: Path to the source text file.
    :param tgt_path: Path to the target text file (translation).
    :return: Alignment result.
    """
    from bertalign import Bertalign, load_model

    with open(src_path, 'r') as f:
        src = f.read()
    with open(tgt_path, 'r') as f:
        tgt = f.read()

    aligner = Bertalign(src, tgt, load_model())
    aligner.align_sents()

    return aligner.get_result()
