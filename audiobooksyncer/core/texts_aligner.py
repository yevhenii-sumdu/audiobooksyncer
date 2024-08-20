import sys
import re

class _ProgressCapturer():
    def __init__(self, progress_callback):
        self.progress_callback = progress_callback
        self.second_progressbar = False
        self.last_progress = None

    def __enter__(self):
        if self.progress_callback is not None:
            self.orig_stderr_write = sys.stderr.write
            sys.stderr.write = lambda s: (self.orig_stderr_write(s), self.handle_progress(s))
    
    def __exit__(self, exc_type, exc_value, tb):
        if self.progress_callback is not None:
            sys.stderr.write = self.orig_stderr_write

    def handle_progress(self, str):
        match = re.search(r'Batches:\s+(\d+)%', str)

        if match:
            progress = int(match.group(1)) / 2

            if self.last_progress == 50 and progress == 0:
                self.second_progressbar = True

            if self.second_progressbar:
                progress += 50

            if progress != self.last_progress:
                self.last_progress = progress
                self.progress_callback(progress)

def align_texts(src_path, tgt_path, progress_callback=None):
    from bertalign import Bertalign

    with open(src_path, 'r') as f:
        src = f.read()
    with open(tgt_path, 'r') as f:
        tgt = f.read()

    with _ProgressCapturer(progress_callback):
        aligner = Bertalign(src, tgt)

    aligner.align_sents()

    return aligner.get_result()