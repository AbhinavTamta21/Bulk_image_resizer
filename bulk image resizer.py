import tkinter as tk
from tkinter import filedialog, messagebox
import os
import cv2

class ImageConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Converter")

        # Variables
        self.input_folder = tk.StringVar()
        self.output_folder = tk.StringVar()
        self.width = tk.StringVar()
        self.height = tk.StringVar()
        self.maintain_aspect_ratio = tk.BooleanVar()

        # Create widgets
        self.create_widgets()

    def create_widgets(self):
        # Input folder selection
        tk.Label(self.root, text="Select input folder:").grid(row=0, column=0, sticky="w")
        tk.Entry(self.root, textvariable=self.input_folder, width=40).grid(row=0, column=1, padx=5)
        tk.Button(self.root, text="Browse", command=self.browse_input_folder).grid(row=0, column=2)

        # Output folder selection
        tk.Label(self.root, text="Select output folder:").grid(row=1, column=0, sticky="w")
        tk.Entry(self.root, textvariable=self.output_folder, width=40).grid(row=1, column=1, padx=5)
        tk.Button(self.root, text="Browse", command=self.browse_output_folder).grid(row=1, column=2)

        # Image size entry
        tk.Label(self.root, text="Image size (Width x Height):").grid(row=2, column=0, sticky="w")
        tk.Entry(self.root, textvariable=self.width, width=10).grid(row=2, column=1, padx=5)
        tk.Entry(self.root, textvariable=self.height, width=10).grid(row=2, column=2, padx=5)

        # Maintain aspect ratio checkbox
        tk.Checkbutton(self.root, text="Maintain Aspect Ratio", variable=self.maintain_aspect_ratio).grid(row=3, column=0, columnspan=3, pady=5)

        # Convert button
        tk.Button(self.root, text="Convert Images", command=self.convert_images).grid(row=4, column=1, pady=10)

    def browse_input_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.input_folder.set(folder)

    def browse_output_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_folder.set(folder)

    def calculate_width_and_height(self, img_width, img_height):
        aspect_ratio = img_width / img_height

        if self.maintain_aspect_ratio.get():
            if self.width.get() and not self.height.get():
                self.height.set(int(int(self.width.get()) / aspect_ratio))
            elif not self.width.get() and self.height.get():
                self.width.set(int(int(self.height.get()) * aspect_ratio))

    def convert_images(self):
        input_folder = self.input_folder.get()
        output_folder = self.output_folder.get()

        if not os.path.isdir(input_folder):
            messagebox.showerror("Error", "Input folder does not exist.")
            return

        if not os.path.isdir(output_folder):
            os.makedirs(output_folder)

        for filename in os.listdir(input_folder):
            if filename.endswith((".jpg", ".jpeg", ".png", ".bmp")):
                image_path = os.path.join(input_folder, filename)
                img = cv2.imread(image_path)
                if img is not None:
                    img_height, img_width, _ = img.shape
                    self.calculate_width_and_height(img_width, img_height)

                    try:
                        width = int(self.width.get())
                        height = int(self.height.get())
                    except ValueError:
                        messagebox.showerror("Error", "Invalid width or height.")
                        return

                    resized_img = cv2.resize(img, (width, height))
                    output_path = os.path.join(output_folder, filename)
                    cv2.imwrite(output_path, resized_img)
        messagebox.showinfo("Conversion", "Conversion complete.")

def main():
    root = tk.Tk()
    app = ImageConverterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()