import audalign as ad

from clip_generator.editter import dirs


def get_offset(filename: str):
    # fingerprint_rec = ad.FingerprintRecognizer()
    fingerprint_rec = ad.CorrelationRecognizer()

    # fingerprint_rec.config.set_accuracy(3)
    # results = ad.align("../test_borrar/", recognizer=fingerprint_rec)

    # ad.convert_audio_file("../clip.mkv", "../test_borrar/clip.wav")
    ad.convert_audio_file("../stream.mkv", "../test_borrar/stream.wav")

    results = ad.target_align(
        dirs.dirFixedAudioParts + filename,
        directory_path="../test_borrar/",
        recognizer=fingerprint_rec
    )
    return results[filename]
    # ad.pretty_print_alignment(results)
    # fingerprint_rec.save_fingerprinted_files("../test_borrar/save_file.json")
