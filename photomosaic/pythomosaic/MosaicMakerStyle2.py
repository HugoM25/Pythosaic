import numpy as np
import cv2

from .ImageLoader import ImageLoader
from .BucketsHandler import BucketsHandler


MIN_TILE_SIZE = 10
MIN_VARIATION = 20000000
TILE_NB = 16


class MakerStyle2:
    def __init__(self, image_loader: ImageLoader, bucket_pick_method: str = "random") -> None:
        self.image_loader = image_loader
        # Load elements in buckets
        self.buckets_handler = BucketsHandler()
        self.buckets_handler.elements_to_buckets(self.image_loader.elements)
        self.bucket_pick_method = bucket_pick_method

    def calculate_variation(self, pixel_array: np.ndarray) -> float:
        """
        Calculate the variation of a pixel array
        :param pixel_array: The pixel array
        :return: The variation
        """
        # Calculate the average pixel value
        average_pixel = np.average(pixel_array)

        # Calculate the variation
        variation = np.sum(np.square(pixel_array - average_pixel))

        return variation

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

    def recursive_part_fill(self, image_part):
        height, width, _ = image_part.shape
        if height < MIN_TILE_SIZE or self.calculate_variation(image_part) < MIN_VARIATION:
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
                        image_part[i*height//2:(i+1)*height//2, j*width//2:(j+1)*width//2])
        return image_part
