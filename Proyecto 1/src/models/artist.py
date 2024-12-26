from models.circular_linked_list import CircularLinkedList


class Artist:
    def __init__(
        self, artist_id, pwd, full_name, email, phone, specialties, additional_notes
    ):
        self.artist_id = artist_id
        self.pwd = pwd
        self.full_name = full_name
        self.email = email
        self.phone = phone
        self.specialties = specialties
        self.additional_notes = additional_notes
        self.processed_images = CircularLinkedList()

    def insert_processed_image(self, value):
        self.processed_images.insert(value)
