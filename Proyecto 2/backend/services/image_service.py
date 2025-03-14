import os
from xml.etree import ElementTree as ET
from xml.dom import minidom
from xml.sax.saxutils import escape
from models.image import Image  # Import the Image model
from models.pixel import Pixel  # Import the Pixel model
from models.sparse_matrix import SparseMatrix  # Import the SparseMatrix model
from utils.color_utils import (
    hex_to_rgb,
    rgb_to_hex,
)  # Import the color conversion functions


class ImageService:
    """
    Service for managing images stored in an XML file.

    Attributes:
        storage_path (str): Path to the directory where the XML file is stored.
        images_file (str): Path to the images XML file.
    """

    def __init__(self):
        """
        Initializes the ImageService and ensures the XML file exists.
        """
        self.storage_path = os.path.abspath("database")
        self.images_file = os.path.join(self.storage_path, "imagenes.xml")
        self.base64_file = os.path.join(self.storage_path, "imagenes_base64.xml")

        # Create storage directory if it doesn't exist
        os.makedirs(self.storage_path, exist_ok=True)

        # Initialize XML file if it doesn't exist
        self._initialize_images_file()
        self._initialize_base64_file()

    def _initialize_images_file(self):
        """
        Initializes the images XML file if it does not already exist.
        """
        if not os.path.exists(self.images_file):
            root = ET.Element("imagenes")
            tree = ET.ElementTree(root)
            self._write_pretty_xml(tree, self.images_file)

    def _initialize_base64_file(self):
        """
        Initializes the base64 XML file if it does not already exist.
        """
        if not os.path.exists(self.base64_file):
            root = ET.Element("imagenes_base64")
            tree = ET.ElementTree(root)
            self._write_pretty_xml(tree, self.base64_file)

    def _write_pretty_xml(self, tree, file_path):
        """Write XML with compact formatting"""
        try:

            def _indent(elem, level=0):
                i = "\n" + level * "  "
                if len(elem):
                    if not elem.text or not elem.text.strip():
                        elem.text = i + "  "
                    if not elem.tail or not elem.tail.strip():
                        elem.tail = i
                    for subelem in elem:
                        _indent(subelem, level + 1)
                    if not elem.tail or not elem.tail.strip():
                        elem.tail = i
                else:
                    if level and (not elem.tail or not elem.tail.strip()):
                        elem.tail = i

            root = tree.getroot()
            _indent(root)
            tree.write(file_path, encoding="utf-8", xml_declaration=True)
        except Exception as e:
            raise Exception(f"Error writing XML: {str(e)}")

    def _image_exists(self, image_id, root):
        """
        Checks if an image with the given ID already exists.

        Args:
            image_id (str): ID of the image to check.
            root (Element): Root element of the XML tree.

        Returns:
            bool: True if the image exists, False otherwise.
        """
        return root.find(f"./imagen[@id='{image_id}']") is not None

    def _generate_next_id(self):
        """
        Genera el siguiente ID incremental en formato de cuatro dígitos.

        Returns:
            str: El nuevo ID en formato '0001', '0002', etc.
        """
        try:
            tree = ET.parse(self.images_file)
            root = tree.getroot()

            # Obtener todos los IDs existentes
            ids = [int(image_elem.get("id")) for image_elem in root.findall("imagen")]
            next_id = max(ids) + 1 if ids else 1

            # Retornar el ID en formato de cuatro dígitos
            return f"{next_id:04d}"
        except Exception as e:
            raise Exception(f"Error generating next ID: {e}")

    def save_base64(self, image_id, base64_data, user_id, edited=False):
        """
        Saves the base64 representation of an image in a separate XML file.

        Args:
            image_id (str): The ID of the image.
            base64_data (str): The base64 representation of the image.
            user_id (str): The user ID associated with the image.
            edited (bool): False if the image is original, True if edited.
        """
        try:
            tree = ET.parse(self.base64_file)
            root = tree.getroot()

            # Check if base64 for the image already exists
            base64_elem = root.find(f"./imagen[@id='{image_id}']")
            if base64_elem is not None:
                base64_elem.text = escape(base64_data)  # Update if it exists
                base64_elem.set("id_usuario", escape(user_id))  # Update user ID
                base64_elem.set(
                    "editado", "1" if edited else "0"
                )  # Update edited status
            else:
                # Add a new base64 entry
                ET.SubElement(
                    root,
                    "imagen",
                    {
                        "id": escape(image_id),
                        "id_usuario": escape(user_id),
                        "editado": "1" if edited else "0",
                    },
                ).text = escape(base64_data)

            self._write_pretty_xml(tree, self.base64_file)
        except Exception as e:
            raise Exception(f"Error saving base64 data: {e}")

    def add_image(self, image):
        """
        Adds a new image to the XML file.

        Args:
            image (Image): Image object to add.

        Returns:
            bool: True if the image was added, False if an image with the same ID already exists.
        """
        try:
            tree = ET.parse(self.images_file)
            root = tree.getroot()

            if not image.id:
                image.id = self._generate_next_id()

            if self._image_exists(image.id, root):
                return False

            image_elem = ET.SubElement(
                root,
                "imagen",
                {
                    "id": escape(image.id),
                    "id_usuario": escape(image.user_id),
                    "editado": "0",
                },
            )
            ET.SubElement(image_elem, "nombre").text = escape(image.name)

            # Add the design (pixels)
            design_elem = ET.SubElement(image_elem, "diseño")
            sparse_matrix = SparseMatrix()  # Create a SparseMatrix object
            for pixel in image.pixels:
                ET.SubElement(
                    design_elem,
                    "pixel",
                    {"fila": str(pixel.row), "col": str(pixel.column)},
                ).text = escape(pixel.color)

                sparse_matrix.insert(
                    pixel.row, pixel.column, pixel.color
                )  # Insert the pixel into the sparse matrix

            graph_base64 = sparse_matrix.plot()  # Convert the sparse matrix to base64

            self.save_base64(
                image.id, graph_base64, image.user_id
            )  # Save the base64 data

            self._write_pretty_xml(
                tree, self.images_file
            )  # Save the changes to the XML file
            return {"success": True, "image_id": image.id, "graph": graph_base64}

        except Exception as e:
            raise Exception(f"Error adding image: {e}")

    def get_base64(self, image_id):
        """
        Retrieves the base64 representation of an image by its ID.

        Args:
            image_id (str): The ID of the image.

        Returns:
            str: The base64 representation of the image.
        """
        try:
            tree = ET.parse(self.base64_file)
            root = tree.getroot()

            base64_elem = root.find(f"./imagen[@id='{image_id}']")
            if base64_elem is None or not base64_elem.text:
                raise ValueError("Base64 representation not found for the image.")

            return base64_elem.text
        except Exception as e:
            raise Exception(f"Error retrieving base64 data: {e}")

    def get_all_gallery_images(self):
        """
        Retrieves the images metadata required for the gallery by user ID.

        Args:
            user_id (str): The ID of the user.

        Returns:
            list[dict]: A list of dictionaries containing image metadata.
        """
        try:
            tree = ET.parse(self.base64_file)
            root = tree.getroot()

            gallery_images = []
            for image_elem in root.findall("imagen"):
                gallery_images.append(
                    {
                        "id": image_elem.get("id"),
                        "id_usuario": image_elem.get("id_usuario"),
                        "editado": image_elem.get("editado"),
                        "base64": image_elem.text,
                    }
                )

            return gallery_images
        except Exception as e:
            raise Exception(f"Error retrieving gallery images: {e}")

    def get_all_images(self):
        """
        Retrieves all images from the XML file.

        Returns:
            list[Image]: List of Image objects.
        """
        try:
            tree = ET.parse(self.images_file)
            root = tree.getroot()

            images = []
            for image_elem in root.findall("imagen"):
                # Parse pixels
                pixels = []
                for pixel_elem in image_elem.find("diseño").findall("pixel"):
                    pixel = Pixel(
                        row=int(pixel_elem.get("fila")),
                        column=int(pixel_elem.get("col")),
                        color=pixel_elem.text,
                    )
                    pixels.append(pixel)

                # Create Image object
                image = Image(
                    id=image_elem.get("id"),
                    user_id=image_elem.get("id_usuario"),
                    name=image_elem.find("nombre").text or "",
                    pixels=pixels,
                )
                image.edited = image_elem.get("editado") == "1"
                images.append(image)

            return images

        except Exception as e:
            raise Exception(f"Error retrieving images: {e}")

    def get_images_by_user_id(self, user_id):
        """
        Retrieves all images associated with a specific user ID.

        Args:
            user_id (str): ID of the user to retrieve images for.

        Returns:
            list[Image]: List of Image objects associated with the user ID.
        """
        try:
            tree = ET.parse(self.images_file)
            root = tree.getroot()

            images = []
            for image_elem in root.findall(f"./imagen[@id_usuario='{user_id}']"):
                pixels = [
                    Pixel(
                        row=int(pixel_elem.get("fila")),
                        column=int(pixel_elem.get("col")),
                        color=pixel_elem.text,
                    )
                    for pixel_elem in image_elem.find("diseño").findall("pixel")
                ]

                image = Image(
                    id=image_elem.get("id"),
                    user_id=image_elem.get("id_usuario"),
                    name=image_elem.find("nombre").text or "",
                    pixels=pixels,
                )
                image.edited = image_elem.get("editado") == "1"
                images.append(image)

            return images

        except Exception as e:
            raise Exception(f"Error retrieving images for user ID {user_id}: {e}")

    def apply_grayscale(self, image):
        """
        Applies a grayscale filter to an image.

        Args:
            image (Image): The original image.

        Returns:
            Image: The image transformed to grayscale.
        """
        transformed_pixels = []
        for pixel in image.pixels:
            r, g, b = hex_to_rgb(pixel.color)  # Convert HEX to RGB
            gray = int(
                0.2989 * r + 0.5870 * g + 0.1140 * b
            )  # Calculate grayscale value
            gray_hex = rgb_to_hex(gray, gray, gray)  # Convert grayscale back to HEX
            transformed_pixels.append(
                Pixel(row=pixel.row, column=pixel.column, color=gray_hex)
            )

        transformed_image = Image(
            id=None,  # The new ID will be assigned later
            user_id=image.user_id,
            name=f"{image.name}_grayscale",
            pixels=transformed_pixels,
        )
        return transformed_image

    def apply_sepia(self, image):
        """
        Applies a sepia filter to an image.

        Args:
            image (Image): The original image.

        Returns:
            Image: The image transformed to sepia.
        """
        transformed_pixels = []
        for pixel in image.pixels:
            r, g, b = hex_to_rgb(pixel.color)  # Convert HEX to RGB

            # Apply sepia formulas
            new_r = min(int(0.393 * r + 0.769 * g + 0.189 * b), 255)
            new_g = min(int(0.349 * r + 0.686 * g + 0.168 * b), 255)
            new_b = min(int(0.272 * r + 0.534 * g + 0.131 * b), 255)

            sepia_hex = rgb_to_hex(
                new_r, new_g, new_b
            )  # Convert sepia result back to HEX
            transformed_pixels.append(
                Pixel(row=pixel.row, column=pixel.column, color=sepia_hex)
            )

        transformed_image = Image(
            id=None,  # The new ID will be assigned later
            user_id=image.user_id,
            name=f"{image.name}_sepia",
            pixels=transformed_pixels,
        )
        return transformed_image

    def apply_negative(self, image):
        """
        Applies a negative filter to an image.

        Args:
            image (Image): The original image.

        Returns:
            Image: The image transformed to negative.
        """
        transformed_pixels = []
        for pixel in image.pixels:
            r, g, b = hex_to_rgb(pixel.color)  # Convert HEX to RGB

            # Apply negative transformation
            neg_r = 255 - r
            neg_g = 255 - g
            neg_b = 255 - b

            negative_hex = rgb_to_hex(neg_r, neg_g, neg_b)  # Convert back to HEX
            transformed_pixels.append(
                Pixel(row=pixel.row, column=pixel.column, color=negative_hex)
            )

        transformed_image = Image(
            id=None,  # The new ID will be assigned later
            user_id=image.user_id,
            name=f"{image.name}_negative",
            pixels=transformed_pixels,
        )
        return transformed_image

    def transform_image(self, image_id, filter_type):
        """
        Transforms an existing image by applying a filter (grayscale or sepia) and saves it to the XML file.

        Args:
            image_id (str): The ID of the image to transform.
            filter_type (str): The type of filter ('grayscale' or 'sepia').

        Returns:
            dict: Contains the status, the new image ID, the original graph, and the transformed graphical representation.
        """
        try:
            # Load all images from the XML file
            images = self.get_all_images()

            # Find the original image
            original_image = next((img for img in images if img.id == image_id), None)
            if not original_image:
                raise ValueError("The image with the specified ID does not exist.")

            if original_image.edited:
                raise ValueError("The image has already been edited.")

            # Apply the corresponding filter
            if filter_type == "grayscale":
                transformed_image = self.apply_grayscale(original_image)
            elif filter_type == "sepia":
                transformed_image = self.apply_sepia(original_image)
            elif filter_type == "negative":
                transformed_image = self.apply_negative(original_image)
            else:
                raise ValueError("Unsupported filter type.")

            # Update the edited status and assign a new ID
            transformed_image.id = self._generate_next_id()
            transformed_image.edited = True

            # Generate the transformed graphical representation
            sparse_matrix = SparseMatrix()
            for pixel in transformed_image.pixels:
                sparse_matrix.insert(pixel.row, pixel.column, pixel.color)

            transformed_graph_base64 = sparse_matrix.plot()

            # Write the transformed image directly to the XML file
            tree = ET.parse(self.images_file)
            root = tree.getroot()

            image_elem = ET.SubElement(
                root,
                "imagen",
                {
                    "id": escape(transformed_image.id),
                    "id_usuario": escape(transformed_image.user_id),
                    "editado": "1",  # Transformed images are always edited
                },
            )
            ET.SubElement(image_elem, "nombre").text = escape(transformed_image.name)

            design_elem = ET.SubElement(image_elem, "diseño")
            for pixel in transformed_image.pixels:
                ET.SubElement(
                    design_elem,
                    "pixel",
                    {"fila": str(pixel.row), "col": str(pixel.column)},
                ).text = escape(pixel.color)

            # Save changes to the XML file
            self._write_pretty_xml(tree, self.images_file)

            # Save the transformed graph as base64
            self.save_base64(
                transformed_image.id,
                transformed_graph_base64,
                transformed_image.user_id,
                edited=True,
            )

            return {
                "success": True,
                "image_id": transformed_image.id,
                "transformed_graph": transformed_graph_base64,
            }

        except Exception as e:
            raise Exception(f"Error transforming image: {e}")

    def get_image_graph(self, image_id, edited=False):
        """
        Retrieves the base64 graphical representation of an image by its ID.

        Args:
            image_id (str): The ID of the image.
            edited (bool): If True, only return the original image (editado="0").

        Returns:
            str: The base64 graphical representation of the image.
        """
        try:
            tree = ET.parse(self.base64_file)
            root = tree.getroot()

            # Find the image element with the specified ID
            if edited:
                image_elem = root.find(f"./imagen[@id='{image_id}' and @editado='0']")
            else:
                image_elem = root.find(f"./imagen[@id='{image_id}']")

            if image_elem is None:
                raise ValueError(
                    "Image with the specified ID does not exist or does not match criteria."
                )

            return image_elem.text

        except Exception as e:
            raise Exception(f"Error retrieving the image graph: {e}")
