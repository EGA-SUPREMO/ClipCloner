import numpy as np
from scipy.io import wavfile
from matplotlib import pyplot as plt

rate1, data1 = wavfile.read("clip1.wav")
rate2, data2 = wavfile.read("clip.wav")

if rate1 != rate2:
    raise ValueError("The sample rates of the two audio files must match")

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


# normalizing waves
data1 = data1/np.max(data1)
data2 = data2/np.max(data2)



def euclidean_distance(arr1, arr2):
    # Calculate the difference between the arrays
    diff = np.abs(arr1 - arr2)
    # Square the differences
    diff_squared = diff**2
    # Sum the squared differences
    sum_diff_squared = np.sum(diff_squared)
    # Take the square root of the sum of the squared differences
    distance = np.sqrt(sum_diff_squared)
    return distance

def similarity_percentage(arr1, arr2):
    # Calculate the Euclidean distance between the arrays
    distance = euclidean_distance(arr1, arr2)
    # Calculate the maximum possible distance between the arrays
    max_distance = np.sqrt(np.sum((np.abs(arr1)+np.abs(arr2))**2))
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


audio1_freq = np.fft.fftfreq(len(audio1_fft), d = 1/rate1)
audio2_freq = np.fft.fftfreq(len(audio2_fft), d = 1/rate2)

fig, ax = plt.subplots()
ax.plot(audio1_freq, audio1_fft, color="red")
fig.savefig("cross-correlation10.png")
fig1, ax1 = plt.subplots()
ax1.plot(audio2_freq, audio2_fft, color="blue") 
fig1.savefig("cross-correlation0.png")