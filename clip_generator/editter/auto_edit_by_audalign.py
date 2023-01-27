import os

import audalign as ad

from clip_generator.editter import dirs


def get_offset(filename: str):
    #fingerprint_rec = ad.FingerprintRecognizer()
    fingerprint_rec = ad.CorrelationRecognizer()

    #fingerprint_rec.config.set_accuracy(3)

    results = ad.align_files(dirs.dirFixedAudioParts + filename, dirs.dir_audio_stream, recognizer=fingerprint_rec)

    return results[filename]
    # ad.pretty_print_alignment(results)
    # fingerprint_rec.save_fingerprinted_files("../test_borrar/save_file.json")
