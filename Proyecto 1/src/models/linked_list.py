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

    def search(self, artist_id, pwd):
        current = self.head
        while current:
            if (
                hasattr(current.data, "artist_id")
                and current.data.artist_id == artist_id
                and current.data.pwd == pwd
            ):
                return current.data
            current = current.next
        return None

    def search_by_id(self, artist_id):
        current = self.head
        while current:
            if (
                hasattr(current.data, "artist_id")
                and current.data.artist_id == artist_id
            ):
                return current.data
            current = current.next
        return None

    def generate_report(self, filename="ListaArtistas"):
        os.makedirs("Reportes", exist_ok=True)

        dot = graphviz.Digraph(
            "ListaArtistas",
            filename=f"./Reportes/{filename}",
            format="svg",
            node_attr={"shape": "record", "style": "filled", "fillcolor": "lightgreen"},
        )

        current = self.head
        while current:
            artist = current.data
            label = (
                f"ID: {artist.artist_id}\\n"
                f"Nombre: {artist.full_name}\\n"
                f"Email: {artist.email}\\n"
                f"Teléfono: {artist.phone}\\n"
                f"Especialidades: {artist.specialties}\\n"
                f"Notas: {artist.additional_notes}"
            )

            dot.node(artist.artist_id, label)

            # Conexión al siguiente nodo
            if current.next:
                dot.edge(artist.artist_id, current.next.data.artist_id)

            current = current.next

        dot.render(cleanup=True)

    def insert_processed(self, artist_id, processed_item):
        current = self.head
        while current:
            if current.data.artist_id == artist_id:
                current.data.processed.insert(processed_item)
                break
            current = current.next
