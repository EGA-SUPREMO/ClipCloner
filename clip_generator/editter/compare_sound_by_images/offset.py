from PIL import Image

from matplotlib import pyplot as plt

# Open the two images
clip_image = Image.open('clip30.png')
stream_image = Image.open('stream.png')

def blending(image1, image2, offset_x):
    # Add an offset to image2 by pasting it onto a blank image and then resizing it
    offset_image = Image.new('RGBA', image2.size, (0, 0, 0, 0))
    offset_image.paste(image2, (offset_x, 0))
    offset_image = offset_image.resize(image2.size)

    # Get the size of the intersection of the two images
    intersection_width = min(image1.size[0] - offset_x, image2.size[0])
    intersection_height = min(image1.size[1], image2.size[1])

    offset_image = offset_image.resize(image1.size)
    # Blend the images
    blended_image = Image.blend(image1, offset_image, alpha=0.5)

    # Crop the blended image to the intersection size
    cropped_image = blended_image.crop((offset_x, 0, intersection_width + offset_x, intersection_height))

    # Save the blended image
    cropped_image.save(f'blending/blended_image{offset_x}.png')

    return cropped_image


def relation_percentage(value1: int, value2: int) -> float:
    value1 = max(value1, 1)
    value2 = max(value2, 1)
    
    return 100 * value1 / (value1 + value2)

# Iterate over the pixels and count the red ones
def count_colored_pixels(pixels: list[tuple[int, int, int, int]]) -> dict[str, int]:
    result = {'purple': 0, 'blue': 0, 'red': 0, 'none': 0, 'other': 0}
    for pixel in pixels:
        match(pixel):
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

line = []
lineamount = []
line_average = []
for x in range(stream_image.width):
    blended_image = blending(clip_image, stream_image, x)
    # Get the pixel data for the image
    pixels = blended_image.getdata()
    result = count_colored_pixels(pixels)
    mismatch_pixels = result["red"] + result["blue"] + result["other"]
    accuracy = relation_percentage(result["purple"], mismatch_pixels)
    amount = relation_percentage(result["purple"] + mismatch_pixels, result["none"] + (x * clip_image.height))

    line.append(accuracy)
    lineamount.append(amount)
    line_average.append((accuracy * 0.3) + (amount * 0.7))

fig, ax = plt.subplots()
ax.plot(line, color="red")
ax.plot(lineamount, color="blue")
ax.plot(line_average, color="green")
fig.savefig("cross-correlation10.png")

print(f'Number of red pixels: {result["red"]}')
print(f'Number of blue pixels: {result["blue"]}')
print(f'Number of purple pixels: {result["purple"]}')
print(f'Number of other non transparent pixels: {result["other"]}')

