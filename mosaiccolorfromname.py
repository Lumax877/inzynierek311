from PIL import Image
import os
import re
import numpy as np

def load_images_from_directory(directory):
    directory = str(directory)  # parse error for some reason
    image_files = [f for f in os.listdir(directory) if f.endswith(('.png', '.jpg', '.jpeg'))]
    images = [Image.open(os.path.join(directory, f)).convert('RGB') for f in image_files]
    return images

def resize_image(image, size):
    return image.resize(size)

def get_average_color_from_name(name):
    match = re.match(r'image_(\d+)_(\d+)_(\d+)_(\d+)\.(png|jpg|jpeg)', name)
    if match:
        r, g, b, _ = match.groups()
        return tuple(map(int, [r, g, b]))

def create_mosaic(input_image_path, output_image_path, tile_directory, tile_size):
    input_image = Image.open(input_image_path)
    input_image = resize_image(input_image, (tile_size[0] * input_image.width // tile_size[0], tile_size[1] * input_image.height // tile_size[1]))

    tiles = load_images_from_directory(tile_directory)
    tile_size = tiles[0].size

    output_image = Image.new('RGB', input_image.size)

    input_colors = []
    for y in range(0, input_image.height, tile_size[1]):
        for x in range(0, input_image.width, tile_size[0]):
            region = (x, y, x + tile_size[0], y + tile_size[1])
            input_tile = input_image.crop(region)
            input_colors.append(np.array(input_tile).mean(axis=(0, 1)))

    for y in range(0, input_image.height, tile_size[1]):
        print(y)
        for x in range(0, input_image.width, tile_size[0]):
            region = (x, y, x + tile_size[0], y + tile_size[1])
            input_tile_color = input_colors.pop(0)

            best_match_tile, _ = min(tiles, key=lambda tile: np.linalg.norm(input_tile_color - tile[1]))
            best_match_tile = best_match_tile.resize(tile_size)
            output_image.paste(best_match_tile, region)

    output_image.save(output_image_path)

if __name__ == "__main__":
    input_image_path = "venv/generatedimages/some_input_images/lawka1000.jpg"
    output_image_path = "venv/generatedimages/some_input_images/lawkamosaic10k-4xgpt.jpg"
    tile_directory = "venv/generatedimages/script_v1"
    tile_size = (25, 25)

    create_mosaic(input_image_path, output_image_path, tile_directory, tile_size)
