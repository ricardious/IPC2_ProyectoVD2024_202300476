class ImageRequest:
    def __init__(self, request_id, xml_path):
        """Constructor de la clase que inicializa una solicitud de imagen en el carrito."""
        self.request_id = request_id  # Identificador único de la solicitud de imagen
        self.xml_path = xml_path  # Ruta del archivo XML que define la solicitud

    def __str__(self):
        """Representación en forma de texto de la solicitud de imagen."""
        return (
            f"ID de la Solicitud: {self.request_id}\n"
            f"Ruta del XML: {self.xml_path}\n"
        )
