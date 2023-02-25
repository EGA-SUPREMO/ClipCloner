import os

import audalign as ad

from clip_generator.editter import dirs


def get_offset(filename: str):
    #corr_rec = ad.FingerprintRecognizer()
    corr_rec = ad.CorrelationRecognizer()
    #corr_rec = ad.VisualRecognizer()
    corr_rec.config.normalize = True
    #corr_rec.config.sample_rate = 8000
    #corr_rec.config.set_accuracy(1)
#    corr_rec.save_fingerprinted_files("../test_borrar/save_file.json")
#    corr_rec.load_fingerprinted_files("../test_borrar/save_file.json")
    #print(corr_rec.config.get_hash_style())

    results = ad.align_files(dirs.dirFixedAudioParts + filename, dirs.dir_audio_stream, recognizer=corr_rec)
    #corr_rec.save_fingerprinted_files("../test_borrar/save_file.json")

    try:
        return results[filename]
    except Exception:
        return 9999999
