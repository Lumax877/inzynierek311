import requests
from PIL import Image
import os
import io
import glob

path = "venv/generatedimages/script_v2"

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

def lorem_images(number, resolution, picpath):
    for i in range(0,number):
        while True:
            try:
                image_url = f'https://picsum.photos/{resolution[0]}/{resolution[1]}/?random'
                response = requests.get(image_url)

                if response.status_code == 200:
                    image = Image.open(io.BytesIO(response.content))

                    avg_color = calculate_average_color(image)

                    avg_color_str = "_".join(map(str, avg_color))

                    image.save(f"{picpath}/image_{i}_{avg_color_str}.png")
                    print(f"Generated image {i}")
                    break
            except requests.exceptions.RequestException as e:
                print(f"Failed to download image {i}, retrying...")


def check(dirpath):
    files = glob.glob(os.path.join(dirpath, '*'))

    for file_path in files:
        try:
            os.remove(file_path)
        except Exception as e:
            print(f"Error: {str(e)}")



