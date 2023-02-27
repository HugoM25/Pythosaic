from __future__ import annotations
from Bucket import Bucket
from Element import Element
from Utils import euclidean_distance
from CONST import *
import cv2
import numpy as np


class Maker:
    def __init__(self) -> None:
        self.buckets = []

    def empty_buckets(self) -> None:
        self.buckets = []

    def elements_to_buckets(self, elements: Element) -> None:
        """
        Sort the elements into buckets
        :param elements: the list of elements
        """
        for element in elements:
            # if the element is black only skip it
            if element.color[0] == 0 and element.color[1] == 0 and element.color[2] == 0:
                continue

            # if there are no buckets create one and add the element
            if len(self.buckets) == 0:
                bucket = Bucket([element])
                self.buckets.append(bucket)
                continue

            # if there are buckets find the closest one
            min_dist = 10000
            bucket_target = None

            for bucket in self.buckets:
                dist = euclidean_distance(
                    bucket.average_color,
                    element.color
                )
                if dist < min_dist:
                    bucket_target = bucket
                    min_dist = dist

            # check if the closest bucket is close enough to add the element else create a new bucket
            if min_dist < DIST_MAX_COLOR_BUCKET:
                bucket_target.add_element(element)
            else:
                bucket = Bucket([element])
                self.buckets.append(bucket)

    def build_construction_matrix(self, image: np.ndarray) -> np.ndarray:

        # get the average color of each bucket
        bucket_colors = np.array(
            [bucket.average_color for bucket in self.buckets])

        # calculate the distance between each bucket color and each pixel in the image
        dist_result = np.sqrt(
            ((bucket_colors[:, np.newaxis, np.newaxis, :] - image) ** 2).sum(axis=3))

        # get the index of the minimum distance for each pixel
        closest_bucket_indices = np.argmin(dist_result, axis=0)

        return closest_bucket_indices.reshape((image.shape[0], image.shape[1]))

    def build_img_from_matrix(self, matrix: np.ndarray, buckets: list[Bucket], size_img: tuple) -> np.ndarray:
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
                bucket = buckets[matrix[i, j]]
                element = bucket.get_random_element()
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
            matrix, self.buckets, (30, 30))
        return img_result
