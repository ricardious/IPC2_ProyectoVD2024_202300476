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

    def search(self, requester_id, pwd):
        current = self.head
        while current:
            if (
                hasattr(current.data, "requester_id")
                and current.data.requester_id == requester_id
                and current.data.pwd == pwd
            ):
                return current.data
            current = current.next
        return None

    def generate_report(self, filename="ListaSolicitantes"):
        os.makedirs("Reportes", exist_ok=True)

        dot = graphviz.Digraph(
            "ListaSolicitantes",
            filename=f"./Reportes/{filename}",
            format="svg",
            node_attr={"shape": "record", "style": "filled", "fillcolor": "lightblue"},
        )

        current = self.head
        while current:
            # Acceder a los atributos del objeto en lugar de las claves del diccionario
            requester = current.data
            label = (
                f"ID: {requester.requester_id}\\n"
                f"Nombre: {requester.full_name}\\n"
                f"Email: {requester.email}\\n"
                f"Teléfono: {requester.phone}\\n"
                f"Dirección: {requester.address}"
            )

            dot.node(requester.requester_id, label)

            # Conexión al siguiente nodo
            if current.next:
                dot.edge(
                    current.data.requester_id,
                    current.next.data.requester_id,
                    color="blue",
                )

            # Conexión al nodo anterior
            if current.prev:
                dot.edge(
                    current.data.requester_id,
                    current.prev.data.requester_id,
                    color="red",
                    style="dashed",
                )

            current = current.next

        dot.render(cleanup=True)

    def insert_to_user_stack(self, requester_id, value):
        """Insert a value into the stack of a specific user."""
        current = self.head
        while current:
            if current.data.requester_id == requester_id:
                current.data.push_stack(value)
                break
            current = current.next

    def pop_from_user_stack(self, requester_id):
        """Remove and return the top value from a specific user's stack."""
        current = self.head
        while current:
            if current.data.requester_id == requester_id:
                if current.data.cart_stack.isEmpty():
                    return None
                return current.data.pop_stack()
            current = current.next
        return None

    def insert_user_image(self, requester_id, image):
        """Insert an image for a specific user."""
        current = self.head
        while current:
            if current.data.requester_id == requester_id:
                current.data.insert_image(image)
                break
            current = current.next
