from models.circular_doubly_linked_list import CircularDoublyLinkedList
from models.stack import Stack


class Requester:
    def __init__(self, requester_id, pwd, full_name, email, phone, address):
        """Constructor de la clase solicitante."""
        self.requester_id = requester_id
        self.pwd = pwd
        self.full_name = full_name
        self.email = email
        self.phone = phone
        self.address = address
        self.image_gallery = (
            CircularDoublyLinkedList()
        )  # Galería de imágenes del solicitante
        self.cart_stack = Stack()  # Pila de carrito de imágenes del solicitante

    def add_image_to_gallery(self, image_matrix):
        """Agrega una imagen (matriz dispersa) a la galería de imágenes del solicitante."""
        self.image_gallery.append(image_matrix)

    def view_gallery_forward(self):
        """Muestra la galería desde la posición actual hacia adelante."""
        return self.image_gallery.traverse_forward()

    def view_gallery_backward(self):
        """Muestra la galería desde la posición actual hacia atrás."""
        return self.image_gallery.traverse_backward()

    def next_image(self):
        """Mueve la posición actual hacia la siguiente imagen."""
        self.image_gallery.move_forward()

    def previous_image(self):
        """Mueve la posición actual hacia la imagen anterior."""
        self.image_gallery.move_backward()

    def view_current_image(self):
        """Muestra la imagen actual de la galería."""
        return self.image_gallery.display_current_image()

    # Métodos de la pila de carrito de imágenes
    def add_image_to_cart(self, image_matrix):
        """Agrega una imagen al carrito de imágenes del solicitante."""
        self.cart_stack.push(image_matrix)

    def remove_image_from_cart(self):
        """Elimina y devuelve la imagen superior de la pila de carrito."""
        return self.cart_stack.pop()

    def view_current_cart_image(self):
        """Muestra la imagen superior de la pila de carrito sin eliminarla."""
        return self.cart_stack.peek()

    def view_cart_images(self):
        """Muestra todas las imágenes en la pila de carrito."""
        print("Imágenes en el carrito:")
        self.cart_stack.show()

    def is_cart_empty(self):
        """Verifica si la pila de carrito está vacía."""
        return self.cart_stack.isEmpty()

    def push_stack(self, value):
        """Inserta un valor en la pila de carrito."""
        self.cart_stack.push(value)

    def pop_stack(self):
        return self.cart_stack.pop()

    def insert_image(self, image_matrix):
        """Inserta una imagen en la galería del solicitante."""
        self.image_gallery.append(image_matrix)
