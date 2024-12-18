import sys
import os
from pathlib import Path
from tkinter import (
    Tk,
    Canvas,
    Entry,
    Text,
    Button,
    PhotoImage,
    filedialog,
    messagebox,
    Frame,
    Scrollbar,
    Label,
    ttk,
)
from PIL import Image, ImageTk
from global_state import artist_list, requester_list
import cairosvg

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.window_utils import center_window
from utils.xml_parser import XMLParser
from utils.graphviz_reports import GraphvizReports
from views.login_view import LoginView


class AdminView:
    def __init__(self, title="IPCArt - Admin", width=1000, height=700):
        # Configurar ruta de activos de forma relativa al directorio del script
        self.output_path = Path(__file__).parent
        self.assets_path = self.output_path / "../../assets" / "admin_assets"

        # Configurar ventana principal
        self.window = Tk()
        self.window.title(title)

        center_window(self.window, width, height)

        self.window.configure(bg="#141432")
        self.window.resizable(False, False)

        # Estilo para los Scrollbars usando ttk.Style
        self.style = ttk.Style(self.window)
        self.style.theme_use("clam")
        self.style.configure(
            "Custom.Vertical.TScrollbar",
            background="#6A0DAD",  # Fondo de la barra (morado oscuro)
            troughcolor="#4B0082",  # Color de la ranura (índigo profundo)
            arrowcolor="#D8BFD8",  # Color de las flechas (morado claro)
            bordercolor="#8A2BE2",  # Color del borde (morado azul oscuro)
            activebackground="#9370DB",  # Color al pasar el cursor por encima (morado claro)
        )

        # Crear canvas
        self.canvas = Canvas(
            self.window,
            bg="#141432",
            height=height,
            width=width,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )
        self.canvas.place(x=0, y=0)
        self.canvas.create_rectangle(0.0, 0.0, width, 90.0, fill="#1D1D42", outline="")

        # Cargar y preparar recursos

        self.artist_list = artist_list  # Listas globales
        self.requester_list = requester_list  # Listas globales
        self.load_images()
        self.create_buttons()
        self.create_images()

    def relative_to_assets(self, path: str) -> Path:
        """Convierte rutas relativas a la carpeta de assets"""
        return self.assets_path / Path(path)

    def load_images(self):
        """Cargar todas las imágenes"""
        self.button_image_1 = PhotoImage(file=self.relative_to_assets("button_1.png"))
        self.button_image_2 = PhotoImage(file=self.relative_to_assets("button_2.png"))
        self.button_image_3 = PhotoImage(file=self.relative_to_assets("button_3.png"))
        self.button_image_4 = PhotoImage(file=self.relative_to_assets("button_4.png"))
        self.button_image_5 = PhotoImage(file=self.relative_to_assets("button_5.png"))

        self.image_1 = PhotoImage(file=self.relative_to_assets("image_1.png"))
        self.image_2 = PhotoImage(file=self.relative_to_assets("image_2.png"))
        self.image_3 = PhotoImage(file=self.relative_to_assets("image_3.png"))
        self.image_4 = PhotoImage(file=self.relative_to_assets("image_4.png"))
        self.image_5 = PhotoImage(file=self.relative_to_assets("image_5.png"))
        self.image_6 = PhotoImage(file=self.relative_to_assets("image_6.png"))
        self.image_7 = PhotoImage(file=self.relative_to_assets("image_7.png"))
        self.image_8 = PhotoImage(file=self.relative_to_assets("image_8.png"))

    def create_buttons(self):
        """Crear todos los botones"""
        self.button_1 = Button(
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.log_out,
            relief="flat",
            bg="#1D1D42",
            activebackground="#1D1D42",
        )
        self.button_1.place(x=804.0, y=23.0, width=171.0, height=44.0)

        buttons_config = [
            (self.button_image_2, 73.0, 262.0, "button_2", self.load_requesters),
            (self.button_image_3, 73.0, 345.0, "button_3", self.load_artists),
            (self.button_image_4, 73.0, 428.0, "button_4", self.requester_report),
            (self.button_image_5, 73.0, 511.0, "button_5", self.artist_report),
        ]

        for image, x, y, name, command in buttons_config:
            button = Button(
                image=image,
                borderwidth=0,
                highlightthickness=0,
                command=command,
                relief="flat",
                bg="#141432",
                activebackground="#141432",
            )
            button.place(x=x, y=y, width=240.0, height=45.0)

    def create_images(self):
        """Crear todas las imágenes en el canvas"""
        self.create_scrollable_frame()

        image_positions = [
            (self.image_1, 190.0, 45.0),
            (self.image_2, 686.0, 149.0),
            (self.image_4, 193.0, 186.0),
            (self.image_5, 411.0, 201.0),
            (self.image_6, 958.0, 201.0),
            (self.image_7, 411.0, 607.0),
            (self.image_8, 958.0, 614.0),
        ]

        for image, x, y in image_positions:
            image = self.canvas.create_image(x, y, image=image)
            self.canvas.tag_raise(image)

    def create_scrollable_frame(self):
        """Crear un frame con barras de desplazamiento"""
        # Adjust the position and size to fit between the specified images
        container_frame = Frame(self.window, bg="#4B0082", width=520, height=350)

        # Positioning the frame between image_4 (193.0, 186.0) and image_5 (411.0, 201.0)
        frame_id = self.canvas.create_window(
            420.0,  # Centered between image_4 and image_5
            225.0,  # Lowered to avoid overlapping with other images
            window=container_frame,
            width=530,
            height=360,
            anchor="nw",
        )

        # Scrollbars personalizadas con ttk y estilo
        self.scrollbar_y = ttk.Scrollbar(
            container_frame, orient="vertical", style="Custom.Vertical.TScrollbar"
        )
        self.scrollbar_y.pack(side="right", fill="y")

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
            text="No content available",
            font=("Helvetica", 16, "bold"),
            bg="#4B0082",
            fg="white",
            anchor="center",
        ).pack(
            expand=True, fill="both", pady=150, padx=150
        )  # Usar 'expand' para centrar verticalmente

        self.inner_frame.update_idletasks()
        self.scrollable_frame.config(scrollregion=self.scrollable_frame.bbox("all"))

        # Send the scrollable frame to the back
        self.canvas.tag_lower(frame_id)

    def display_svg_in_scroll_frame(self, svg_path):
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

    def load_requesters(self):
        files = filedialog.askopenfilenames(
            title="Select Requester XML Files", filetypes=[("XML Files", "*.xml")]
        )

        for file in files:
            XMLParser.load_requesters(file, self.requester_list)

        messagebox.showinfo("Load Complete", f"{len(files)} requester files loaded")

    def load_artists(self):
        files = filedialog.askopenfilenames(
            title="Select Artist XML Files", filetypes=[("XML Files", "*.xml")]
        )

        for file in files:
            XMLParser.load_artists(file, self.artist_list)

        messagebox.showinfo("Load Complete", f"{len(files)} artist files loaded")

    def requester_report(self):
        if self.requester_list.is_empty():
            messagebox.showerror(
                "Error", "No hay solicitantes para generar el reporte."
            )
            return

        report_path = "./Reportes/ListaSolicitantes.svg"
        self.requester_list.generate_report(report_path)
        self.display_svg_in_scroll_frame(report_path)
        messagebox.showinfo(
            "Reporte generado", "El reporte de solicitantes ha sido generado."
        )

    def artist_report(self):
        if self.artist_list.is_empty():
            messagebox.showerror("Error", "No hay artistas para generar el reporte.")
            return

        report_path = "./Reportes/ListaArtistas.svg"
        self.artist_list.generate_report(report_path)
        self.display_svg_in_scroll_frame(report_path)
        messagebox.showinfo(
            "Reporte generado", "El reporte de artistas ha sido generado."
        )

    def log_out(self):
        """Close admin window and return to login"""
        self.window.destroy()  # Close current window

        login = LoginView()  # Create new login window
        login.run()  # Start login window mainloop

    def run(self):
        """Iniciar el bucle principal de la aplicación"""
        self.window.mainloop()


if __name__ == "__main__":
    app = AdminView()
    app.run()
