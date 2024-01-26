from PIL import Image
import os
import re
import numpy as np
import tqdm


def load_images_from_directory(directory):
    directory = str(directory)
    image_files = [f for f in os.listdir(directory) if f.endswith(('.png', '.jpg', '.jpeg'))]
    images = []

    for f in image_files:
        match = re.match(r'image_(\d+)_(\d+)_(\d+)_(\d+)\.(png|jpg|jpeg)', f)
        if match:
            i, r, g, b, _ = match.groups()
            color = tuple(map(int, [r, g, b]))
            image_path = os.path.join(directory, f)
            images.append((Image.open(image_path).convert('RGB'), color))

    print("Tiles loaded")
    return images

def resize_image(image, size):
    return image.resize(size)

def calculate_scale_factor(tile_size, region_size):
    scale_factor = max(tile_size) / region_size
    return scale_factor

def create_mosaic(input_image_path, output_image_path, tile_directory, tile_size, region_size):
    input_image = Image.open(input_image_path)

    adjusted_width = (input_image.width // region_size) * region_size
    adjusted_height = (input_image.height // region_size) * region_size

    input_image = resize_image(input_image, (adjusted_width, adjusted_height))

    tiles = load_images_from_directory(tile_directory)

    scale_factor = calculate_scale_factor(tile_size, region_size)

    output_width = int(adjusted_width * scale_factor)
    output_height = int(adjusted_height * scale_factor)

    output_image = Image.new('RGB', (output_width, output_height))

    input_colors = []
    for y in range(0, adjusted_height, region_size):
        for x in range(0, adjusted_width, region_size):
            region = (x, y, x + region_size, y + region_size)
            input_tile = input_image.crop(region)
            input_colors.append(np.array(input_tile).mean(axis=(0, 1)))

    for y in tqdm.tqdm(range(0, output_height, tile_size[1]), desc="Rows", leave=False):
        for x in range(0, output_width, tile_size[0]):
            region = (x, y, x + tile_size[0], y + tile_size[1])
            input_tile_color = input_colors.pop(0)

            best_match_tile = min(tiles, key=lambda tile: np.linalg.norm(input_tile_color - tile[1]))
            best_match_tile = best_match_tile[0].resize(tile_size)
            output_image.paste(best_match_tile, region)

    output_image.save(output_image_path)

if __name__ == "__main__":
    input_image_path = "venv/generatedimages/some_input_images/dziadufolud.jpg"
    output_image_path = "venv/generatedimages/some_input_images/dziadufloud500-tile100-reg10-10k.jpg"
    tile_directory = "venv/generatedimages/script_v2"
    tile_size = (100, 100)
    region_size = 10

    create_mosaic(input_image_path, output_image_path, tile_directory, tile_size, region_size)
