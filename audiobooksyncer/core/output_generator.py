def get_sync_map(aligned_texts, aligned_audio):
    return [
        {
            'src': texts_fr['src'],
            'tgt': texts_fr['tgt'],
            'begin': audio_fr['begin'],
            'end': audio_fr['end']
        }
        for texts_fr, audio_fr in zip(aligned_texts, aligned_audio)
    ]
