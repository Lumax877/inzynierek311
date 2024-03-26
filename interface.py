import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image
from finalscript import create_mosaic
import os
from img_generation import generate_images, check
from lorempicsum import lorem_images
from imgprep import process_images_in_folder
import threading

class MosaicApp:
    def __init__(self, master):
        self.master = master
        master.title("Mosaic Generator")

        self.tabControl = ttk.Notebook(master)
        self.tab1 = ttk.Frame(self.tabControl)
        self.tab2 = ttk.Frame(self.tabControl)
        self.tab3 = ttk.Frame(self.tabControl)
        self.tab4 = ttk.Frame(self.tabControl)
        self.tab5 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab1, text="Mosaic Generator")
        self.tabControl.add(self.tab2, text="Single-Color Tile Generator")
        self.tabControl.add(self.tab3, text="Lorem Picsum Pictures Generator")
        self.tabControl.add(self.tab4, text="Custom Images Preparator")
        self.tabControl.add(self.tab5, text="Help / How to Use")
        self.tabControl.pack(expand=1, fill="both")

        self.setup_mosaic_tab()
        self.setup_image_tab()
        self.setup_lorem_tab()
        self.setup_prep_tab()
        self.setup_help_tab()

    def setup_mosaic_tab(self):
        self.input_image_path = tk.StringVar()
        self.tile_directory = tk.StringVar()
        self.output_image_path = tk.StringVar()
        self.tile_size = tk.StringVar()
        self.target_region_size = tk.StringVar()
        self.progress_string = tk.StringVar()
        self.progress_string.set("Waiting for user's input data...")

        self.input_path_label = ttk.Label(self.tab1, text="Input Image Path:")
        self.input_path_label.pack()

        self.input_path_scrollbar = ttk.Scrollbar(self.tab1, orient="horizontal")
        self.input_path_entry = ttk.Entry(self.tab1, textvariable=self.input_image_path, xscrollcommand=self.input_path_scrollbar.set)
        self.input_path_scrollbar.config(command=self.input_path_entry.xview)

        self.input_path_entry.pack(fill="x")
        self.input_path_scrollbar.pack(fill="x")

        self.input_button = tk.Button(self.tab1, text="Select Input Image", command=self.select_input_image)
        self.input_button.pack()

        self.input_file_label = ttk.Label(self.tab1, text="Tile Directory Path:")
        self.input_file_label.pack()

        self.tile_path_scrollbar = ttk.Scrollbar(self.tab1, orient="horizontal")
        self.tile_path_entry = ttk.Entry(self.tab1, textvariable=self.tile_directory, xscrollcommand=self.tile_path_scrollbar.set)
        self.tile_path_scrollbar.config(command=self.tile_path_entry.xview)

        self.tile_path_entry.pack(fill="x")
        self.tile_path_scrollbar.pack(fill="x")

        self.tile_button = tk.Button(self.tab1, text="Select Tile Directory", command=self.select_tile_directory)
        self.tile_button.pack()

        self.output_file_label = ttk.Label(self.tab1, text="Output Image Path:")
        self.output_file_label.pack()

        self.output_path_scrollbar = ttk.Scrollbar(self.tab1, orient="horizontal")
        self.output_path_entry = ttk.Entry(self.tab1, textvariable=self.output_image_path, xscrollcommand=self.output_path_scrollbar.set)
        self.output_path_scrollbar.config(command=self.output_path_entry.xview)

        self.output_path_entry.pack(fill="x")
        self.output_path_scrollbar.pack(fill="x")

        self.output_button = tk.Button(self.tab1, text="Select Output Image Path", command=self.select_output_image)
        self.output_button.pack()

        tk.Label(self.tab1, text="Tile Size:").pack()
        self.tile_size_entry = tk.Entry(self.tab1, textvariable=self.tile_size)
        self.tile_size_entry.pack()

        tk.Label(self.tab1, text="Target Region Size:").pack()
        self.target_region_size_entry = tk.Entry(self.tab1, textvariable=self.target_region_size)
        self.target_region_size_entry.pack()

        self.run_button = tk.Button(self.tab1, text="Generate Mosaic", command=self.generate_mosaic_thread)
        self.run_button.pack()

        self.info = ttk.Label(self.tab1, text="Please use buttons instead of textboxes to select required files.")
        self.info.pack()

        self.info2 = ttk.Label(self.tab1, text="Remember that non-square images will be resized to a square to match the place to paste.")
        self.info2.pack()

        self.custom = ttk.Label(self.tab1, text= "---------------------------------------------------------------")
        self.custom.pack()

        self.progress1 = ttk.Label(self.tab1, textvariable=self.progress_string)
        self.progress1.pack()

    def select_input_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if file_path and not self.is_valid_image(file_path):
            print("Invalid input file. Please select a valid image.")
            self.progress_string.set("Invalid input file. Please select a valid image.")
            return
        self.input_image_path.set(file_path)
        self.progress_string.set("Waiting for user's input data...")

    def select_tile_directory(self):
        dir_path = filedialog.askdirectory()
        if dir_path and not self.contains_valid_images(dir_path):
            print("Invalid tile directory. Please select a directory containing valid image files.")
            self.progress_string.set("Invalid tile directory. Please select a directory containing valid image files.")
            return
        self.tile_directory.set(dir_path)
        self.progress_string.set("Waiting for user's input data...")

    def select_output_image(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg")])
        self.output_image_path.set(file_path)

    def generate_mosaic_thread(self):
        threading.Thread(target=self.generate_mosaic).start()

    def generate_mosaic(self):
        input_path = self.input_image_path.get()
        tile_dir = self.tile_directory.get()
        output_path = self.output_image_path.get()

        try:
            tile_size = int(self.tile_size.get())
            target_region_size = int(self.target_region_size.get())
        except ValueError:
            print("Invalid input for Tile Size or Target Region Size. Please enter valid integers.")
            self.progress_string.set("Invalid input for Tile Size or Target Region Size. Please enter valid integers.")
            return

        if not input_path or not tile_dir or not output_path:
            print("Please select input image, tile directory, and output image path.")
            self.progress_string.set("Please select input image, tile directory, and output image path.")
            return

        if not self.is_valid_image(input_path):
            print("Invalid input file. Please select a valid image.")
            self.progress_string.set("Invalid input file. Please select a valid image.")
            return

        if not self.contains_valid_images(tile_dir):
            print("Invalid tile directory. Please select a directory containing valid image files.")
            self.progress_string.set("Invalid tile directory. Please select a directory containing valid image files.")
            return

        self.progress_string.set("Generating photomosaic. This may take up to several minutes...")
        create_mosaic(input_path, output_path, tile_dir, tile_size=(tile_size, tile_size), region_size=target_region_size)
        print("Mosaic generated successfully!")
        self.progress_string.set("Photomosaic made successfully.")

    def setup_image_tab(self):
        self.num_generated_images = tk.StringVar()
        self.generated_image_size = tk.StringVar()
        self.generated_images_path = tk.StringVar()
        self.progress_string2 = tk.StringVar()
        self.progress_string2.set("Waiting for user's input data...")

        tk.Label(self.tab2, text="Number of Generated Images:").pack()
        self.num_generated_images_entry = tk.Entry(self.tab2, textvariable=self.num_generated_images)
        self.num_generated_images_entry.pack()

        tk.Label(self.tab2, text="Generated Image Size (square):").pack()
        self.generated_image_size_entry = tk.Entry(self.tab2, textvariable=self.generated_image_size)
        self.generated_image_size_entry.pack()

        self.folder_path_label = ttk.Label(self.tab2, text="Tile Folder Path:")
        self.folder_path_label.pack()

        self.folder_path_scrollbar = ttk.Scrollbar(self.tab2, orient="horizontal")
        self.folder_path_entry = ttk.Entry(self.tab2, textvariable=self.generated_images_path, xscrollcommand=self.folder_path_scrollbar.set)
        self.folder_path_scrollbar.config(command=self.folder_path_entry.xview)

        self.folder_path_entry.pack(fill="x")
        self.folder_path_scrollbar.pack(fill="x")

        self.generated_images_path_button = tk.Button(self.tab2, text="Select Folder", command=self.select_generated_images_path)
        self.generated_images_path_button.pack()

        self.generate_images_button = tk.Button(self.tab2, text="Generate Images", command=self.generate_images_thread)
        self.generate_images_button.pack()

        self.info2 = ttk.Label(self.tab2, text="Warning: all files in the selected folder will be deleted when generating starts.")
        self.info2.pack()

        self.custom2 = ttk.Label(self.tab2, text="---------------------------------------------------------------")
        self.custom2.pack()

        self.progress2 = ttk.Label(self.tab2, textvariable=self.progress_string2)
        self.progress2.pack()

    def select_generated_images_path(self):
        folder_path = filedialog.askdirectory()
        self.generated_images_path.set(folder_path)

    def is_path_variable_empty(self, path_variable):
        return not path_variable.get()

    def generate_images_thread(self):
        threading.Thread(target=self.generate_images).start()

    def generate_images(self):
        if self.is_path_variable_empty(self.generated_images_path):
            self.progress_string2.set("Please select a folder to save images in.")
            print("Please select a folder to save images in.")
            return
        picpath = self.generated_images_path.get()
        try:
            num_images = int(self.num_generated_images.get())
            image_size = int(self.generated_image_size.get())
        except ValueError:
            print("Invalid input for Number of Generated Images or Generated Image Size. Please enter valid integers.")
            self.progress_string2.set("Invalid input for Number of Generated Images or Generated Image Size. Please enter valid integers.")
            return

        check(picpath)
        self.progress_string2.set("Generating images...")
        generate_images(num_images, (image_size, image_size), picpath)
        self.progress_string2.set("Generating images completed.")
        print(f"{num_images} images generated successfully!")

    def is_valid_image(self, file_path):
        try:
            img = Image.open(file_path)
            img.close()
            return True
        except (IOError, SyntaxError):
            return False
    def is_valid_image_filename(self, filename):
        parts = filename.split('_')
        extpart = parts[4].split('.')
        if len(parts) == 5 and parts[0] == 'image' and all(
                part.isdigit() for part in (parts[1], parts[2], parts[3], extpart[0])):
            return True
        return False

    def contains_valid_images(self, dir_path):
        if not os.path.exists(dir_path):
            return False

        for filename in os.listdir(dir_path):
            file_path = os.path.join(dir_path, filename)
            if os.path.isfile(file_path) and not (self.is_valid_image(file_path) and self.is_valid_image_filename(filename)):
                return False

        return True

    def setup_lorem_tab(self):
        self.num_lorem_images = tk.StringVar()
        self.lorem_image_size = tk.StringVar()
        self.lorem_images_path = tk.StringVar()
        self.progress_string3 = tk.StringVar()
        self.progress_string3.set("Waiting for user's input data...")

        tk.Label(self.tab3, text="Number of Downloaded Images:").pack()
        self.num_lorem_images_entry = tk.Entry(self.tab3, textvariable=self.num_lorem_images)
        self.num_lorem_images_entry.pack()

        tk.Label(self.tab3, text="Downloaded Image Size (square):").pack()
        self.lorem_image_size_entry = tk.Entry(self.tab3, textvariable=self.lorem_image_size)
        self.lorem_image_size_entry.pack()

        self.lorem_path_label = ttk.Label(self.tab3, text="Tile Folder Path:")
        self.lorem_path_label.pack()

        self.lorem_path_scrollbar = ttk.Scrollbar(self.tab3, orient="horizontal")
        self.lorem_path_entry = ttk.Entry(self.tab3, textvariable=self.lorem_images_path, xscrollcommand=self.lorem_path_scrollbar.set)
        self.lorem_path_scrollbar.config(command=self.lorem_path_entry.xview)

        self.lorem_path_entry.pack(fill="x")
        self.lorem_path_scrollbar.pack(fill="x")

        self.lorem_images_path_button = tk.Button(self.tab3, text="Select Folder", command=self.select_lorem_images_path)
        self.lorem_images_path_button.pack()

        self.lorem_images_button = tk.Button(self.tab3, text="Download Images", command=self.lorem_images_thread)
        self.lorem_images_button.pack()

        self.info = ttk.Label(self.tab3, text="Warning: all files in the selected folder will be deleted when downloading starts.")
        self.info.pack()

        self.custom3 = ttk.Label(self.tab3, text="---------------------------------------------------------------")
        self.custom3.pack()

        self.progress3 = ttk.Label(self.tab3, textvariable=self.progress_string3)
        self.progress3.pack()

    def select_lorem_images_path(self):
        folder_path = filedialog.askdirectory()
        self.lorem_images_path.set(folder_path)

    def lorem_images_thread(self):
        threading.Thread(target=self.lorem_images).start()

    def lorem_images(self):
        if self.is_path_variable_empty(self.lorem_images_path):
            print("Please select a folder to save images in.")
            self.progress_string3.set("Please select a folder to save images in.")
            return
        picpath = self.lorem_images_path.get()
        try:
            num_images = int(self.num_lorem_images.get())
            image_size = int(self.lorem_image_size.get())
        except ValueError:
            print("Invalid input for Number of Generated Images or Generated Image Size. Please enter valid integers.")
            self.progress_string3.set("Invalid input for Number of Generated Images or Generated Image Size. Please enter valid integers.")
            return

        check(picpath)
        self.progress_string3.set("Downloading images...")
        lorem_images(num_images, (image_size, image_size), picpath)
        self.progress_string3.set("Images downloaded successfully.")
        print(f"{num_images} images generated successfully!")

    def setup_prep_tab(self):
        self.prep_folder_path = tk.StringVar()
        self.progress_string4 = tk.StringVar()
        self.progress_string4.set("Waiting for user's input data...")

        self.prep_path_label = ttk.Label(self.tab4, text="Images Folder Path:")
        self.prep_path_label.pack()

        self.prep_path_scrollbar = ttk.Scrollbar(self.tab4, orient="horizontal")
        self.prep_path_entry = ttk.Entry(self.tab4, textvariable=self.prep_folder_path, xscrollcommand=self.prep_path_scrollbar.set)
        self.prep_path_scrollbar.config(command=self.prep_path_entry.xview)

        self.prep_path_entry.pack(fill="x")
        self.prep_path_scrollbar.pack(fill="x")

        self.prep_images_path_button = tk.Button(self.tab4, text="Select Folder", command=self.select_prep_images_path)
        self.prep_images_path_button.pack()

        self.lorem_images_button = tk.Button(self.tab4, text="Prepare Images", command=self.prep_images_thread)
        self.lorem_images_button.pack()

        self.info41 = ttk.Label(self.tab4, text="Please be aware that this program will not run unless the selected folder will contain only image files.")
        self.info41.pack()

        self.custom3 = ttk.Label(self.tab4, text="---------------------------------------------------------------")
        self.custom3.pack()

        self.progress3 = ttk.Label(self.tab4, textvariable=self.progress_string4)
        self.progress3.pack()

    def select_prep_images_path(self):
        folder_path = filedialog.askdirectory()
        self.prep_folder_path.set(folder_path)

    def prep_images_thread(self):
        threading.Thread(target=self.prep_images).start()

    def prep_images(self):
        if self.is_path_variable_empty(self.prep_folder_path):
            print("Please select a folder with valid images.")
            self.progress_string4.set("Please select a folder with valid images.")
            return

        image_extensions = ['.jpg', '.jpeg', '.png']

        all_files = os.listdir(self.prep_folder_path.get())

        image_files = [f for f in all_files if os.path.isfile(os.path.join(self.prep_folder_path.get(), f)) and os.path.splitext(f)[
            1].lower() in image_extensions]

        if not image_files:
            self.progress_string4.set("No images detected in selected folder.")
            raise ValueError("No images detected in selected folder.")

        if len(all_files) != len(image_files):
            self.progress_string4.set("Detected non-graphic files. Cannot prepare images.")
            raise ValueError(
                "Detected non-graphic files. Cannot prepare images.")

        picpath = self.prep_folder_path.get()
        self.progress_string4.set("Preparing images...")
        process_images_in_folder(picpath, image_files)
        self.progress_string4.set("Images renamed successfully.")
        print(f"Images renamed successfully!")

    def setup_help_tab(self):
        self.info51 = ttk.Label(self.tab5, text="In order to use Mosaic Generator, you must select image you want to make photomosaic of (input image)")
        self.info52 = ttk.Label(self.tab5, text="and folder containing images that photomosaic will be made of (tile folder).")
        self.info53 = ttk.Label(self.tab5, text="Also you need to write charactercistics of the photomosaic, which are region size and tile size.")
        self.info54 = ttk.Label(self.tab5, text="Region size is the size of squares that photomosaic will be \"cut\" into.")
        self.info55 = ttk.Label(self.tab5, text="The color values of each region will be calculated independently.")
        self.info56 = ttk.Label(self.tab5, text="Then, generator will chose the most similar image from tile folder (tile).")
        self.info57 = ttk.Label(self.tab5, text="Each selected tile will be resized to match the value of previously declared \"tile size\". ")
        self.info58 = ttk.Label(self.tab5, text="For example, if region size equals 10, and tile size equals 100, ")
        self.info59 = ttk.Label(self.tab5, text="then the photomosaic will be 10x times (100 / 10) bigger than original photo.")
        self.info510 = ttk.Label(self.tab5, text="In addition to the mosaic generator, this program also has 2 image generators that can be used to make the tile folder.")
        self.info511 = ttk.Label(self.tab5, text="1. Single-Color Tile Generator that generates simple images with solid color.")
        self.info512 = ttk.Label(self.tab5, text="2. Lorem Picsum Generator that downloades images from \"Lorem Picsum\" webpage.")
        self.info513 = ttk.Label(self.tab5, text="If you want to use your own photos they must be renamed (prepared) by the Custom Image Preparator.")
        self.info514 = ttk.Label(self.tab5, text="You can mix pictures made by these 3 ways however you want in order to make unique tile folder.")
        self.info51.pack()
        self.info52.pack()
        self.info53.pack()
        self.info54.pack()
        self.info55.pack()
        self.info56.pack()
        self.info57.pack()
        self.info58.pack()
        self.info59.pack()
        self.info510.pack()
        self.info511.pack()
        self.info512.pack()
        self.info513.pack()
        self.info514.pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = MosaicApp(root)
    root.geometry("700x500")
    root.resizable(False, False)
    root.mainloop()