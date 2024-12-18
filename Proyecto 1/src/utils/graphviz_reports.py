import os
import graphviz


class GraphvizReports:
    @staticmethod
    def generate_requester_report(requester_list):
        os.makedirs("Reports", exist_ok=True)

        dot = graphviz.Digraph(
            "RequesterList",
            filename="./Reports/RequesterList.svg",
            node_attr={"shape": "record", "style": "filled", "fillcolor": "lightblue"},
        )

        current = requester_list.head
        previous = None

        while current:
            data = current.data
            label = (
                f"ID: {data['id']}\\n"
                f"Name: {data['full_name']}\\n"
                f"Email: {data['email']}\\n"
                f"Phone: {data['phone']}\\n"
                f"Address: {data['address']}"
            )

            dot.node(data["id"], label)

            if previous:
                dot.edge(previous.data["id"], data["id"], constraint="true")

            previous = current
            current = current.next

        dot.render(format="svg")
        print("Requester report generated at ./Reports/RequesterList.svg")

    @staticmethod
    def generate_artist_report(artist_list):
        os.makedirs("Reports", exist_ok=True)

        dot = graphviz.Digraph(
            "ArtistList",
            filename="./Reports/ArtistList.svg",
            node_attr={"shape": "record", "style": "filled", "fillcolor": "lightgreen"},
        )

        current = artist_list.head
        previous = None

        while current:
            data = current.data
            label = (
                f"ID: {data['id']}\\n"
                f"Name: {data['full_name']}\\n"
                f"Email: {data['email']}\\n"
                f"Phone: {data['phone']}\\n"
                f"Specialties: {data['specialties']}\\n"
                f"Notes: {data['additional_notes']}"
            )

            dot.node(data["id"], label)

            if previous:
                dot.edge(previous.data["id"], data["id"], constraint="true")

            previous = current
            current = current.next

        dot.render(format="svg")
        print("Artist report generated at ./Reports/ArtistList.svg")
