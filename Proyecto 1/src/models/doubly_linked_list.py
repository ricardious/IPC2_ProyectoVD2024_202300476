import os
import graphviz


class DoublyNode:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None


class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def insert(self, data):
        new_node = DoublyNode(data)
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node

    def __iter__(self):
        """Make the list iterable."""
        self._current = self.head
        return self

    def __next__(self):
        """Iterate through the list."""
        if self._current is None:
            raise StopIteration
        data = self._current.data
        self._current = self._current.next
        return data

    def get_all(self):
        """Return all the elements in the list."""
        elements = DoublyLinkedList()
        current = self.head
        while current:
            elements.insert(current.data)
            current = current.next
        return elements

    def size(self):
        """Return the size of the list."""
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count

    def is_empty(self):
        """Check if the list is empty."""
        return self.head is None

    def search(self, data):
        current = self.head
        while current:
            if current.data["id"] == data["id"] and current.data["pwd"] == data["pwd"]:
                return current.data  # Retorna el nodo encontrado
            current = current.next
        return None

    def generate_report(self, filename="ListaSolicitantes"):
        os.makedirs("Reportes", exist_ok=True)

        dot = graphviz.Digraph(
            "ListaSolicitantes",
            filename=f"./Reportes/{filename}",
            format="png",
            node_attr={"shape": "record", "style": "filled", "fillcolor": "lightblue"},
        )

        current = self.head
        while current:
            data = current.data
            label = (
                f"ID: {data['id']}\\n"
                f"Nombre: {data['full_name']}\\n"
                f"Email: {data['email']}\\n"
                f"Teléfono: {data['phone']}\\n"
                f"Dirección: {data['address']}"
            )

            dot.node(data["id"], label)

            # Conexión al siguiente nodo
            if current.next:
                dot.edge(current.data["id"], current.next.data["id"], color="blue")

            # Conexión al nodo anterior
            if current.prev:
                dot.edge(
                    current.data["id"],
                    current.prev.data["id"],
                    color="red",
                    style="dashed",
                )

            current = current.next

        dot.render(cleanup=True)
