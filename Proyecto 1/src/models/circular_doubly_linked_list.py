import os
import graphviz


class Node:
    def __init__(self, image_matrix):
        """Constructor del nodo."""
        self.image_matrix = image_matrix  # Matriz dispersa que representa la imagen
        self.next = None  # Referencia al siguiente nodo
        self.prev = None  # Referencia al nodo anterior


class CircularDoublyLinkedList:
    def __init__(self):
        """Constructor de la lista doblemente circular enlazada."""
        self.head = None

    def is_empty(self):
        """Verifica si la lista está vacía."""
        return self.head is None

    def append(self, image_matrix):
        """Agrega una nueva imagen (matriz dispersa) al final de la lista."""
        new_node = Node(image_matrix)

        if self.is_empty():
            self.head = new_node
            self.head.next = self.head
            self.head.prev = self.head
        else:
            tail = self.head.prev
            tail.next = new_node
            new_node.prev = tail
            new_node.next = self.head
            self.head.prev = new_node

    def display(self):
        """Muestra las imágenes en la lista."""
        if self.is_empty():
            print("La lista está vacía.")
            return

        current = self.head
        while True:
            print(current.image_matrix)
            current = current.next
            if current == self.head:
                break

    def get_next(self, id):
        if self.is_empty():
            return None
        current = self.head
        while True:
            if current.image_matrix.id == id:
                return current.next.image_matrix
            current = current.next
            if current == self.head:
                break
        return None

    def get_prev(self, id):
        if self.is_empty():
            return None
        current = self.head
        while True:
            if current.image_matrix.id == id:
                return current.prev.image_matrix
            current = current.next
            if current == self.head:
                break
        return None

    def display_current_image(self):
        """Devuelve la imagen de la posición actual."""
        if self.is_empty():
            return None
        return self.head.image_matrix

    def generate_graph(self, filename="DoublyCircularList"):
        """
        Genera una visualización de la lista doblemente enlazada circular en formato DOT y elimina el archivo DOT después de renderizar la imagen.

        Args:
            filename (str): Nombre del archivo a generar
        """
        os.makedirs("Reportes", exist_ok=True)
        codigodot = ""
        codigodot += """digraph G {
        rankdir=LR;
        node[shape=record, height=.1];
        """

        if not self.is_empty():
            # Crear los nodos
            current = self.head
            contador_nodos = 0
            while True:
                label = f"{{<f1>|[ Matrix ]|<f2>}}"
                if current == self.head:
                    label = f"{{<f1>|[ Matrix ]\\n(Current)|<f2>}}"

                codigodot += f'nodo{contador_nodos} [label="{label}"];\n'
                current = current.next
                contador_nodos += 1
                if current == self.head:
                    break

            # Crear los enlaces hacia adelante
            for i in range(contador_nodos):
                codigodot += (
                    f"nodo{i}:f2 -> nodo{(i + 1) % contador_nodos}:f1 [dir=both];\n"
                )

            # Enlace entre el último y el primero (circularidad)
            codigodot += f"nodo0:f1 -> nodo{contador_nodos - 1}:f2 [dir=both, constraint=false];\n"

        codigodot += "}"

        # Escribir el archivo DOT
        ruta_dot = f"./Reportes/{filename}.dot"
        with open(ruta_dot, "w") as archivo:
            archivo.write(codigodot)

        # Generar la imagen
        ruta_imagen = f"./Reportes/{filename}.svg"
        os.system(f"dot -Tsvg {ruta_dot} -o {ruta_imagen}")

        # Eliminar el archivo DOT
        if os.path.exists(ruta_dot):
            os.remove(ruta_dot)

        # Abrir la imagen generada
        ruta_abrir_imagen = os.path.abspath(ruta_imagen)
        os.startfile(ruta_abrir_imagen)
