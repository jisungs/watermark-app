import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw, ImageFont


class WatermarkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("jisungs Watermark App")
        self.root.geometry("600x600")
        
        self.image = None
        self.tk_img = None

        self.create_widgets()

    def create_widgets(self):
         # Image Label for thumbnail
        self.img_label = tk.Label(self.root, bg='white')
        self.img_label.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

        # Open Image Button
        open_button = tk.Button(self.root, text="Open Image", command=self.open_image)
        open_button.grid(row=1, column=0, padx=10, pady=5, sticky="w")

         # Save Image Button
        save_button = tk.Button(self.root, text="Save Image", command=self.save_image)
        save_button.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # Watermark Text Entry
        self.watermark_entry = tk.Entry(self.root)
        self.watermark_entry.insert(0, "Watermark")
        self.watermark_entry.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        # Opacity Slider
        self.opacity_label = tk.Label(self.root, text="Opacity:")
        self.opacity_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.opacity_slider = tk.Scale(self.root, from_=0, to_=255, orient=tk.HORIZONTAL)
        self.opacity_slider.set(128)  # Default opacity
        self.opacity_slider.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

         # X Position Slider
        self.x_pos_label = tk.Label(self.root, text="X Position:")
        self.x_pos_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.x_pos_slider = tk.Scale(self.root, from_=0, to_=500, orient=tk.HORIZONTAL)
        self.x_pos_slider.set(10)  # Default X position
        self.x_pos_slider.grid(row=4, column=1, padx=10, pady=5, sticky="ew")

        # Y Position Slider
        self.y_pos_label = tk.Label(self.root, text="Y Position:")
        self.y_pos_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.y_pos_slider = tk.Scale(self.root, from_=0, to_=500, orient=tk.HORIZONTAL)
        self.y_pos_slider.set(10)  # Default Y position
        self.y_pos_slider.grid(row=5, column=1, padx=10, pady=5, sticky="ew")

        # Update Button
        update_button = tk.Button(self.root, text="Update Watermark", command=self.update_watermark)
        update_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="ew")


        # Configure column and row weights for resizing
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=0)
        self.root.grid_rowconfigure(2, weight=0)
        self.root.grid_rowconfigure(3, weight=0)
        self.root.grid_rowconfigure(4, weight=0)
        self.root.grid_rowconfigure(5, weight=0)
        self.root.grid_rowconfigure(6, weight=0)

        # # Open Image button
        # open_button = tk.Button(self.root, text="Open Image", command=self.open_image)
        # open_button.pack()

        # # Watermark Text Entry
        # self.watermark_entry = tk.Entry(self.root)
        # self.watermark_entry.insert(0, "Watermark")
        # self.watermark_entry.pack()

        # # Opacity Slider
        # self.opacity_label = tk.Label(self.root, text="Opacity:")
        # self.opacity_label.pack()
        # self.opacity_slider = tk.Scale(self.root, from_=0, to_=255, orient=tk.HORIZONTAL)
        # self.opacity_slider.set(128)  # Default opacity
        # self.opacity_slider.pack()

        # # X Position Slider
        # self.x_pos_label = tk.Label(self.root, text="X Position:")
        # self.x_pos_label.pack()
        # self.x_pos_slider = tk.Scale(self.root, from_=0, to_=500, orient=tk.HORIZONTAL)
        # self.x_pos_slider.set(10)  # Default X position
        # self.x_pos_slider.pack()

        # # Y Position Slider
        # self.y_pos_label = tk.Label(self.root, text="Y Position:")
        # self.y_pos_label.pack()
        # self.y_pos_slider = tk.Scale(self.root, from_=0, to_=500, orient=tk.HORIZONTAL)
        # self.y_pos_slider.set(10)  # Default Y position
        # self.y_pos_slider.pack()

        # # Update Button
        # update_button = tk.Button(self.root, text="Update Watermark", command=self.update_watermark)
        # update_button.pack()

        # # Save Image Button
        # save_button = tk.Button(self.root, text="Save Image", command=self.save_image)
        # save_button.pack()

        # # Image Label
        # self.img_label = tk.Label(self.root)
        # self.img_label.pack()

    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.image_path = file_path
            self.load_image()

    def load_image(self):
        img = Image.open(self.image_path)
        img.thumbnail((500, 500))  # Resize image for preview
        self.image = img
        self.update_watermark()

    def add_watermark(self, image, watermark_text, opacity, x_pos, y_pos):
        image = image.convert("RGBA")
        txt = Image.new('RGBA', image.size, (255, 255, 255, 0))
        
        try:
            font = ImageFont.truetype("arial.ttf", 36)  # Adjust the font and size as needed
        except IOError:
            font = ImageFont.load_default()

        draw = ImageDraw.Draw(txt)
        draw.text((x_pos, y_pos), watermark_text, font=font, fill=(0, 0, 0, opacity))
        
        watermarked = Image.alpha_composite(image, txt)
        return watermarked.convert("RGB")

    def update_watermark(self):
        if not self.image:
            return

        watermark_text = self.watermark_entry.get()
        opacity = self.opacity_slider.get()
        x_pos = self.x_pos_slider.get()
        y_pos = self.y_pos_slider.get()

        watermarked_image = self.add_watermark(self.image, watermark_text, opacity, x_pos, y_pos)
        self.tk_img = ImageTk.PhotoImage(watermarked_image)
        self.img_label.config(image=self.tk_img)
        self.img_label.image = self.tk_img

    def save_image(self):
        if self.image:
            save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                     filetypes=[("PNG files", "*.png"),
                                                                ("JPEG files", "*.jpg"),
                                                                ("All files", "*.*")])
            if save_path:
                watermark_text = self.watermark_entry.get()
                opacity = self.opacity_slider.get()
                x_pos = self.x_pos_slider.get()
                y_pos = self.y_pos_slider.get()

                watermarked_image = self.add_watermark(self.image, watermark_text, opacity, x_pos, y_pos)
                watermarked_image.save(save_path)

if __name__ == "__main__":
    root = tk.Tk()
    app = WatermarkApp(root)
    root.mainloop()