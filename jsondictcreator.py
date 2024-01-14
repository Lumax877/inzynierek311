import json
import os
from PIL import Image

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


def create_tiles_color_json(tiles_folder, output_json_path):
    tiles_color_dict = {}

    for tile_filename in os.listdir(tiles_folder):
        tile_path = os.path.join(tiles_folder, tile_filename)
        tile_color = calculate_average_color(Image.open(tile_path))
        tiles_color_dict[tile_filename] = tile_color
        print(tile_filename)

    with open(output_json_path, 'w') as json_file:
        json.dump(tiles_color_dict, json_file)


create_tiles_color_json("venv/generatedimages/script_v1", "tiles_color.json")
