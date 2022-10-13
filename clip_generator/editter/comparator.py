import librosa

import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

dir_audiocito = "../../../"
sec = 0.1
def find_similarity(within_file, find_file):
	y_within, sr_within = librosa.load(within_file, sr=None)
	y_find, _ = librosa.load(find_file, sr=sr_within)


	fig, ax = plt.subplots()
	ax.plot(y_find)
	ax.plot(y_within)
	fig.savefig("eee with.png")

	c = signal.correlate(y_within, y_find, mode='valid', method='fft')
	peak = np.argmax(c)


	fig, ax = plt.subplots()
	ax.plot(c)
	fig.savefig(f"crosscorrelation stream.png")

	print(c)
	print(peak)
	print(c[peak])

find_similarity(dir_audiocito + "clip.wav", dir_audiocito + "zeta_trimmed_stream.wav")
