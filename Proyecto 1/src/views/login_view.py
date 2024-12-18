import os
from pathlib import Path
from typing import Optional, Union

import tkinter as tk

from tkinter import Canvas, Entry, PhotoImage, messagebox

from PIL import Image, ImageTk, ImageEnhance, ImageFont
from global_state import artist_list, requester_list

# Importar utilidad de fuentes (asumiendo que está en la misma carpeta o en el path)
from utils.window_utils import center_window


class LoginView:
    def __init__(self, window_width: int = 1000, window_height: int = 700):
        # Configurar rutas de archivos
        self.OUTPUT_PATH = Path(__file__).parent
        self.ASSETS_PATH = self.OUTPUT_PATH / "../../assets/login_assets/"

        # Crear ventana principal
        self.window = tk.Tk()
        self.window.title("Login")

        # Centrar y configurar ventana
        center_window(self.window, window_width, window_height)
        self.window.configure(bg="#FFFFFF")
        self.window.resizable(False, False)

        # Configurar canvas
        self.canvas = Canvas(
            self.window,
            bg="#FFFFFF",
            height=window_height,
            width=window_width,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )
        self.canvas.place(x=0, y=0)

        self.artist_list = artist_list  # Listas globales
        self.requester_list = requester_list  # Listas globales
        # Inicializar elementos
        self.create_background()
        self.create_entries()
        self.create_button()
        # Configurar evento de doble clic para quitar foco
        self.setup_defocus_event()

    def setup_defocus_event(self):
        """
        Configura un evento de doble clic en el canvas para quitar el foco de los entries
        """

        def on_double_click(event):
            # Verificar si alguno de los entries tiene foco
            focused_widget = self.window.focus_get()

            # Si hay un entry con foco, quitarle el foco
            if focused_widget in self.entries:
                # Quitar foco estableciendo el foco en la ventana principal
                self.window.focus_force()

        # Bind del evento de doble clic en todo el canvas
        self.canvas.bind("<Double-Button-1>", on_double_click)

    def relative_to_assets(self, path: str) -> Path:
        return self.ASSETS_PATH / Path(path)

    def create_background(self):
        # Cargar imágenes de fondo
        background_images = [
            "image_1.png",
            "image_2.png",
            "image_3.png",
            "image_4.png",
            "image_5.png",
            "image_6.png",
        ]

        positions = [
            (500.0, 350.0),  # image_1
            (500.0, 414.0),  # image_2
            (500.0, 488.0),  # image_3
            (643.0, 489.0),  # image_4
            (643.0, 415.0),  # image_5
            (500.0, 190.0),  # image_6
        ]

        # Almacenar referencias para evitar recolección de basura
        self.bg_images = []

        for img_name, pos in zip(background_images, positions):
            img = PhotoImage(file=self.relative_to_assets(img_name))
            self.bg_images.append(img)
            self.canvas.create_image(pos[0], pos[1], image=img)

        # Cargar imagen adicional para el cambio de fondo
        self.image_7 = PhotoImage(file=self.relative_to_assets("image_7.png"))
        self.image_8 = PhotoImage(file=self.relative_to_assets("image_8.png"))

        # Texto de título
        self.canvas.create_text(
            392.0,
            295.0,
            anchor="nw",
            text="Login",
            fill="#FFFFFF",
            font=("Daydream", 45 * -1),
        )

    def create_entries(self):
        # Configuraciones de entradas
        entry_configs = [
            {
                "img_name": "entry_1.png",
                "x": 353.0,
                "y": 392.0,
                "placeholder": "Username",
                "show": None,
                "special_image": "image_7.png",
            },
            {
                "img_name": "entry_2.png",
                "x": 353.0,
                "y": 466.0,
                "placeholder": "Password",
                "show": "•",
                "special_image": "image_8.png",
            },
        ]

        # Almacenar referencias de imágenes e inputs
        self.entry_images = []
        self.entries = []

        # Imagen de fondo original de image_6
        canvas_items = self.canvas.find_all()
        self.image_6_bg = canvas_items[5]  # Asume que image_6 es el sexto elemento

        for i, config in enumerate(entry_configs):
            # Imagen de fondo de entrada
            entry_image = PhotoImage(file=self.relative_to_assets(config["img_name"]))
            self.entry_images.append(entry_image)

            # Crear fondo de imagen
            entry_bg = self.canvas.create_image(
                490.0, config["y"] + 22.5, image=entry_image
            )

            # Crear entrada
            entry = Entry(
                bd=0,
                bg="#A725CB",
                fg="#000716",
                highlightthickness=0,
                show=config["show"],
                font=("Pixelify Sans", 20),
            )
            entry.place(x=config["x"], y=config["y"], width=274.0, height=43.0)

            self.add_placeholder(
                entry,
                config["placeholder"],
                config["show"],
                is_username_entry=(i == 0),
                is_password_entry=(i == 1),
                special_image=config["special_image"],
            )

            self.entries.append(entry)

    def add_placeholder(
        self,
        entry,
        placeholder_text,
        show,
        is_username_entry=False,
        is_password_entry=False,
        special_image=None,
    ):
        default_color = "#FFFFFF"  # Color del texto
        placeholder_color = "#FFC1E3"  # Color del placeholder

        def on_focus_in(event):
            # Quitar el placeholder al enfocar si el texto es igual al placeholder
            if entry.get() == placeholder_text:
                entry.delete(0, tk.END)
                entry.config(
                    fg=default_color, show=show
                )  # Aplicar `show` solo cuando no sea placeholder

            # Cambiar imagen de fondo según el tipo de entrada
            if is_username_entry:
                self.canvas.itemconfig(self.image_6_bg, image=self.image_7)
            elif is_password_entry:
                self.canvas.itemconfig(self.image_6_bg, image=self.image_8)

        def on_focus_out(event):
            # Restaurar el placeholder si el campo está vacío
            if not entry.get():
                entry.insert(0, placeholder_text)
                entry.config(
                    fg=placeholder_color, show=""
                )  # Eliminar `show` para mostrar el placeholder

            # Restaurar imagen de fondo original
            if is_username_entry or is_password_entry:
                self.canvas.itemconfig(self.image_6_bg, image=self.bg_images[5])

        # Inicializar con el placeholder
        entry.insert(0, placeholder_text)
        entry.config(
            fg=placeholder_color, show=""
        )  # Mostrar el placeholder como texto normal

        # Vincular eventos de foco
        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

    def create_button(self):
        # Cargar imagen original
        original_image = Image.open(self.relative_to_assets("button_1.png"))

        # Crear versiones de imagen
        button_image_1 = ImageTk.PhotoImage(original_image)
        button_image_hover = ImageTk.PhotoImage(self.create_hover_image(original_image))
        button_image_press = ImageTk.PhotoImage(self.create_press_image(original_image))

        # Crear botón en el canvas
        self.button_1 = self.canvas.create_image(500.0, 576.0, image=button_image_1)

        # Almacenar referencias para evitar recolección de basura
        self.button_images = [button_image_1, button_image_hover, button_image_press]

        # Configurar eventos
        self.canvas.tag_bind(
            self.button_1,
            "<Enter>",
            lambda event: self.canvas.itemconfig(
                self.button_1, image=button_image_hover
            ),
        )

        self.canvas.tag_bind(
            self.button_1,
            "<Leave>",
            lambda event: self.canvas.itemconfig(self.button_1, image=button_image_1),
        )

        self.canvas.tag_bind(
            self.button_1,
            "<ButtonPress-1>",
            lambda event: self.canvas.itemconfig(
                self.button_1, image=button_image_press
            ),
        )

        self.canvas.tag_bind(self.button_1, "<ButtonRelease-1>", self.on_button_release)

    @staticmethod
    def create_hover_image(img):
        enhancer = ImageEnhance.Brightness(img)
        return enhancer.enhance(1.2)

    @staticmethod
    def create_press_image(img):
        enhancer = ImageEnhance.Brightness(img)
        return enhancer.enhance(0.8)

    def on_button_release(self, event):
        # Restaurar imagen original
        self.canvas.itemconfig(self.button_1, image=self.button_images[0])

        # Obtener usuario y contraseña ingresados
        username = self.entries[0].get()
        password = self.entries[1].get()

        # Validar credenciales
        if username == "AdminIPC" and password == "ARTIPC2":
            print("Login exitoso: Administrador")
            self.window.destroy()  # Cierra la ventana de login
            self.open_admin_window()  # Abre la ventana del administrador
            return

        # Verificar si el usuario es un Artista (que el ID comience con ART-)
        if username.startswith("ART-"):
            usuario_artista = self.artist_list.search({"id": username, "pwd": password})
            if usuario_artista is not None:
                print(f"Login exitoso: Artista {usuario_artista['full_name']}")
                self.window.destroy()  # Cierra la ventana de login
                self.open_artist_window(usuario_artista)  # Abre la vista del artista
                return

        # Verificar si el usuario es un Solicitante (que el ID comience con IPC-)
        if username.startswith("IPC-"):
            usuario_solicitante = self.requester_list.search(
                {"id": username, "pwd": password}
            )
            if usuario_solicitante is not None:
                print(f"Login exitoso: Solicitante {usuario_solicitante['full_name']}")
                self.window.destroy()  # Cierra la ventana de login
                self.open_requester_window(
                    usuario_solicitante
                )  # Abre la vista del solicitante
                return

        # Si no coincide con ninguno, mostrar error
        print("Credenciales incorrectas")
        tk.messagebox.showerror("Error de Login", "Usuario o contraseña incorrectos.")

    def open_admin_window(self):
        from views.admin_view import AdminView

        admin_view = AdminView()
        admin_view.run()

    def open_artist_window(self, artista):
        print(f"Abriendo ventana para el artista: {artista['full_name']}")
        from views.artist_view import ArtistView

        artist_view = ArtistView(artista)
        artist_view.run()

    def open_requester_window(self, solicitante):
        print(f"Abriendo ventana para el solicitante: {solicitante['full_name']}")
        # Aquí iría la lógica para abrir la ventana del solicitante
        from views.requester_view import RequesterView

        requester_view = RequesterView(solicitante)
        requester_view.run()

    def run(self):
        self.window.mainloop()
