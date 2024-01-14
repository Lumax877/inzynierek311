import tkinter as tk
from tkinter import filedialog
from PIL import Image
from finalscript import create_mosaic

class MosaicApp:
    def __init__(self, master):
        self.master = master
        master.title("Mosaic Generator")

        self.input_image_path = tk.StringVar()
        self.tile_directory = tk.StringVar()
        self.output_image_path = tk.StringVar()
        self.tile_size = tk.StringVar()
        self.target_region_size = tk.StringVar()
        self.create_widgets()

    def create_widgets(self):

        self.input_button = tk.Button(self.master, text="Select Input Image", command=self.select_input_image)
        self.input_button.pack()

        self.tile_button = tk.Button(self.master, text="Select Tile Directory", command=self.select_tile_directory)
        self.tile_button.pack()

        self.output_button = tk.Button(self.master, text="Select Output Image Path", command=self.select_output_image)
        self.output_button.pack()

        tk.Label(self.master, text="Tile Size:").pack()
        self.tile_size_entry = tk.Entry(self.master, textvariable=self.tile_size)
        self.tile_size_entry.pack()

        tk.Label(self.master, text="Target Region Size:").pack()
        self.target_region_size_entry = tk.Entry(self.master, textvariable=self.target_region_size)
        self.target_region_size_entry.pack()

        self.run_button = tk.Button(self.master, text="Generate Mosaic", command=self.generate_mosaic)
        self.run_button.pack()

    def select_input_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        self.input_image_path.set(file_path)

    def select_tile_directory(self):
        dir_path = filedialog.askdirectory()
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

        if input_path and tile_dir and output_path:
            create_mosaic(input_path, output_path, tile_dir, tile_size=(tile_size, tile_size), region_size=target_region_size)
            print("Mosaic generated successfully!")
        else:
            print("Please select input image, tile directory, and output image path.")

if __name__ == "__main__":
    root = tk.Tk()
    app = MosaicApp(root)
    root.mainloop()
