import timeit

from PIL import Image

from clip_generator.editter.compare_sound_by_images.offset import compare_images

# Test scenario 1: compare a normal worstaudio stream of 13K seconds, nene gets tricked by viewers
clip_image = Image.open('clip2022.png')
stream_image = Image.open('stream2022.png')

return_values = compare_images(clip_image, stream_image)
execution_time = timeit.timeit(lambda: return_values, number=1)
print(f'Execution time for test scenario 1: {execution_time:.6f} seconds')

print(f'Return values:' + str(len(return_values[0])))

# # Test scenario 2: compare two large images with a large offset
# clip_image = # large image data
# stream_image = # large image data
# offsets = (1000, 1000)
# execution_time = timeit.timeit(lambda: compare_images(clip_image, stream_image, offsets), number=1)
# print(f'Execution time for test scenario 2: {execution_time:.6f} seconds')

# # Test scenario 3: compare two images with different sizes and a small offset
# clip_image = # small image data
# stream_image = # large image data
# offsets = (10, 10)
# execution_time = timeit.timeit(lambda: compare_images(clip_image, stream_image, offsets), number=1)
# print(f'Execution time for test scenario 3: {execution_time:.6f} seconds')
