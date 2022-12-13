import numpy as np
from scipy.io import wavfile

import matplotlib.pyplot as plt

# Read in the two audio files
rate1, data1 = wavfile.read("borrar/stream1.wav")
rate2, data2 = wavfile.read("borrar/clip3.wav")

# Make sure the audio files have the same sample rate
if rate1 != rate2:
    raise ValueError("The sample rates of the two audio files must match")

data1 = np.resize(data1, data2.shape)

# Calculate the difference between the two audio files
difference = np.abs(data1 - data2)

# normalizing waves
data1 = data1/np.max(data1)
data2 = data2/np.max(data2)

# Print the difference
print(difference)
result = np.sum(difference)/np.sum(np.abs(data1)+np.abs(data2)) 
print(result)

fig, ax = plt.subplots()
ax.plot(result)
fig.savefig("result.png")

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

