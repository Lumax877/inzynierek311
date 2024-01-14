import os
import re
import numpy as np
from PIL import Image
from skimage import color
import tqdm



def rgb_to_lab(rgb):
    return color.rgb2lab([[rgb]])[0][0]

def extract_color_from_tile_filename(filename):
    match = re.match(r'image_(\d+)_(\d+)_(\d+)_(\d+)', filename)
    if match:
        return tuple(map(int, match.groups()[1:]))
    return None


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


def color_difference(color1, color2):
    lab1 = rgb_to_lab(color1)
    lab2 = rgb_to_lab(color2)
    return np.linalg.norm(lab1 - lab2)


def find_most_similar_tile(target_color, tile_filenames):
    min_difference = float('inf')
    most_similar_tile = None

    for tile_filename in tile_filenames:
        tile_color = extract_color_from_tile_filename(tile_filename)

        difference = color_difference(target_color, tile_color)

        if difference < min_difference:
            min_difference = difference
            most_similar_tile = tile_filename

    return most_similar_tile


def mosaic_from_tiles(input_image_path, tiles_folder, output_path, tile_size=25):
    original_image = Image.open(input_image_path)
    original_w, original_h = original_image.size

    mosaic_image = Image.new('RGB', (original_w, original_h), (255, 255, 255))

    tile_filenames = os.listdir(tiles_folder)

    for y in tqdm.tqdm(range(0, original_h, tile_size), desc="Rows"):
        for x in tqdm.tqdm(range(0, original_w, tile_size), desc="Columns", leave=False):
            region = original_image.crop((x, y, x + tile_size, y + tile_size))

            target_color = calculate_average_color(region)

            most_similar_tile_filename = find_most_similar_tile(target_color, tile_filenames)

            most_similar_tile_path = os.path.join(tiles_folder, most_similar_tile_filename)
            most_similar_tile = Image.open(most_similar_tile_path)
            mosaic_image.paste(most_similar_tile, (x, y))

    mosaic_image.save(output_path)

mosaic_from_tiles(
    input_image_path="venv/generatedimages/some_input_images/lawka1000.jpg",
    tiles_folder="venv/generatedimages/script_v1",
    output_path="venv/generatedimages/some_input_images/lawkamosaic10k-4x.jpg"
)