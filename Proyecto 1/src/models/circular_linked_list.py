import os
import graphviz


class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class CircularLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def __len__(self):
        return self.size

    def insert(self, value):
        new_node = Node(value)
        # IF THE LIST IS EMPTY
        if self.head is None and self.tail is None:
            # 1. Assign the new node as the head of the list
            self.head = new_node
            # 2. Assign the new node as the tail of the list
            self.tail = new_node
            # 3. The tail node points to the head node
            self.tail.next = self.head
        # IF THE LIST IS NOT EMPTY
        else:
            # 1. The next of the tail node points to the new node
            self.tail.next = new_node
            # 2. The new node becomes the tail node
            self.tail = new_node
            # 3. The next of the tail node points to the head node
            self.tail.next = self.head
        self.size += 1

    def display(self):
        counter = 0
        current = self.head
        while counter < self.size:
            print(current.value)
            current = current.next
            counter += 1

    def get_value(self, id):
        counter = 0
        current = self.head
        while counter < self.size:
            if current.value.id == id:
                return current.value
            current = current.next
            counter += 1
        return None

    def generate_graph(self, filename="Procesadas"):
        try:
            # Crear el directorio si no existe
            os.makedirs("Reportes", exist_ok=True)

            # Configurar el grafo
            dot = graphviz.Digraph(
                "CircularList",
                filename=f"./Reportes/{filename}",
                format="svg",
                node_attr={
                    "shape": "record",
                    "style": "filled",
                    "fillcolor": "lightblue",
                    "fontsize": "12",
                },
            )

            if self.size == 0:
                # Si la lista está vacía, crear un nodo que lo indique
                dot.node("empty", "Lista vacía")
            else:
                # Crear los nodos con la información de la imagen
                counter = 0
                current = self.head
                while counter < self.size:
                    # Formatear la información de la imagen
                    node_label = f"{{Request ID: {current.value.request_id}|Name: {current.value.name}}}"
                    dot.node(str(counter), node_label)

                    # Crear la conexión al siguiente nodo
                    next_index = (counter + 1) % self.size
                    dot.edge(str(counter), str(next_index))

                    current = current.next
                    counter += 1

            # Renderizar el grafo
            dot_path = f"./Reportes/{filename}"
            dot.render(cleanup=True)

            # Verificar que el archivo se creó correctamente
            svg_path = f"{dot_path}.svg"
            if not os.path.exists(svg_path):
                raise Exception(f"Failed to generate SVG file at {svg_path}")

            return os.path.abspath(svg_path)

        except Exception as e:
            print(f"Error generating graph: {str(e)}")
            return None
