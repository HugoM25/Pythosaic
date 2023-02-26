from Bucket import Bucket
from Element import Element
from Utils import euclidean_distance
from CONST import *
import cv2
import numpy as np


class Maker:
    def __init__(self) -> None:
        self.buckets = []

    def empty_buckets(self):
        self.buckets = []

    def elements_to_buckets(self, elements):
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

    # def image_to_mosaic(self, image):

    #     bucket_colors = np.array(
    #         [bucket.average_color for bucket in self.buckets])

    #     height, width, _ = image.shape
    #     image_reshaped = image.reshape((height * width, 3))

    #     image_norms = np.sqrt(np.sum(image_reshaped**2, axis=1))
    #     bucket_norms = np.sqrt(np.sum(bucket_colors**2, axis=1))
    #     image_normed = image_reshaped / image_norms[:, np.newaxis]
    #     bucket_normed = bucket_colors / bucket_norms[:, np.newaxis]

    #     cos_sim = np.dot(image_normed, bucket_normed.transpose())
    #     closest_bucket_indices = np.argmax(cos_sim, axis=1)

    #     return closest_bucket_indices.reshape((height, width))

    def build_construction_matrix(self, image):

        # get the average color of each bucket
        bucket_colors = np.array(
            [bucket.average_color for bucket in self.buckets])

        # calculate the distance between each bucket color and each pixel in the image
        dist_result = np.sqrt(
            ((bucket_colors[:, np.newaxis, np.newaxis, :] - image) ** 2).sum(axis=3))

        # get the index of the minimum distance for each pixel
        closest_bucket_indices = np.argmin(dist_result, axis=0)

        return closest_bucket_indices.reshape((image.shape[0], image.shape[1]))

    # def build_construction_matrix(self, image):
    #     maxtrix = np.zeros((image.shape[0], image.shape[1]), dtype=np.uint8)
    #     for i in range(image.shape[0]):
    #         for j in range(image.shape[1]):
    #             min_dist = 10000
    #             bucket_target = None
    #             for bucket in self.buckets:
    #                 dist = euclidean_distance(
    #                     bucket.average_color,
    #                     image[i, j]
    #                 )
    #                 if dist < min_dist:
    #                     bucket_target = bucket
    #                     min_dist = dist
    #             maxtrix[i, j] = self.buckets.index(bucket_target)
    #     return maxtrix

    def build_img_from_matrix(self, matrix, buckets, size_img):
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

    # def make(self, image):
    #     matrix = self.image_to_mosaic(image)
    #     img_result = self.build_img_from_matrix(
    #         matrix, self.buckets, (30, 30))
    #     return img_result

    def make(self, image):
        matrix = self.build_construction_matrix(image)
        img_result = self.build_img_from_matrix(
            matrix, self.buckets, (30, 30))
        return img_result
