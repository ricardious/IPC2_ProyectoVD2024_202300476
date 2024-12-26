import xml.etree.ElementTree as ET
from utils.validations import Validator
from models.stack import Stack
from models.requester import Requester
from models.artist import Artist
from models.image_request import ImageRequest
from global_state import requester_list


class XMLParser:
    @staticmethod
    def load_requesters(xml_path, requester_list):
        try:
            tree = ET.parse(xml_path)
            root = tree.getroot()

            for requester in root.findall("solicitante"):
                requester_id = requester.get("id")
                pwd = requester.get("pwd")
                full_name = requester.find("NombreCompleto").text
                email = requester.find("CorreoElectronico").text
                phone = requester.find("NumeroTelefono").text
                address = requester.find("Direccion").text

                if (
                    Validator.validate_requester_id(requester_id, requester_list)
                    and Validator.validate_email(email)
                    and Validator.validate_phone(phone)
                ):
                    new_requester = Requester(
                        requester_id, pwd, full_name, email, phone, address
                    )
                    requester_list.insert(new_requester)
                else:
                    print(f"Invalid requester {requester_id}, skipping...")

        except ET.ParseError:
            print(f"Error parsing XML file: {xml_path}")

    @staticmethod
    def load_artists(xml_path, artist_list):
        try:
            tree = ET.parse(xml_path)
            root = tree.getroot()

            for artist in root.findall("Artista"):
                artist_id = artist.get("id")
                pwd = artist.get("pwd")
                full_name = artist.find("NombreCompleto").text
                email = artist.find("CorreoElectronico").text
                phone = artist.find("NumeroTelefono").text
                specialties = artist.find("Especialidades").text
                additional_notes = artist.find("NotasAdicionales").text

                if (
                    Validator.validate_artist_id(artist_id, artist_list)
                    and Validator.validate_email(email)
                    and Validator.validate_phone(phone)
                ):
                    new_artist = Artist(
                        artist_id,
                        pwd,
                        full_name,
                        email,
                        phone,
                        specialties,
                        additional_notes,
                    )
                    artist_list.insert(new_artist)
                else:
                    print(f"Invalid artist {artist_id}, skipping...")

        except ET.ParseError:
            print(f"Error parsing XML file: {xml_path}")

    @staticmethod
    def load_figures(xml_path, logged_in_user_id):
        try:
            tree = ET.parse(xml_path)
            root = tree.getroot()

            request_id = ""
            if root.tag == "figura":
                for elementos in root:
                    if elementos.tag == "nombre":
                        request_id = elementos.attrib["id"]

            new_request = ImageRequest(request_id, xml_path)
            requester_list.insert_to_user_stack(logged_in_user_id, new_request)

        except ET.ParseError:
            print(f"Error parsing XML file: {xml_path}")
