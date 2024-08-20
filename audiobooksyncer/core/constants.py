import os

WORKDIR = 'audiobooksyncer_workdir'

TEXTS_ALIGNMENT_RES = os.path.join(WORKDIR, 'aligned_texts.json')
CHAPTER_LOCATION_RES = os.path.join(WORKDIR, 'chapter_locations.json')
AUDIO_ALIGNMENT_RES = os.path.join(WORKDIR, 'aligned_audio.json')
SYNC_MAP = os.path.join(WORKDIR, 'sync_map.json')
