import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

import tkinter as tk
import cairosvg
from pathlib import Path
from tkinter import (
    filedialog,
    ttk,
    Frame,
    Canvas,
    Label,
    Scrollbar,
    PhotoImage,
    messagebox,
)
from PIL import Image, ImageTk

from utils.window_utils import center_window
from views.login_view import LoginView
from utils.xml_parser import XMLParser
from models.image_queue_request import ImageQueueRequest
from global_state import request_queue, requester_list


class RequesterView:
    def __init__(
        self,
        window_width: int = 1000,
        window_height: int = 700,
        user_id: str = None,
        pwd: str = None,
    ):
        self.window = tk.Tk()

        center_window(self.window, window_width, window_height)
        self.window.configure(bg="#141432")
        self.window.resizable(False, False)

        self.user_id = user_id
        self.pwd = pwd

        print(self.user_id)

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
        self.scroll_frame()

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
            bg="#1D1D42",
            activebackground="#1D1D42",
        )
        top_button.place(x=804.0, y=23.0, width=171.0, height=44.0)
        # Keep a reference to prevent garbage collection
        self._top_button_image = top_button_image

    def create_buttons(self):
        """Create all buttons in the application."""
        button_configs = [
            ("button_2.png", 78.0, 143.0, 240.0, 45.0, self.load_figure_from_xml),
            ("button_3.png", 78.0, 250.0, 240.0, 45.0, self.process_requests),
            ("button_4.png", 78.0, 471.0, 240.0, 45.0, self.view_stack),
            ("button_5.png", 78.0, 563.0, 240.0, 45.0, self.view_circular_double_list),
            ("button_6.png", 380.0, 635.0, 240.0, 45.0, self.open_gallery),
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
                bg="#141432",
                activebackground="#141432",
            )
            button.place(x=x, y=y, width=width, height=height)
            self._button_images.append(button_image)

    def create_images(self):
        """Create images in the application."""
        image_configs = [
            ("image_2.png", 672.0, 171.0),
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

    def scroll_frame(self):
        container_frame = Frame(self.window, bg="#4B0082", width=510, height=290)

        frame_id = self.canvas.create_window(
            670.0,
            390.0,
            window=container_frame,
            width=520,
            height=300,
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
        ).pack(expand=True, fill="both", pady=120, padx=95)

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

    def log_out(self):
        self.window.destroy()  # Close current window

        login = LoginView()  # Create new login window
        login.run()  # Start login window mainloop

    def load_figure_from_xml(self):
        try:
            file_path = filedialog.askopenfilename(
                title="Select XML File",
                filetypes=[("XML Files", "*.xml"), ("All Files", "*.*")],
            )

            if file_path:
                # Call XMLParser to load figures from the XML file
                XMLParser.load_figures(file_path, self.user_id)
                print(f"Figures successfully loaded from: {file_path}")
            else:
                print("No file was selected.")
        except Exception as e:
            print(f"An error occurred while loading the XML file: {e}")

    def process_requests(self):
        try:
            processed_count = 0

            while True:
                # Solo hacemos pop una vez por iteración
                value_from_stack = requester_list.pop_from_user_stack(self.user_id)
                print(f"Processing request from stack: {value_from_stack}")

                if value_from_stack is None:
                    print(f"No more requests found for user {self.user_id}")
                    break

                try:
                    # Crear y encolar el nuevo request
                    new_request = ImageQueueRequest(
                        request_id=value_from_stack.request_id,
                        xml_path=value_from_stack.xml_path,
                        requester_id=self.user_id,
                    )

                    request_queue.enqueue(new_request)
                    processed_count += 1
                    print(f"Successfully enqueued request {new_request.request_id}")

                except AttributeError as e:
                    print(f"Error accessing request attributes: {e}")
                    print(f"Value from stack: {type(value_from_stack)}")
                    break

            print(
                f"Successfully processed {processed_count} requests for user {self.user_id}"
            )

            if processed_count > 0:
                messagebox.showinfo(
                    "Success", f"Successfully processed {processed_count} requests"
                )
            else:
                messagebox.showinfo("Info", "No requests found to process")

        except Exception as e:
            print(f"Error processing requests: {e}")
            messagebox.showerror(
                "Error", f"An error occurred while processing requests: {str(e)}"
            )

    def view_stack(self):
        try:
            # 1️⃣ Buscar el solicitante logueado por su ID
            current_requester = requester_list.search(self.user_id, self.pwd)

            if current_requester is None:
                messagebox.showerror(
                    "Error", f"No se encontró el solicitante con ID {self.user_id}"
                )
                return

            # 2️⃣ Graficar la pila personalizada de este solicitante
            current_requester.cart_stack.graph(filename=f"Pila_{self.user_id}")

            # 3️⃣ Mostrar el reporte en la interfaz gráfica
            report_path = f"./Reportes/Pila_{self.user_id}.svg"
            self.show_report(report_path)

            # 4️⃣ Mostrar mensaje de éxito
            messagebox.showinfo(
                "Reporte generado", "El reporte de la pila ha sido generado."
            )

        except Exception as e:
            print(f"Error al ver la pila: {e}")

    def view_circular_double_list(self):
        try:
            # 1️⃣ Buscar el solicitante logueado por su ID
            current_requester = requester_list.search(self.user_id, self.pwd)

            if current_requester is None:
                messagebox.showerror(
                    "Error", f"No se encontró el solicitante con ID {self.user_id}"
                )
                return

            # 2️⃣ Graficar la pila personalizada de este solicitante
            current_requester.image_gallery.generate_graph(
                filename=f"Lista_Doble_{self.user_id}"
            )

            # 3️⃣ Mostrar el reporte en la interfaz gráfica
            report_path = f"./Reportes/Lista_Doble{self.user_id}.svg"
            self.show_report(report_path)

            # 4️⃣ Mostrar mensaje de éxito
            messagebox.showinfo(
                "Reporte generado",
                "El reporte de la lista doble circular ha sido generado.",
            )

        except Exception as e:
            print(f"Error al ver la pila: {e}")

    def open_gallery(self):
        from views.gallery_view import GalleryView

        self.window.destroy()  # Close current window
        gallery = GalleryView()
        gallery.run()

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
