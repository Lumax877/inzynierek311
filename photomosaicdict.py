import os
import re
import numpy as np
from PIL import Image
from skimage import color
import tqdm
import json


def rgb_to_lab(rgb):
    return color.rgb2lab([[rgb]])[0][0]

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

def find_most_similar_tile(target_color, tiles_color_dict, top_k=5):
    sorted_tiles = sorted(tiles_color_dict.items(), key=lambda x: color_difference(target_color, x[1]))

    for tile_filename, tile_color in sorted_tiles[:top_k]:
        return tile_filename

def mosaic_from_tiles_with_json(input_image_path, tiles_folder, output_path, tile_size=50):
    original_image = Image.open(input_image_path)
    original_w, original_h = original_image.size
    mosaic_image = Image.new('RGB', (original_w, original_h), (255, 255, 255))

    with open("tiles_color.json", 'r') as json_file:
        tiles_color_dict = json.load(json_file)

    for y in tqdm.tqdm(range(0, original_h, tile_size), desc="Rows"):
        for x in tqdm.tqdm(range(0, original_w, tile_size), desc="Columns", leave=False):
            region = original_image.crop((x, y, x + tile_size, y + tile_size))
            target_color = calculate_average_color(region)

            most_similar_tile_filename = find_most_similar_tile(target_color, tiles_color_dict)

            most_similar_tile_path = os.path.join(tiles_folder, most_similar_tile_filename)
            most_similar_tile = Image.open(most_similar_tile_path)
            mosaic_image.paste(most_similar_tile, (x, y))

    mosaic_image.save(output_path)

mosaic_from_tiles_with_json(
    input_image_path="venv/generatedimages/some_input_images/lawka1000.jpg",
    tiles_folder="venv/generatedimages/script_v1",
    output_path="venv/generatedimages/some_input_images/lawkamosaic30k_with_json.jpg"
)



