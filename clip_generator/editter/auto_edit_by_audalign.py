import audalign as ad


#fingerprint_rec = ad.FingerprintRecognizer()
fingerprint_rec = ad.CorrelationRecognizer()

#fingerprint_rec.config.set_accuracy(3)
fingerprint_rec.config.locality = 1
#results = ad.align("../test_borrar/", recognizer=fingerprint_rec)

ad.convert_audio_file("../clip.mkv", "../test_borrar/clip.wav")
ad.convert_audio_file("../stream.mkv", "../test_borrar/stream.wav")

results = ad.target_align(
    "../test_borrar/clip.wav",
    directory_path="../test_borrar/",
    destination_path="../test_borrar1/",
    recognizer=fingerprint_rec
)


#print(results)
ad.pretty_print_alignment(results)
#fingerprint_rec.save_fingerprinted_files("../test_borrar/save_file.json")
