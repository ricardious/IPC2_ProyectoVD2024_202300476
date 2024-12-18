import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

import tkinter as tk
from tkinter import PhotoImage, Button, filedialog, messagebox
from utils.window_utils import center_window


class ArtistView:
    def __init__(self, title="IPCArt - Artist", width=1000, height=700):
        # Dynamically set paths relative to the script location
        self.output_path = Path(__file__).parent
        self.assets_path = self.output_path / "../../assets" / "artist_assets"

        # Create the main window
        self.window = tk.Tk()

        center_window(self.window, width, height)

        self.window.configure(bg="#141432")
        self.window.resizable(False, False)

        # Create canvas
        self.canvas = tk.Canvas(
            self.window,
            bg="#141432",
            height=height,
            width=width,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )
        self.canvas.place(x=0, y=0)

        # Set up the UI
        self.canvas.create_rectangle(0.0, 0.0, width, 90.0, fill="#1D1D42", outline="")
        self.load_images()
        self.create_buttons()
        self.create_images()
        self.create_text()

    def relative_to_assets(self, path: str) -> Path:
        """Convert relative path to full asset path"""
        return self.assets_path / Path(path)

    def load_images(self):
        """Load all images"""
        # Button images
        self.button_image_1 = tk.PhotoImage(
            file=self.relative_to_assets("button_1.png")
        )
        self.button_image_2 = tk.PhotoImage(
            file=self.relative_to_assets("button_2.png")
        )
        self.button_image_3 = tk.PhotoImage(
            file=self.relative_to_assets("button_3.png")
        )
        self.button_image_4 = tk.PhotoImage(
            file=self.relative_to_assets("button_4.png")
        )

        # Canvas images
        self.image_1 = tk.PhotoImage(file=self.relative_to_assets("image_1.png"))
        self.image_2 = tk.PhotoImage(file=self.relative_to_assets("image_2.png"))
        self.image_3 = tk.PhotoImage(file=self.relative_to_assets("image_3.png"))
        self.image_4 = tk.PhotoImage(file=self.relative_to_assets("image_4.png"))
        self.image_5 = tk.PhotoImage(file=self.relative_to_assets("image_5.png"))
        self.image_6 = tk.PhotoImage(file=self.relative_to_assets("image_6.png"))
        self.image_7 = tk.PhotoImage(file=self.relative_to_assets("image_7.png"))
        self.image_8 = tk.PhotoImage(file=self.relative_to_assets("image_8.png"))
        self.image_9 = tk.PhotoImage(file=self.relative_to_assets("image_9.png"))

    def create_buttons(self):
        """Create all buttons"""
        # First button with custom styling
        self.button_1 = tk.Button(
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.upload_image,
            relief="flat",
            bg="#1D1D42",
            activebackground="#1D1D42",
        )
        self.button_1.place(x=804.0, y=23.0, width=171.0, height=44.0)

        # Additional buttons configuration
        buttons_config = [
            (self.button_image_2, 52.0, 152.0, "button_2", self.on_button2_click),
            (self.button_image_3, 52.0, 420.0, "button_3", self.on_button3_click),
        ]

        for image, x, y, name, command in buttons_config:
            button = tk.Button(
                image=image,
                borderwidth=0,
                highlightthickness=0,
                command=command,
                relief="flat",
                bg="#141432",
                activebackground="#141432",
            )
            button.place(x=x, y=y, width=240.0, height=45.0)

        self.button_4 = Button(
            image=self.button_image_4,
            borderwidth=0,
            highlightthickness=0,
            command=self.on_button4_click,
            relief="flat",
            bg="#141432",
            activebackground="#141432",
        )
        self.button_4.place(x=52.0, y=527.0, width=240.0, height=70.0)

    def create_images(self):
        """Create all images in the canvas"""
        image_positions = [
            (self.image_1, 190.0, 45.0),
            (self.image_2, 678.0, 286.0),
            (self.image_3, 679.0, 499.0),
            (self.image_4, 179.0, 285.0),
            (self.image_5, 395.0, 338.0),
            (self.image_6, 960.0, 338.0),
            (self.image_7, 395.0, 656.0),
            (self.image_8, 960.0, 656.0),
            (self.image_9, 682.0, 174.0),
        ]

        for image, x, y in image_positions:
            self.canvas.create_image(x, y, image=image)

    def create_text(self):
        """Create text elements"""
        text_configs = [
            (422.0, 143.0, "Requester: IPC-001"),
            (422.0, 178.0, "Image: Ricardious"),
        ]

        for x, y, text in text_configs:
            self.canvas.create_text(
                x,
                y,
                anchor="nw",
                text=text,
                fill="#FFFFFF",
                font=("Pixelify Sans", -20),
            )

    def upload_image(self):
        """Handle image upload"""
        file_path = filedialog.askopenfilename(
            title="Select Image File",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"),
                ("All files", "*.*"),
            ],
        )

        if file_path:
            messagebox.showinfo("Upload", f"Image uploaded: {file_path}")
            # Add your image upload logic here

    def on_button2_click(self):
        """Handler for button 2 click"""
        print("Button 2 clicked")

    def on_button3_click(self):
        """Handler for button 3 click"""
        print("Button 3 clicked")

    def on_button4_click(self):
        """Handler for button 4 click"""
        print("Button 4 clicked")

    def run(self):
        """Start the main application loop"""
        self.window.mainloop()


def main():
    """Main entry point of the application"""
    app = ArtistView()
    app.run()


if __name__ == "__main__":
    main()
