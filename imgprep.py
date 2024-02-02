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

def process_images_in_folder(folder_path):
    if not os.path.isdir(folder_path):
        raise ValueError("Podana ścieżka nie prowadzi do folderu.")

    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']

    all_files = os.listdir(folder_path)

    image_files = [f for f in all_files if os.path.isfile(os.path.join(folder_path, f)) and os.path.splitext(f)[1].lower() in image_extensions]

    if not image_files:
        raise ValueError("W folderze nie ma żadnych obrazów.")

    if len(all_files) != len(image_files):
        raise ValueError("W folderze znajdują się również inne pliki niż obrazy. Nie można obliczyć średnich wartości kolorów.")

    for i, image_file in enumerate(image_files, start=1):
        image_path = os.path.join(folder_path, image_file)
        try:
            image = Image.open(image_path)
            avg_color = calculate_average_color(image)
            new_name = f"image_{i}_{avg_color[0]}_{avg_color[1]}_{avg_color[2]}{os.path.splitext(image_file)[1].lower()}"
            new_path = os.path.join(folder_path, new_name)
            os.rename(image_path, new_path)
            print(f"Pomyślnie przetworzono {image_file}. Nowa nazwa: {new_name}")
        except Exception as e:
            print(f"Błąd podczas przetwarzania {image_file}: {str(e)}")
