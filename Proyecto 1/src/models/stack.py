import os
from graphviz import Digraph


class Node:
    def __init__(self, value):
        """Nodo para la pila."""
        self.value = value
        self.down = None


class Stack:
    def __init__(self):
        """Inicialización de la pila."""
        self.top = None
        self.size = 0

    def __len__(self):
        """Devuelve el tamaño de la pila."""
        return self.size

    def push(self, value):
        """Agrega un elemento a la pila."""
        newNode = Node(value)
        newNode.down = self.top
        self.top = newNode
        self.size += 1

    def pop(self):
        """Elimina y devuelve el elemento superior de la pila."""
        if self.top is None:
            return None
        removedNode = self.top.value
        self.top = self.top.down
        self.size -= 1
        return removedNode

    def peek(self):
        """Devuelve el elemento superior de la pila sin eliminarlo."""
        if self.top is None:
            return None
        return self.top.value

    def isEmpty(self):
        """Verifica si la pila está vacía."""
        return self.top is None

    def show(self):
        """Muestra los elementos de la pila."""
        if self.isEmpty():
            print("Stack is empty")
            return

        current = self.top
        while current is not None:
            print(current.value)
            current = current.down

    def graph(self, filename="stack"):
        """Genera una visualización gráfica de la pila usando Graphviz."""
        # Create Reportes directory
        os.makedirs("Reportes", exist_ok=True)

        # Initialize graph
        dot = Digraph(comment="Stack Visualization")
        dot.attr(rankdir="TB")
        dot.attr("node", shape="box", style="filled")

        if self.isEmpty():
            dot.node("empty", "Empty Stack", fillcolor="#FF9999")
        else:
            current = self.top
            prev_id = None
            count = 0

            while current is not None:
                # Evitar desbordamiento de los colores
                red = max(0, min(255, 255 - count * 20))
                green = max(0, min(255, 150 + count * 20))
                blue = 255
                color = f"#{red:02x}{green:02x}{blue:02x}"

                # Crear el nodo para el grafo
                node_id = f"node_{count}"
                dot.node(node_id, str(current.value), fillcolor=color)

                # Conectar el nodo actual con el nodo anterior
                if prev_id is not None:
                    dot.edge(prev_id, node_id)

                # Actualizar las referencias
                prev_id = node_id
                current = current.down
                count += 1

        # Definir la ruta y el nombre del archivo .svg
        svg_path = os.path.join("Reportes", f"{filename}")

        # Renderizar y guardar el grafo como archivo SVG
        dot.render(svg_path, format="svg", cleanup=True)
