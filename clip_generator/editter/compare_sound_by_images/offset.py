from typing import Tuple, List

from PIL import Image
import os

from matplotlib import pyplot as plt
import clip_generator.editter.dirs as dirs


def image_blend(clip_image, stream_image, offset_x):
    if offset_x < 0:
        raise ValueError("Input offset_x must be positive")
    if stream_image.mode != clip_image.mode:
        raise ValueError("Stream image and clip image don't have the same mode")
    # Add an offset to stream_image by pasting it onto a blank image and then crop it
    offset_image = Image.new('RGBA', (clip_image.width + offset_x, clip_image.height), (0, 0, 0, 0))
    offset_image.paste(clip_image, (offset_x, 0))

    # Get the size of the intersection of the two images
    intersection_width = min(clip_image.size[0], stream_image.size[0] - offset_x)
    intersection_height = min(clip_image.size[1], stream_image.size[1])

    # Check if the images have the same size and mode
    if stream_image.size != offset_image.size:
        # crop to the size of stream_image
        offset_image = offset_image.crop((0, 0, stream_image.width, stream_image.height))
    # Blend the images
    blended_image = Image.blend(stream_image, offset_image, alpha=0.5)

    # Crop the blended image to the intersection size
    cropped_image = blended_image.crop((offset_x, 0, intersection_width + offset_x, intersection_height))

    return cropped_image


def relation_percentage(value1: int, value2: int) -> float:
    if value1 < 0 or value2 < 0:
        raise ValueError("Input values must be positive")

    value1 = max(value1, 1)
    value2 = max(value2, 1)

    return 100 * value1 / (value1 + value2)


# Iterate over the pixels and count the red ones
def count_colored_pixels(pixels: list[tuple[int, int, int, int]]) -> dict[str, int]:
    result = {'purple': 0, 'blue': 0, 'red': 0, 'none': 0, 'other': 0}
    for pixel in pixels:
        match pixel:
            case (127, 0, 127, 254):
                result['purple'] += 1
            case (0, 0, 127, 127):
                result['blue'] += 1
            case (127, 0, 0, 127):
                result['red'] += 1
            case (0, 0, 0, 0):
                result['none'] += 1
            case _:
                result['other'] += 1
    return result


def compare_images(clip_image: Image, stream_image: Image) -> tuple[
        list[float], list[float], list[float]]:
    indexes_accuracy = []
    indexes_similarity = []
    indexes_average = []
    x = 0

    clip_image = crop_height_image(clip_image, 256, 256)
    stream_image = crop_height_image(stream_image, 256, 256)

    offsets = range(stream_image.width - clip_image.width)

    for offset in offsets:
        blended_image = image_blend(clip_image, stream_image, offset)
        pixels = blended_image.getdata()
        result = count_colored_pixels(pixels)

        similarity, accuracy = calculate_similarity_and_accuracy(result)

        x += 1
        indexes_similarity.append(similarity)
        indexes_accuracy.append(accuracy)
        indexes_average.append(accuracy * 0.5 + similarity * 0.5)

    return indexes_similarity, indexes_accuracy, indexes_average


def save_data(indexes_similarity: list[float], indexes_accuracy: list[float], indexes_average: list[float], foldername: str):
    os.makedirs(foldername, exist_ok=True)

    write_sorted_values(indexes_similarity, foldername + "indices_similarity.txt")
    write_sorted_values(indexes_accuracy, foldername + "indices_accuracy.txt")
    write_sorted_values(indexes_average, foldername + "indices_average.txt")

    draw_plot_indexes(indexes_similarity, indexes_accuracy, indexes_average, foldername + "testo.png")


def draw_plot_indexes(indexes_similarity, indexes_accuracy, indexes_average, filename):
    fig, ax = plt.subplots(figsize=(45, 10))
    ax.plot(indexes_similarity, color="red")
    ax.plot(indexes_accuracy, color="blue")
    ax.plot(indexes_average, color="purple")
    fig.savefig(filename)


def write_sorted_values(values: list[float], file_path: str):
    sorted_array = sorted(enumerate(values), key=lambda x: x[1], reverse=True)
    with open(file_path, "w") as f:
        for i, element in sorted_array:
            f.write(f"{element} in {i}\n")


# TODO TESTSETSESTS
def pixels_into_seconds(seconds: int):
    return seconds / dirs.scale_edit


# TODO update tests, make them tests the results itself!!!!!1, needs compare the files pregenerated
def calculate_similarity_and_accuracy(result):
    # Calculate the similarity
    match_pixels = result["purple"]
    mismatch_pixels = result["red"] + result["blue"] + result["other"]
    similarity = relation_percentage(match_pixels, mismatch_pixels)

    # Calculate the accuracy, this has a bug where the higher the mismatch, the higher the accuracy, that's because
    # when there is a mismatch, there is more red and blue, a potencial solution is to multiply by two purple pixels and
    # or divide by two red and blue
    match_mismatch = match_pixels*2 + mismatch_pixels/2
    null = result["none"]

    accuracy = relation_percentage(match_mismatch, null)

    return similarity, accuracy


def crop_height_image(image, y_offset, height):
    # Crop the image to the specified size
    image = image.crop((0, y_offset, image.width, height + y_offset))

    return image


def crop_width_image(image, x_offset, width):
    # Crop the image to the specified size
    image = image.crop((x_offset, 0, width + x_offset, image.height))

    return image


if __name__ == '__main__':
    stream_image = Image.open('stream.png')
    clip_image = Image.open('330.png')

    indexes_similarity, indexes_accuracy, indexes_average = compare_images(clip_image, stream_image)
    save_data(indexes_similarity, indexes_accuracy, indexes_average, "typical_test/")
