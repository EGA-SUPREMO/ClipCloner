import timeit
import numpy as np
import cv2

def compare_images(clip_image, stream_image, offsets):
    # Convert the images to grayscale
    clip_image = cv2.cvtColor(clip_image, cv2.COLOR_BGR2GRAY)
    stream_image = cv2.cvtColor(stream_image, cv2.COLOR_BGR2GRAY)

    # Calculate the difference between the two images
    difference = cv2.absdiff(clip_image, stream_image)

    # Threshold the difference image to create a black and white image
    threshold = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)[1]

    # Calculate the number of white pixels in the threshold image
    white_pixels = np.sum(threshold == 255)

    # Calculate the accuracy, average, and amount of lines
    line_accuracy = white_pixels / (clip_image.shape[0] * clip_image.shape[1])
    line_average = white_pixels / clip_image.shape[0]
    line_amount = white_pixels / clip_image.shape[1]

    return line_accuracy, line_average, line_amount

clip_image = # image data
stream_image = # image data
offsets = (10, 10)

execution_time = timeit.timeit(lambda: compare_images(clip_image, stream_image, offsets), number=1)
print(f'Execution time: {execution_time:.6f} seconds')
