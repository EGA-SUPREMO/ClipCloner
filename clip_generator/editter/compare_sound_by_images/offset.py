from PIL import Image

# Open the two images
image1 = Image.open('clip1.png')
image2 = Image.open('stream1.png')

def blending(image1, image2, offset_x):
    # Add an offset to image2 by pasting it onto a blank image and then resizing it
    offset_image = Image.new('RGBA', image2.size, (0, 0, 0, 0))
    offset_image.paste(image2, (offset_x, 0))
    offset_image = offset_image.resize(image2.size)

    # Get the size of the intersection of the two images
    intersection_width = min(image1.size[0], image2.size[0] - offset_x)
    intersection_height = min(image1.size[1], image2.size[1])

    # Blend the images
    blended_image = Image.blend(image1, offset_image, alpha=0.5)

    # Crop the blended image to the intersection size
    cropped_image = blended_image.crop((offset_x, 0, intersection_width + offset_x, intersection_height))

    # Save the blended image
    cropped_image.save(f'blending/blended_image{offset_x}.png')

    return cropped_image

for x in range(image1.width):
    blended_image = blending(image1, image2, x)

# Iterate over the pixels and count the red ones
def count_colored_pixels(pixels: list[tuple[int, int, int, int]]) -> dict[str, int]:
    result = {'purple': 0, 'blue': 0, 'red': 0, 'other': 0}
    for pixel in pixels:
        match(pixel):
            case (127, 0, 127, 254):
                result['purple'] += 1
            case (0, 0, 127, 127):
                result['blue'] += 1
            case (127, 0, 0, 127):
                result['red'] += 1
            case (0, 0, 0, 0):
                pass
            case _:
                result['other'] += 1
    return result

# Get the pixel data for the image
pixels = blended_image.getdata()
result = count_colored_pixels(pixels)

print(f'Number of red pixels: {result["red"]}')
print(f'Number of blue pixels: {result["blue"]}')
print(f'Number of purple pixels: {result["purple"]}')
print(f'Number of other non transparent pixels: {result["other"]}')

