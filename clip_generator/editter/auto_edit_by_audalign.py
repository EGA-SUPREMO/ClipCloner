import os

import audalign as ad

from clip_generator.editter import dirs


def get_offset(filename: str):
    #fingerprint_rec = ad.FingerprintRecognizer()
    corr_rec = ad.CorrelationRecognizer()
    #corr_rec = ad.VisualRecognizer()
    corr_rec.config.normalize = True
    corr_rec.config.sample_rate = 4000
    #fingerprint_rec.config.set_accuracy(3)

    results = ad.align_files(dirs.dirFixedAudioParts + filename, dirs.dir_audio_stream, recognizer=corr_rec)

    try:
        return results[filename]
    except Exception:
        return 9999999
    # fingerprint_rec.save_fingerprinted_files("../test_borrar/save_file.json")
