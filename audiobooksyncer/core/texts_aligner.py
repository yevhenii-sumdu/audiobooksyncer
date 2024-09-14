import multiprocessing as mp


def _align_texts(src_path, tgt_path):
    from bertalign import Bertalign, load_model

    with open(src_path, 'r') as f:
        src = f.read()
    with open(tgt_path, 'r') as f:
        tgt = f.read()

    aligner = Bertalign(src, tgt, load_model())
    aligner.align_sents()

    return aligner.get_result()


def align_texts(src_path, tgt_path):
    with mp.Pool(1) as pool:
        return pool.apply(_align_texts, (src_path, tgt_path))
