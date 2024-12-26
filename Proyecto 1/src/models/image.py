class Image:
    def __init__(self, id, name, image_path):
        self.id = id
        self.name = name
        self.image_path = image_path

    def __str__(self):
        return (
            f"ID: {self.id}\\n"
            f"Name: {self.name}\\n"
            f"Image Path: {self.image_path}\\n"
        )
