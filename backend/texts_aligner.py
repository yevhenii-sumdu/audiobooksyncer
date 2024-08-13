def align_texts(src_path, tgt_path):
    from bertalign import Bertalign

    with open(src_path, 'r') as f:
        src = f.read()
    with open(tgt_path, 'r') as f:
        tgt = f.read()

    aligner = Bertalign(src, tgt)
    aligner.align_sents()

    return aligner.get_result()