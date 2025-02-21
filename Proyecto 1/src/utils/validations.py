import re


class Validator:
    @staticmethod
    def validate_email(email):
        pattern = r"^[a-zA-Z0-9._%+-áéíóúÁÉÍÓÚñÑ]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, email) is not None

    @staticmethod
    def validate_phone(phone):
        return len(str(phone)) == 8 or 9 and str(phone).isdigit()

    @staticmethod
    def validate_requester_id(requester_id, requester_list):
        pattern = r"^IPC-\d+$"
        if not re.match(pattern, requester_id):
            return False

        for requester in requester_list:
            if requester.requester_id == requester_id:
                return False

        return True

    @staticmethod
    def validate_artist_id(artist_id, artist_list):
        pattern = r"^ART-\d+$"
        if not re.match(pattern, artist_id):
            return False

        for artist in artist_list:
            if artist.artist_id == artist_id:
                return False

        return True
