from typing import Tuple, List

from PIL import Image
import os

from matplotlib import pyplot as plt


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


def compare_images(clip_image: Image, stream_image: Image, offsets: list[int]) -> tuple[
        list[float], list[float], list[float]]:
    line_accuracy = []
    line_amount = []
    line_average = []
    x = 0

    for offset in offsets:
        blended_image = image_blend(clip_image, stream_image, offset)
        pixels = blended_image.getdata()
        result = count_colored_pixels(pixels)

        accuracy, amount = calculate_accuracy_and_amount(result)

        x += 1
        line_accuracy.append(accuracy)
        line_amount.append(amount)
        line_average.append((accuracy * 0.3) + (amount * 0.7))

    return line_accuracy, line_amount, line_average


def save_data(line_accuracy: list[float], line_average: list[float], line_amount: list[float], foldername: str):
    os.makedirs(foldername, exist_ok=True)

    write_sorted_values(line_accuracy, foldername + "indices_accuracy.txt")
    write_sorted_values(line_average, foldername + "indices_average.txt")
    write_sorted_values(line_amount, foldername + "indices_amount.txt")

    draw_average_plot_lines(line_accuracy, line_amount, line_average, foldername + "testo.png")


def draw_average_plot_lines(line_accuracy, line_amount, line_average, filename):
    fig, ax = plt.subplots(figsize=(45, 10))
    ax.plot(line_accuracy, color="red")
    ax.plot(line_amount, color="blue")
    ax.plot(line_average, color="green")
    fig.savefig(filename)


def write_sorted_values(values: list[float], file_path: str):
    sorted_array = sorted(enumerate(values), key=lambda x: x[1], reverse=True)
    with open(file_path, "w") as f:
        for i, element in sorted_array:
            f.write(f"{element} in {i}\n")


def calculate_accuracy_and_amount(result):
    # Calculate the accuracy
    mismatch_pixels = result["red"] + result["blue"] + result["other"]
    accuracy = relation_percentage(result["purple"], mismatch_pixels)

    # Calculate the amount
    amount = relation_percentage(result["purple"] + mismatch_pixels, result["none"] + (0 * clip_image.height))

    return accuracy, amount


# TODO Needs tests
def crop_height_image(image):
    # Crop the image to the specified size
    image = image.crop((0, 0, image.width, 512))
    image = image.crop((0, 256, image.width, 512))

    return image


if __name__ == '__main__':
    stream_image = Image.open('stream2022.png')
    clip_image = Image.open('clip2022.png')

    clip_image = crop_height_image(clip_image)
    stream_image = crop_height_image(stream_image)

    offsets = range(stream_image.width)
    line_accuracy, line_average, line_amount = compare_images(clip_image, stream_image, offsets)
    save_data(line_accuracy, line_average, line_amount, "typical_test/")
