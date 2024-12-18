import os
import graphviz


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def insert(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def __iter__(self):
        self._current = self.head
        return self

    def __next__(self):
        if self._current is None:
            raise StopIteration
        data = self._current.data
        self._current = self._current.next
        return data

    def get_all(self):
        elements = LinkedList()
        current = self.head
        while current:
            elements.insert(current.data)
            current = current.next
        return elements

    def size(self):
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count

    def is_empty(self):
        return self.head is None

    def search(self, data):
        current = self.head
        while current:
            if current.data["id"] == data["id"] and current.data["pwd"] == data["pwd"]:
                return current.data  # Retorna el nodo encontrado
            current = current.next
        return None

    def generate_report(self, filename="ListaArtistas"):
        os.makedirs("Reportes", exist_ok=True)

        dot = graphviz.Digraph(
            "ListaArtistas",
            filename=f"./Reportes/{filename}",
            format="png",
            node_attr={"shape": "record", "style": "filled", "fillcolor": "lightgreen"},
        )

        current = self.head
        while current:
            data = current.data
            label = (
                f"ID: {data['id']}\\n"
                f"Nombre: {data['full_name']}\\n"
                f"Email: {data['email']}\\n"
                f"Teléfono: {data['phone']}\\n"
                f"Especialidades: {data['specialties']}\\n"
                f"Notas: {data['additional_notes']}"
            )

            dot.node(data["id"], label)

            # Conexión al siguiente nodo
            if current.next:
                dot.edge(data["id"], current.next.data["id"])

            current = current.next

        dot.render(cleanup=True)
