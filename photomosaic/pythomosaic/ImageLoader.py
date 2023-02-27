import cv2
import numpy as np
import glob

from .Element import Element


class ImageLoader:

    def __init__(self) -> None:
        self.elements = []

    def load_tileset_image(self, tileset_path: str, tile_size: int) -> None:
        """
        Load a tileset image and split it into tiles before converting them to elements
        :param tileset_path: the path of the tileset image
        :param tile_size: the size of the tiles
        :return: None
        """
        self.elements = []

        tileset_img = cv2.imread(tileset_path, cv2.IMREAD_UNCHANGED)
        tileset_img = cv2.cvtColor(tileset_img, cv2.COLOR_BGR2BGRA)

        for row in range(0, tileset_img.shape[0], tile_size):
            for col in range(0, tileset_img.shape[1], tile_size):
                image = tileset_img[row:row + tile_size, col:col + tile_size]

                self.elements.append(self.image_to_element(image))

    def load_folder_images(self, path: str) -> None:
        """
        Load all images from a folder and convert them to elements
        :param path: the path of the folder
        :return: None
        """
        self.elements = []

        files_path = glob.glob(path + '*[.jpg, .png, .jpeg]')

        for file_path in files_path:
            image = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)

            self.elements.append(self.image_to_element(image))

    def image_to_element(self, image: np.ndarray) -> Element:
        """
        Convert an image to an element
        :param image: the image
        :return: the element
        """
        return Element(image, image.shape)
