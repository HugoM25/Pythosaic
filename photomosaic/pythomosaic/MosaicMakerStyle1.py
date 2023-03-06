from __future__ import annotations
import cv2
import numpy as np
from .ImageLoader import ImageLoader
from .BucketsHandler import BucketsHandler


class MosaicMakerStyle1:
    def __init__(self, image_loader: ImageLoader, bucket_pick_method: str = "random") -> None:
        self.image_loader = image_loader
        # Load elements in buckets
        self.buckets_handler = BucketsHandler()
        self.buckets_handler.elements_to_buckets(self.image_loader.elements)

        self.bucket_pick_method = bucket_pick_method

    def build_construction_matrix(self, image: np.ndarray) -> np.ndarray:
        """
        Build the construction matrix
        :param image: the image to build the matrix from
        :return: the construction matrix
        """
        # get the average color of each bucket
        bucket_colors = np.array(
            [bucket.average_color for bucket in self.buckets_handler.buckets])

        # calculate the distance between each bucket color and each pixel in the image
        dist_result = np.sqrt(
            ((bucket_colors[:, np.newaxis, np.newaxis, :] - image) ** 2).sum(axis=3))

        # get the index of the minimum distance for each pixel
        closest_bucket_indices = np.argmin(dist_result, axis=0)

        # reshape the matrix to the size of the image
        matrix = closest_bucket_indices.reshape(
            (image.shape[0], image.shape[1]))

        # if the pixel is transparent, we set the value to -1
        # activate this line if you want to keep the transparency
        matrix = np.where(image[:, :, 3] == 0, -1, matrix)

        return matrix

    def build_img_from_matrix(self, matrix: np.ndarray, image: np.ndarray, size_img: tuple) -> np.ndarray:
        """
        Build the final image from the construction matrix
        :param matrix: the construction matrix
        :param buckets: the list of buckets
        :param size_img: the size of the image
        :return: the final image
        """
        # Calculating the size of the final image
        height, width = matrix.shape
        height_final = height * size_img[0]
        width_final = width * size_img[1]

        final_image_result = np.zeros(
            (height_final, width_final, 4), dtype=np.uint8)

        # Building the final image
        for i in range(height):
            for j in range(width):
                # If the pixel is transparent, we skip it
                if matrix[i, j] == -1:
                    continue
                bucket = self.buckets_handler.buckets[matrix[i, j]]
                element = bucket.get_element(
                    method="random", color=image[i, j])
                final_image_result[i*size_img[0]:(i+1)*size_img[0],
                                   j*size_img[1]:(j+1)*size_img[1], :] = cv2.resize(element.image, size_img)
        return final_image_result

    def make(self, image: np.ndarray) -> np.ndarray:
        """
        Make the photomosaic
        :param image: the image to make the photomosaic from
        :return: the final image
        """
        matrix = self.build_construction_matrix(image)
        img_result = self.build_img_from_matrix(
            matrix,
            image,
            (30, 30)
        )
        return img_result
