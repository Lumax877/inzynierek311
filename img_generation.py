from PIL import Image
import random
import os
import glob
import tqdm

path = "venv/generatedimages/script_v1"


def calculate_average_color(region):
    width, height = region.size
    r, g, b = 0, 0, 0

    for y in range(height):
        for x in range(width):
            pixel_color = region.getpixel((x, y))
            r += pixel_color[0]
            g += pixel_color[1]
            b += pixel_color[2]

    total_pixels = width * height
    avg_color = (r // total_pixels, g // total_pixels, b // total_pixels)
    return avg_color


def generate_images(number, resolution, picpath):
    for i in tqdm.tqdm(range(0, number), desc="Pictures", leave=False):
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        image = Image.new('RGB', resolution, color)

        avg_color = calculate_average_color(image)

        avg_color_str = "_".join(map(str, avg_color))

        image.save(f"{picpath}/image_{i}_{avg_color_str}.png")


def check(dirpath):
    files = glob.glob(os.path.join(dirpath, '*'))

    for file_path in files:
        try:
            os.remove(file_path)
        except Exception as e:
            print(f"Error: {str(e)}")