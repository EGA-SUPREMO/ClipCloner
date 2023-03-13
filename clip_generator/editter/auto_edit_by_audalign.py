import os

import audalign as ad

from clip_generator.editter import dirs


def get_offset(filename: str):
    #corr_rec = ad.FingerprintRecognizer()
    corr_rec = ad.CorrelationRecognizer()
    #corr_rec = ad.VisualRecognizer()
    #corr_rec = ad.CorrelationSpectrogramRecognizer()
    corr_rec.config.normalize = True
    corr_rec.config.sample_rate = 8000
    corr_rec.config.match_len_filter = 100
    #corr_rec.config.set_accuracy(1)
#    corr_rec.save_fingerprinted_files("../test_borrar/save_file.json")
#    corr_rec.load_fingerprinted_files("../test_borrar/save_file.json")

    results = ad.align_files(dirs.dirFixedAudioParts + filename, dirs.dir_audio_stream, recognizer=corr_rec)
    #corr_rec.save_fingerprinted_files("../test_borrar/save_file.json")

    print(results['match_info'][filename]['match_info']['stream_audio.mp4']['offset_seconds'])
    try:
        return results[filename]
    except Exception:
        return 9999999


# TODO needs tests
def get_offset_for_trim():
    corr_rec = ad.CorrelationRecognizer()
    corr_rec.config.normalize = True
    corr_rec.config.sample_rate = 8000
    corr_rec.config.match_len_filter = 1000

    results = ad.align_files(dirs.dir_audio_clip, dirs.dir_audio_stream, recognizer=corr_rec)

    try:
        return results['match_info'][os.path.basename(dirs.dir_audio_clip)]['match_info'][os.path.basename(dirs.dir_audio_stream)]['offset_seconds']
    except Exception:
        return 9999999