def get_sync_map(aligned_texts: list[dict], aligned_audio: list[dict]):
    """
    Generate a synchronization map.

    :param aligned_texts: Text alignment result.
    :param aligned_audio: Audio alignment result.
    :return: A sync map.
    """
    return [
        {
            'src': texts_fr['src'],
            'tgt': texts_fr['tgt'],
            'begin': audio_fr['begin'],
            'end': audio_fr['end'],
        }
        for texts_fr, audio_fr in zip(aligned_texts, aligned_audio)
    ]
