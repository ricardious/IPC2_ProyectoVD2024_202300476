import re
from graphviz import Digraph


class Node:
    def __init__(self, value):
        """Nodo de la cola."""
        self.value = value
        self.next = None


class Queue:
    def __init__(self):
        """Constructor de la cola."""
        self.front = None
        self.rear = None
        self.size = 0

    def __len__(self):
        """Devuelve el tamaño de la cola."""
        return self.size

    def enqueue(self, value):
        """Agrega un elemento al final de la cola."""
        newNode = Node(value)
        if self.rear is None:
            self.front = self.rear = newNode
        else:
            self.rear.next = newNode
            self.rear = newNode
        self.size += 1

    def dequeue(self):
        """Elimina y devuelve el primer elemento de la cola."""
        if self.front is None:
            return None
        removedNode = self.front.value
        self.front = self.front.next
        if self.front is None:
            self.rear = None
        self.size -= 1
        return removedNode

    def peek(self):
        """Devuelve el primer elemento de la cola sin eliminarlo."""
        if self.front is None:
            return None
        return self.front.value

    def isEmpty(self):
        """Verifica si la cola está vacía."""
        return self.front is None

    def show(self):
        """Muestra los elementos de la cola."""
        if self.isEmpty():
            print("Queue is empty")
            return

        current = self.front
        while current is not None:
            print(current.value)
            current = current.next

    def generate_graph(self, filename="Cola"):
        """Genera un archivo SVG que representa la cola."""
        dot = Digraph(format="svg")
        dot.attr(rankdir="TB", size="8,12")  # Aumentado el tamaño

        # Configuración de nodos con texto más grande
        dot.attr(
            "node",
            shape="circle",
            style="filled",
            fillcolor="lightblue",
            color="black",
            fontname="Arial",
            fontcolor="white",
            fontsize="16",  # Texto más grande
            width="1.5",  # Nodos más grandes
            height="1.5",
        )

        if self.isEmpty():
            # Crear un nodo especial para cola vacía
            dot.node(
                "empty",
                "Cola\nVacía",
                shape="circle",
                style="filled",
                fillcolor="#FFB6C1",  # Color rosa claro
                fontsize="20",
            )
        else:
            current = self.front
            index = 0
            prev_y = 0
            spacing = 2  # Espaciado vertical entre nodos

            while current is not None:
                formatted_value = "\n".join(str(current.value).split("\n"))
                # Posicionar cada nodo con coordenadas específicas
                dot.node(f"node{index}", f"{formatted_value}", pos=f"0,{prev_y}")

                if current.next is not None:
                    dot.edge(f"node{index}", f"node{index + 1}")

                current = current.next
                index += 1
                prev_y -= spacing  # Mover hacia abajo para el siguiente nodo

        output_path = f"./Reportes/{filename}"
        dot.render(output_path, cleanup=True)
        print(f"SVG generado en {output_path}.svg")
        self.add_gradient_to_svg(f"{output_path}.svg")

    def add_gradient_to_svg(self, file_path):
        """Agrega un gradiente al archivo SVG generado."""
        with open(file_path, "r") as file:
            content = file.read()

        # Gradiente más llamativo
        gradient_def = (
            "<defs>\n"
            '  <linearGradient id="grad1" x1="0%" y1="0%" x2="0%" y2="100%">\n'
            '    <stop offset="0%" style="stop-color:#FF69B4;stop-opacity:1" />\n'  # Rosa
            '    <stop offset="50%" style="stop-color:#9370DB;stop-opacity:1" />\n'  # Púrpura
            '    <stop offset="100%" style="stop-color:#4169E1;stop-opacity:1" />\n'  # Azul real
            "  </linearGradient>\n"
            "</defs>\n"
        )

        content = re.sub(r"(<svg[^>]*>)", r"\1\n" + gradient_def, content, count=1)
        content = content.replace('fill="lightblue"', 'fill="url(#grad1)"')
        content = content.replace(
            'fill="#FFB6C1"', 'fill="url(#grad1)"'
        )  # Aplicar gradiente al nodo vacío

        with open(file_path, "w") as file:
            file.write(content)
        print(f"Gradiente añadido a {file_path}")
