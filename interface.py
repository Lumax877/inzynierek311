import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image
from finalscript import create_mosaic
import os
from img_generation import generate_images, check
from lorempicsum import lorem_images

class MosaicApp:
    def __init__(self, master):
        self.master = master
        master.title("Mosaic Generator")

        self.tabControl = ttk.Notebook(master)
        self.tab1 = ttk.Frame(self.tabControl)
        self.tab2 = ttk.Frame(self.tabControl)
        self.tab3 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab1, text="Mosaic Generator")
        self.tabControl.add(self.tab2, text="Single-Color Tile Generator")
        self.tabControl.add(self.tab3, text="Lorem Picsum Pictures Generator")
        self.tabControl.pack(expand=1, fill="both")

        self.setup_mosaic_tab()

        self.setup_image_tab()

        self.setup_lorem_tab()

    def setup_mosaic_tab(self):
        self.input_image_path = tk.StringVar()
        self.tile_directory = tk.StringVar()
        self.output_image_path = tk.StringVar()
        self.tile_size = tk.StringVar()
        self.target_region_size = tk.StringVar()

        self.input_path_label = ttk.Label(self.tab1, text="Input Image Path:")
        self.input_path_label.pack(pady=1)

        self.input_path_scrollbar = ttk.Scrollbar(self.tab1, orient="horizontal")
        self.input_path_entry = ttk.Entry(self.tab1, textvariable=self.input_image_path, xscrollcommand=self.input_path_scrollbar.set)
        self.input_path_scrollbar.config(command=self.input_path_entry.xview)

        self.input_path_entry.pack(pady=1, fill="x")
        self.input_path_scrollbar.pack(fill="x")

        self.input_button = tk.Button(self.tab1, text="Select Input Image", command=self.select_input_image)
        self.input_button.pack()

        self.input_file_label = ttk.Label(self.tab1, text="Tile Directory Path:")
        self.input_file_label.pack(pady=1)

        self.tile_path_scrollbar = ttk.Scrollbar(self.tab1, orient="horizontal")
        self.tile_path_entry = ttk.Entry(self.tab1, textvariable=self.tile_directory, xscrollcommand=self.tile_path_scrollbar.set)
        self.tile_path_scrollbar.config(command=self.tile_path_entry.xview)

        self.tile_path_entry.pack(pady=1, fill="x")
        self.tile_path_scrollbar.pack(fill="x")

        self.tile_button = tk.Button(self.tab1, text="Select Tile Directory", command=self.select_tile_directory)
        self.tile_button.pack()

        self.output_file_label = ttk.Label(self.tab1, text="Output Image Path:")
        self.output_file_label.pack(pady=1)

        self.output_path_scrollbar = ttk.Scrollbar(self.tab1, orient="horizontal")
        self.output_path_entry = ttk.Entry(self.tab1, textvariable=self.output_image_path, xscrollcommand=self.output_path_scrollbar.set)
        self.output_path_scrollbar.config(command=self.output_path_entry.xview)

        self.output_path_entry.pack(pady=1, fill="x")
        self.output_path_scrollbar.pack(fill="x")

        self.output_button = tk.Button(self.tab1, text="Select Output Image Path", command=self.select_output_image)
        self.output_button.pack()

        tk.Label(self.tab1, text="Tile Size:").pack()
        self.tile_size_entry = tk.Entry(self.tab1, textvariable=self.tile_size)
        self.tile_size_entry.pack()

        tk.Label(self.tab1, text="Target Region Size:").pack()
        self.target_region_size_entry = tk.Entry(self.tab1, textvariable=self.target_region_size)
        self.target_region_size_entry.pack()

        self.run_button = tk.Button(self.tab1, text="Generate Mosaic", command=self.generate_mosaic)
        self.run_button.pack()

        self.info = ttk.Label(self.tab1, text="Please use buttons instead of textboxes to select required files.")
        self.info.pack(pady=1)

        self.info2 = ttk.Label(self.tab1, text="Remember that tile directory must contain ONLY square images with same resolution.")
        self.info2.pack(pady=1)

    def select_input_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if file_path and not self.is_valid_image(file_path):
            print("Invalid input file. Please select a valid image.")
            return
        self.input_image_path.set(file_path)

    def select_tile_directory(self):
        dir_path = filedialog.askdirectory()
        if dir_path and not self.contains_valid_images(dir_path):
            print("Invalid tile directory. Please select a directory containing valid image files.")
            return
        self.tile_directory.set(dir_path)

    def select_output_image(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg")])
        self.output_image_path.set(file_path)

    def generate_mosaic(self):
        input_path = self.input_image_path.get()
        tile_dir = self.tile_directory.get()
        output_path = self.output_image_path.get()

        try:
            tile_size = int(self.tile_size.get())
            target_region_size = int(self.target_region_size.get())
        except ValueError:
            print("Invalid input for Tile Size or Target Region Size. Please enter valid integers.")
            return

        if not input_path or not tile_dir or not output_path:
            print("Please select input image, tile directory, and output image path.")
            return

        if not self.is_valid_image(input_path):
            print("Invalid input file. Please select a valid image.")
            return

        if not self.contains_valid_images(tile_dir):
            print("Invalid tile directory. Please select a directory containing valid image files.")
            return

        create_mosaic(input_path, output_path, tile_dir, tile_size=(tile_size, tile_size), region_size=target_region_size)
        print("Mosaic generated successfully!")

    def setup_image_tab(self):
        self.num_generated_images = tk.StringVar()
        self.generated_image_size = tk.StringVar()
        self.generated_images_path = tk.StringVar()

        tk.Label(self.tab2, text="Number of Generated Images:").pack()
        self.num_generated_images_entry = tk.Entry(self.tab2, textvariable=self.num_generated_images)
        self.num_generated_images_entry.pack()

        tk.Label(self.tab2, text="Generated Image Size (square):").pack()
        self.generated_image_size_entry = tk.Entry(self.tab2, textvariable=self.generated_image_size)
        self.generated_image_size_entry.pack()

        self.folder_path_label = ttk.Label(self.tab2, text="Tile Folder Path:")
        self.folder_path_label.pack(pady=1)

        self.folder_path_scrollbar = ttk.Scrollbar(self.tab2, orient="horizontal")
        self.folder_path_entry = ttk.Entry(self.tab2, textvariable=self.generated_images_path, xscrollcommand=self.folder_path_scrollbar.set)
        self.folder_path_scrollbar.config(command=self.folder_path_entry.xview)

        self.folder_path_entry.pack(pady=1, fill="x")
        self.folder_path_scrollbar.pack(fill="x")

        self.generated_images_path_button = tk.Button(self.tab2, text="Select Folder", command=self.select_generated_images_path)
        self.generated_images_path_button.pack()

        self.generate_images_button = tk.Button(self.tab2, text="Generate Images", command=self.generate_images)
        self.generate_images_button.pack()

        self.info = ttk.Label(self.tab2, text="Warning: all files in the selected folder will be deleted when generating starts.")
        self.info.pack(pady=1)

    def select_generated_images_path(self):
        folder_path = filedialog.askdirectory()
        self.generated_images_path.set(folder_path)

    def generate_images(self):
        picpath = self.generated_images_path.get()
        try:
            num_images = int(self.num_generated_images.get())
            image_size = int(self.generated_image_size.get())
        except ValueError:
            print("Invalid input for Number of Generated Images or Generated Image Size. Please enter valid integers.")
            return

        check(picpath)
        generate_images(num_images, (image_size, image_size), picpath)
        print(f"{num_images} images generated successfully!")

    def is_valid_image(self, file_path):
        try:
            img = Image.open(file_path)
            img.close()
            return True
        except (IOError, SyntaxError):
            return False

    def contains_valid_images(self, dir_path):
        if not os.path.exists(dir_path):
            return False

        for filename in os.listdir(dir_path):
            file_path = os.path.join(dir_path, filename)
            if os.path.isfile(file_path) and not self.is_valid_image(file_path):
                return False

        return True

    def setup_lorem_tab(self):
        self.num_lorem_images = tk.StringVar()
        self.lorem_image_size = tk.StringVar()
        self.lorem_images_path = tk.StringVar()

        tk.Label(self.tab3, text="Number of Downloaded Images:").pack()
        self.num_lorem_images_entry = tk.Entry(self.tab3, textvariable=self.num_lorem_images)
        self.num_lorem_images_entry.pack()

        tk.Label(self.tab3, text="Downloaded Image Size (square):").pack()
        self.lorem_image_size_entry = tk.Entry(self.tab3, textvariable=self.lorem_image_size)
        self.lorem_image_size_entry.pack()

        self.lorem_path_label = ttk.Label(self.tab3, text="Tile Folder Path:")
        self.lorem_path_label.pack(pady=1)

        self.lorem_path_scrollbar = ttk.Scrollbar(self.tab3, orient="horizontal")
        self.lorem_path_entry = ttk.Entry(self.tab3, textvariable=self.lorem_images_path, xscrollcommand=self.lorem_path_scrollbar.set)
        self.lorem_path_scrollbar.config(command=self.lorem_path_entry.xview)

        self.lorem_path_entry.pack(pady=1, fill="x")
        self.lorem_path_scrollbar.pack(fill="x")

        self.lorem_images_path_button = tk.Button(self.tab3, text="Select Folder", command=self.select_lorem_images_path)
        self.lorem_images_path_button.pack()

        self.lorem_images_button = tk.Button(self.tab3, text="Download Images", command=self.lorem_images)
        self.lorem_images_button.pack()

        self.info = ttk.Label(self.tab3, text="Warning: all files in the selected folder will be deleted when downloading starts.")
        self.info.pack(pady=1)

    def select_lorem_images_path(self):
        folder_path = filedialog.askdirectory()
        self.lorem_images_path.set(folder_path)

    def lorem_images(self):
        picpath = self.lorem_images_path.get()
        try:
            num_images = int(self.num_lorem_images.get())
            image_size = int(self.lorem_image_size.get())
        except ValueError:
            print("Invalid input for Number of Generated Images or Generated Image Size. Please enter valid integers.")
            return

        check(picpath)
        lorem_images(num_images, (image_size, image_size), picpath)
        print(f"{num_images} images generated successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = MosaicApp(root)
    root.geometry("500x500")
    root.resizable(False, False)
    root.mainloop()