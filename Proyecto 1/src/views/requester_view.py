import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

import tkinter as tk
from pathlib import Path


from utils.window_utils import center_window
from views.login_view import LoginView


class RequesterView:
    def __init__(self, window_width: int = 1000, window_height: int = 700):
        self.window = tk.Tk()

        center_window(self.window, window_width, window_height)
        self.window.configure(bg="#141432")
        self.window.resizable(False, False)

        # Set up paths
        self.output_path = Path(__file__).parent
        self.assets_path = self.output_path / "../../assets" / "requester_assets"

        # Create canvas
        self.canvas = tk.Canvas(
            self.window,
            bg="#141432",
            height=window_height,
            width=window_width,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )
        self.canvas.place(x=0, y=0)

        # Create UI elements
        self.create_top_bar()
        self.create_buttons()
        self.create_images()

    def relative_to_assets(self, path: str) -> Path:
        """Convert relative path to absolute path for assets."""
        return self.assets_path / Path(path)

    def create_top_bar(self):
        """Create the top bar rectangle and header elements."""
        # Top bar background
        self.canvas.create_rectangle(0.0, 0.0, 1000.0, 90.0, fill="#1D1D42", outline="")

        # Header image
        header_image = tk.PhotoImage(file=self.relative_to_assets("image_1.png"))
        self.canvas.create_image(190.0, 45.0, image=header_image)
        # Keep a reference to prevent garbage collection
        self._header_image = header_image

        # Top right button
        top_button_image = tk.PhotoImage(file=self.relative_to_assets("button_1.png"))
        top_button = tk.Button(
            image=top_button_image,
            borderwidth=0,
            highlightthickness=0,
            command=self.log_out,
            relief="flat",
        )
        top_button.place(x=804.0, y=23.0, width=171.0, height=44.0)
        # Keep a reference to prevent garbage collection
        self._top_button_image = top_button_image

    def create_buttons(self):
        """Create all buttons in the application."""
        button_configs = [
            ("button_2.png", 78.0, 143.0, 240.0, 45.0, self.on_button2_click),
            ("button_3.png", 78.0, 250.0, 240.0, 45.0, self.on_button3_click),
            ("button_4.png", 78.0, 471.0, 240.0, 45.0, self.on_button4_click),
            ("button_5.png", 78.0, 563.0, 240.0, 45.0, self.on_button5_click),
            ("button_6.png", 380.0, 635.0, 240.0, 45.0, self.on_button6_click),
        ]

        self._button_images = []  # To prevent garbage collection
        for button_file, x, y, width, height, command in button_configs:
            button_image = tk.PhotoImage(file=self.relative_to_assets(button_file))
            button = tk.Button(
                image=button_image,
                borderwidth=0,
                highlightthickness=0,
                command=command,
                relief="flat",
            )
            button.place(x=x, y=y, width=width, height=height)
            self._button_images.append(button_image)

    def create_images(self):
        """Create images in the application."""
        image_configs = [
            ("image_2.png", 672.0, 171.0),
            ("image_3.png", 670.0, 390.0),
            ("image_4.png", 390.0, 221.0),
            ("image_5.png", 955.0, 221.0),
            ("image_6.png", 390.0, 557.0),
            ("image_7.png", 948.0, 557.0),
            ("image_8.png", 197.0, 382.0),
        ]

        self._images = []  # To prevent garbage collection
        for image_file, x, y in image_configs:
            image = tk.PhotoImage(file=self.relative_to_assets(image_file))
            canvas_image = self.canvas.create_image(x, y, image=image)
            self._images.append(image)

    def log_out(self):
        self.window.destroy()  # Close current window

        login = LoginView()  # Create new login window
        login.run()  # Start login window mainloop

    def on_button2_click(self):
        """Handler for button 2 click event."""
        print("button_2 clicked")

    def on_button3_click(self):
        """Handler for button 3 click event."""
        print("button_3 clicked")

    def on_button4_click(self):
        """Handler for button 4 click event."""
        print("button_4 clicked")

    def on_button5_click(self):
        """Handler for button 5 click event."""
        print("button_5 clicked")

    def on_button6_click(self):
        """Handler for button 6 click event."""
        print("button_6 clicked")

    def run(self):
        """Start the Tkinter event loop."""
        self.window.mainloop()


# Example usage
if __name__ == "__main__":
    app = RequesterView()
    app.run()
