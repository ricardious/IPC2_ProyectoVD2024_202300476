import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

import cairosvg
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import (
    PhotoImage,
    Button,
    filedialog,
    messagebox,
    Frame,
    Canvas,
    Label,
    ttk,
    Scrollbar,
)
import xml.etree.ElementTree as ET
from utils.window_utils import center_window
from global_state import request_queue, artist_list, requester_list
from models.artist import Artist
from models.image import Image as CustomImage
from models.sparse_matrix import SparseMatrix
from views.login_view import LoginView


class ArtistView:
    def __init__(
        self, title="IPCArt - Artist", width=1000, height=700, artist_id: str = None
    ):
        # Dynamically set paths relative to the script location
        self.output_path = Path(__file__).parent
        self.assets_path = self.output_path / "../../assets" / "artist_assets"

        # Create the main window
        self.window = tk.Tk()

        self.artist_id = artist_id

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
        self.scroll_frame()

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
            command=self.logout,
            relief="flat",
            bg="#1D1D42",
            activebackground="#1D1D42",
        )
        self.button_1.place(x=804.0, y=23.0, width=171.0, height=44.0)

        # Additional buttons configuration
        buttons_config = [
            (self.button_image_2, 52.0, 152.0, "button_2", self.accept_request),
            (self.button_image_3, 52.0, 420.0, "button_3", self.view_queue),
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
            command=self.view_processed_images,
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
        self.canvas.delete("dynamic_text")  # Remove previous dynamic text

        if not request_queue.isEmpty():
            # Get the first request in the queue
            current_request = request_queue.peek()  # Assuming `peek` is implemented
            requester_text = f"Requester: {current_request.requester_id}"
            image_text = f"Image: {current_request.xml_path}"
        else:
            requester_text = "No requests available"
            image_text = ""

        text_configs = [
            (422.0, 143.0, requester_text),
            (422.0, 178.0, image_text),
        ]

        for x, y, text in text_configs:
            self.canvas.create_text(
                x,
                y,
                anchor="nw",
                text=text,
                fill="#FFFFFF",
                font=("Pixelify Sans", -20),
                tags="dynamic_text",
            )

    def scroll_frame(self):
        """Crear un frame con barras de desplazamiento"""
        # Adjust the position and size to fit between the specified images
        container_frame = Frame(self.window, bg="#4B0082", width=510, height=280)

        # Positioning the frame between image_4 (193.0, 186.0) and image_5 (411.0, 201.0)
        frame_id = self.canvas.create_window(
            678.0,  # Centered between image_4 and image_5
            500.0,  # Lowered to avoid overlapping with other images
            window=container_frame,
            width=520,
            height=290,
            anchor="center",
        )

        # Scrollbars personalizadas con ttk y estilo
        self.scrollbar_y = ttk.Scrollbar(
            container_frame, orient="vertical", style="Custom.Vertical.TScrollbar"
        )

        self.scrollable_frame = Canvas(
            container_frame,
            width=500,
            height=330,
            bg="#4B0082",
            yscrollcommand=self.scrollbar_y.set,
            highlightthickness=0,
        )
        self.scrollable_frame.pack(side="left", fill="both", expand=True)

        self.scrollbar_y.config(command=self.scrollable_frame.yview)

        self.inner_frame = Frame(self.scrollable_frame, bg="#4B0082")
        self.scrollable_frame.create_window(
            (0, 0), window=self.inner_frame, anchor="nw"
        )

        Label(
            self.inner_frame,
            text="No reports available",
            font=("Pixelify Sans", 24),
            bg="#4B0082",
            fg="white",
            anchor="center",
        ).pack(expand=True, fill="both", pady=130, padx=90)

        self.inner_frame.update_idletasks()
        self.scrollable_frame.config(scrollregion=self.scrollable_frame.bbox("all"))
        self.scrollable_frame.bind_all(
            "<MouseWheel>", self.on_mouse_wheel
        )  # Para Windows
        self.scrollable_frame.bind_all(
            "<Button-4>", self.on_mouse_wheel
        )  # Para Linux y MacOS
        self.scrollable_frame.bind_all(
            "<Button-5>", self.on_mouse_wheel
        )  # Para Linux y MacOS
        # Send the scrollable frame to the back
        self.canvas.tag_lower(frame_id)

    def show_report(self, svg_path):
        """Convertir un archivo SVG a PNG y mostrarlo en el centro del scrollable frame"""
        png_path = svg_path.replace(".svg", ".png")
        cairosvg.svg2png(url=svg_path, write_to=png_path)

        image = Image.open(png_path)

        # Escalar la imagen (2x o 3x más grande)
        scale_factor = 1
        image_width, image_height = image.size
        new_width = image_width * scale_factor
        new_height = image_height * scale_factor
        image = image.resize((new_width, new_height))

        self.displayed_image = ImageTk.PhotoImage(image)

        # Limpiar imagen previa
        self.scrollable_frame.delete("all")

        # Calcular el centro de la imagen dentro del scrollable frame
        canvas_width = self.scrollable_frame.winfo_width()
        canvas_height = self.scrollable_frame.winfo_height()

        x_center = max((canvas_width - new_width) // 2, 0)
        y_center = max((canvas_height - new_height) // 2, 0)

        # Crear imagen en el centro
        self.scrollable_frame.create_image(
            x_center, y_center, anchor="nw", image=self.displayed_image
        )

        # Actualizar el scrollregion para permitir el desplazamiento
        self.scrollable_frame.config(scrollregion=self.scrollable_frame.bbox("all"))
        self.check_scrollbar_visibility()

    def check_scrollbar_visibility(self):
        """Verifica si la región de desplazamiento excede el tamaño del marco y muestra la scrollbar si es necesario."""
        scrollable_region = self.scrollable_frame.bbox("all")  # Obtiene el área ocupada
        frame_height = self.scrollable_frame.winfo_height()

        if scrollable_region and scrollable_region[3] > frame_height:
            self.scrollbar_y.pack(side="right", fill="y")  # Muestra la scrollbar
        else:
            self.scrollbar_y.pack_forget()  # Oculta la scrollbar si no es necesaria

    def on_mouse_wheel(self, event):
        """Desplazar el contenido de scrollable_frame con la rueda del mouse"""
        if event.num == 4:  # Para sistemas Unix/Linux/MacOS
            self.scrollable_frame.yview_scroll(-1, "units")
        elif event.num == 5:  # Para sistemas Unix/Linux/MacOS
            self.scrollable_frame.yview_scroll(1, "units")
        else:  # Para Windows
            self.scrollable_frame.yview_scroll(-1 * (event.delta // 120), "units")

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

    def accept_request(self):
        """Accept the current request and process it."""
        try:
            if request_queue.isEmpty():
                messagebox.showinfo("Info", "No requests to accept")
                return

            # Dequeue the request
            current_request = request_queue.dequeue()

            # Add to processed images list
            artist_list.insert_processed(current_request.requester_id, current_request)

            figure_matrix = SparseMatrix()

            tree = ET.parse(current_request.xml_path)
            # Obtengo el elemento raiz
            root = tree.getroot()
            nombre_figura = ""
            for elemento in root:
                if elemento.tag == "diseño":
                    for pixel in elemento:
                        fila = int(pixel.attrib["fila"])
                        columna = int(pixel.attrib["col"])
                        color = pixel.text
                        figure_matrix.insert(fila, columna, color)
                elif elemento.tag == "nombre":
                    nombre_figura = elemento.text

                path = figure_matrix.plot(current_request.request_id)
                # creamos el nuevo objeto imagen para insertarlo a la lista doble del usuario
                new_image = CustomImage(current_request.request_id, nombre_figura, path)
                # insertamos el objeto a la lista doble del usuario
                requester_list.insert_user_image(
                    current_request.requester_id, new_image
                )

            messagebox.showinfo(
                "Success",
                f"Request {current_request.request_id} accepted and processed",
            )

            self.create_text()
        except Exception as e:
            messagebox.showerror("Error", f"Error accepting request: {str(e)}")

    def view_queue(self):
        """Display the current state of the request queue."""
        try:
            queue_path = "./Reportes/Cola.svg"
            request_queue.generate_graph()
            self.show_report(queue_path)
        except Exception as e:
            messagebox.showerror("Error", f"Error viewing queue: {str(e)}")

    def view_processed_images(self):
        """Display the circular list of processed images."""
        try:
            processed_path = f"./Reportes/Procesadas_{self.artist_id}.svg"
            artist = artist_list.search_by_id(self.artist_id)
            if not artist:
                raise ValueError(f"No artist found with ID: {self.artist_id}")

            if not hasattr(artist, "processed_images"):
                raise ValueError(
                    f"Artist {self.artist_id} has no processed images list"
                )

            artist.processed_images.generate_graph(
                filename=f"Procesadas_{self.artist_id}"
            )
            self.show_report(processed_path)
        except Exception as e:
            messagebox.showerror("Error", f"Error viewing processed images: {str(e)}")

    def on_button2_click(self):
        """Handler for button 2 click"""
        print("Button 2 clicked")

    def on_button3_click(self):
        """Handler for button 3 click"""
        print("Button 3 clicked")

    def on_button4_click(self):
        """Handler for button 4 click"""
        print("Button 4 clicked")

    def logout(self):
        """Logout the current user"""
        self.window.destroy()

        login = LoginView()
        login.run()

    def run(self):
        """Start the main application loop"""
        self.window.mainloop()


def main():
    """Main entry point of the application"""
    app = ArtistView()
    app.run()


if __name__ == "__main__":
    main()
