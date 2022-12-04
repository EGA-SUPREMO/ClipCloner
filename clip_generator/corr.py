import numpy as np
from scipy.io import wavfile

import matplotlib.pyplot as plt

# Read in the two audio files
rate1, data1 = wavfile.read("clip2.wav")
rate2, data2 = wavfile.read("clipkoyo.wav")

# Make sure the audio files have the same sample rate
if rate1 != rate2:
    raise ValueError("The sample rates of the two audio files must match")

data1 = np.resize(data1, data2.shape)

# Calculate the difference between the two audio files
difference = np.abs(data1 - data2)
difference1 = np.abs(data2 - data1)


# casting both audios into mono-channel wave
# this is not optimal for comparing multi-channel audio, but this is in general very naive implementation
if len(data1.shape) > 1:
    new_data1 = []
    for el in data1:
        new_data1.append(np.sum(el)/len(el))
    data1 = np.array(new_data1)
    
if len(data2.shape) > 1:
    new_data2 = []
    for el in data2:
        new_data2.append(np.sum(el)/len(el))
    data2 = np.array(new_data2)

# Print the difference
#print(difference) 

#fig, ax = plt.subplots()
#ax.plot(difference)
#fig.savefig("cross-correlation20.png")

#fig1, ax1 = plt.subplots()
#ax1.plot(difference1)
#fig1.savefig("cross-correlation10.png")



# Calculate the Euclidean distance between two arrays
def euclidean_distance(arr1, arr2):
    # Calculate the difference between the arrays
    diff = arr1 - arr2
    # Square the differences
    diff_squared = diff**2
    # Sum the squared differences
    sum_diff_squared = np.sum(diff_squared)
    # Take the square root of the sum of the squared differences
    distance = np.sqrt(sum_diff_squared)
    return distance

# Calculate the percentage of similarity or difference
# between two arrays using the Euclidean distance
def similarity_percentage(arr1, arr2):
    # Calculate the Euclidean distance between the arrays
    distance = euclidean_distance(arr1, arr2)
    # Calculate the maximum possible distance between the arrays
    max_distance = np.sqrt(np.sum(arr1**2) + np.sum(arr2**2))
    # Calculate the percentage of similarity or difference
    percentage = 1 - distance / max_distance
    return percentage

def compare_freq(audio1, audio2, sr):
    # computing fft for both waves 
    audio1_fft = np.fft.fft(audio1, sr)
    audio2_fft = np.fft.fft(audio2, sr)
    # will compare only real part of the ffts
    audio1_fft, audio2_fft = audio1_fft.real, audio2_fft.real
    return audio1_fft, audio2_fft, similarity_percentage(audio1_fft,audio2_fft)

audio1_fft, audio2_fft, similarity = compare_freq(data1, data2, rate1)
print(similarity)