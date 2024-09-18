from .utils import run_in_subprocess


@run_in_subprocess
def align_texts(src_path, tgt_path):
    from bertalign import Bertalign, load_model

    with open(src_path, 'r') as f:
        src = f.read()
    with open(tgt_path, 'r') as f:
        tgt = f.read()

    aligner = Bertalign(src, tgt, load_model())
    aligner.align_sents()

    return aligner.get_result()
