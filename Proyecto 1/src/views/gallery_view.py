from pathlib import Path
import sys
import os
from tkinter import Tk, Canvas, Button, PhotoImage, messagebox

# Add project root to Python path
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

from utils.window_utils import center_window
from global_state import requester_list


class GalleryView:
    def __init__(self):
        self.window = Tk()
        self.window_width = 1000
        self.window_height = 700
        center_window(self.window, self.window_width, self.window_height)
        self.window.configure(bg="#141432")
        self.window.resizable(False, False)

        # Configurar rutas
        self.OUTPUT_PATH = Path(__file__).parent
        self.ASSETS_PATH = self.OUTPUT_PATH / "../../assets" / "gallery_assets"

        # Crear canvas
        self.canvas = Canvas(
            self.window,
            bg="#141432",
            height=700,
            width=1000,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )
        self.canvas.place(x=0, y=0)

        # Dibujar elementos
        self.create_rectangle()
        self.load_images()
        self.create_buttons()

    def relative_to_assets(self, path: str) -> Path:
        return self.ASSETS_PATH / Path(path)

    def create_rectangle(self):
        self.canvas.create_rectangle(0.0, 0.0, 1000.0, 90.0, fill="#1D1D42", outline="")

    def button_1_clicked(self):
        print("button_1 clicked")

    def button_2_clicked(self):
        print("button_2 clicked")

    def button_3_clicked(self):
        print("button_3 clicked")

    def ver(self):

        current_requester = requester_list.search(self.user_id, self.pwd)

        if current_requester is None:
            messagebox.showerror(
                "Error", f"No se encontró el solicitante con ID {self.user_id}"
            )
            return

        image = current_requester.image_gallery()
        current_requester.image_gallery.get_prev()

    def close_gallery(self):
        from views.requester_view import RequesterView

        self.window.destroy()
        requester = RequesterView()
        requester.run()

    def load_images(self):
        # Cargar imágenes
        self.button_image_1 = PhotoImage(file=self.relative_to_assets("button_1.png"))
        self.button_image_2 = PhotoImage(file=self.relative_to_assets("button_2.png"))
        self.button_image_3 = PhotoImage(file=self.relative_to_assets("button_3.png"))

        # Cargar y crear imágenes en el canvas
        for i in range(1, 8):
            image_path = f"image_{i}.png"
            setattr(
                self, f"image_{i}", PhotoImage(file=self.relative_to_assets(image_path))
            )

        # Posicionar imágenes en el canvas
        positions = {
            1: (190.0, 45.0),
            2: (499.0, 136.0),
            3: (499.0, 448.0),
            4: (188.0, 255.0),
            5: (810.0, 255.0),
            6: (188.0, 640.0),
            7: (810.0, 640.0),
        }

        for num, pos in positions.items():
            self.canvas.create_image(
                pos[0], pos[1], image=getattr(self, f"image_{num}")
            )

    def create_buttons(self):
        # Botón 1
        self.button_1 = Button(
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.close_gallery,
            relief="flat",
            background="#1D1D42",
            activebackground="#1D1D42",
        )
        self.button_1.place(x=804.0, y=23.0, width=171.0, height=44.0)

        # Botón 2
        self.button_2 = Button(
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=self.button_2_clicked,
            relief="flat",
            background="#141432",
            activebackground="#141432",
        )
        self.button_2.place(x=233.0, y=182.0, width=240.0, height=45.0)

        # Botón 3
        self.button_3 = Button(
            image=self.button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=self.button_3_clicked,
            relief="flat",
            background="#141432",
            activebackground="#141432",
        )
        self.button_3.place(x=527.0, y=182.0, width=240.0, height=45.0)

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = GalleryView()
    app.run()
