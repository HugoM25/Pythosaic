import numpy as np
import cv2

from .ImageLoader import ImageLoader
from .BucketsHandler import BucketsHandler


MIN_TILE_SIZE = 100
MIN_VARIATION = 5
TILE_NB = 10

MIN_DEVIANCE = 10
MAX_SPLIT = 2


class MakerStyle2:
    def __init__(self, image_loader: ImageLoader, bucket_pick_method: str = "random") -> None:
        self.image_loader = image_loader
        # Load elements in buckets
        self.buckets_handler = BucketsHandler()
        self.buckets_handler.elements_to_buckets(self.image_loader.elements)
        self.bucket_pick_method = bucket_pick_method

    def make(self, image: np.ndarray):
        # Split the image in n squares
        n = TILE_NB
        height, width, _ = image.shape
        height_square = height//n
        width_square = width//n

        # Apply the recursive part fill on each square
        for i in range(n):
            for j in range(n):
                image[i*height_square:(i+1)*height_square, j*width_square:(j+1)*width_square] = self.recursive_part_fill(
                    image[i*height_square:(i+1)*height_square, j*width_square:(j+1)*width_square])

        return image

    def compute_mean_color(self, image: np.ndarray) -> tuple:
        """
        Compute the mean color of an image
        :param image: the image
        :return: the mean color
        """
        mask = image[:, :, 3] != 0
        image_masked = image[mask]

        # Check if image_masked is empty
        if image_masked.size == 0:
            return (0, 0, 0, 0)

        color = np.mean(image_masked, axis=0)
        return tuple(color)

    def compute_standard_deviation_val(self, pixel_array: np.ndarray) -> float:
        """
        Compute the standard deviation of the color of an image
        :param image: the image
        :return: the standard deviation of the color
        """
        mask = pixel_array[:, :, 3] != 0

        image_masked = pixel_array[mask]

        # Check if image_masked is empty
        if image_masked.shape[0] == 0:
            return -1

        color = np.std(image_masked, axis=0)
        deviance = np.mean(color)

        return deviance

    def is_there_too_much_transparent(self, image_part: np.ndarray) -> bool:
        """
        Check if there is too much transparent pixels in an image
        :param image_part: the image
        :return: True if there is too much transparent pixels, False otherwise
        """
        # Calculate the proportion of non fully transparent pixels
        mask = image_part[:, :, 3] != 0
        image_masked = image_part[mask]

        # Check if image_masked is empty
        if image_masked.shape[0] == 0:
            return False

        proportion = image_masked.shape[0] / \
            (image_part.shape[0]*image_part.shape[1])

        # If the proportion is too low, we split the image
        if proportion < 0.5:
            return True
        else:
            return False

    def recursive_part_fill(self, image_part, depth=0):
        height, width, _ = image_part.shape

        deviation_image = self.compute_standard_deviation_val(image_part)
        is_mostly_transparent = self.is_there_too_much_transparent(image_part)

        if depth >= MAX_SPLIT or (deviation_image < MIN_DEVIANCE and is_mostly_transparent == False):
            # Find the closest bucket to the color of the image part
            needed_color = self.compute_mean_color(image_part)

            # Add theses lines to keep the background transparent
            if needed_color[3] < 1:
                return np.array([[[0, 0, 0, 0]]*width]*height)

            # Calculate the dist of every buckets to the color of the image part
            dists = np.sum(
                np.square(self.buckets_handler.buckets_average_colors - needed_color), axis=1)
            # Get the index of the closest bucket
            closest_bucket_index = np.argmin(dists)
            # Get the closest bucket
            closest_bucket = self.buckets_handler.buckets[closest_bucket_index]
            # Get a random element from the closest bucket
            image = closest_bucket.get_element(
                method="random", color=needed_color).image

            return cv2.resize(image, (width, height))
        else:
            for i in range(2):
                for j in range(2):
                    image_part[i*height//2:(i+1)*height//2, j*width//2:(j+1)*width//2] = self.recursive_part_fill(
                        image_part[i*height//2:(i+1)*height//2, j*width//2:(j+1)*width//2], depth=depth+1)
        return image_part
