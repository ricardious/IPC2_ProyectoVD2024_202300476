class ImageQueueRequest:
    def __init__(self, request_id, xml_path, requester_id):
        """Constructor de la clase que inicializa una solicitud en la cola de artistas."""
        self.request_id = request_id  # Identificador único de la solicitud
        self.xml_path = xml_path  # Ruta del archivo XML que define la solicitud
        self.requester_id = (
            requester_id  # Identificador del solicitante que hizo la solicitud
        )

    def __str__(self):
        """Representación en forma de texto de la solicitud en la cola."""
        return (
            f"ID de la Solicitud: {self.request_id}\n"
            f"Ruta del XML: {self.xml_path}\n"
            f"ID del Solicitante: {self.requester_id}"
        )
