import librosa

import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

def find_similarity(within_file, find_file, window):
	y_within, sr_within = librosa.load(within_file, sr=None)
	y_find, _ = librosa.load(find_file, sr=sr_within) 

	c = signal.correlate(y_within, y_find[:sr_within*window], mode='valid', method='fft')
	peak = np.argmax(c)
	offset = round(peak / sr_within, 2)


	fig, ax = plt.subplots()
	ax.plot(c)
	fig.savefig("cross-correlation2.png")

find_similarity("clip.wav", "stream.wav", 5)