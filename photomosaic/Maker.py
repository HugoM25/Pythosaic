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

            if len(self.buckets) == 0:
                bucket = Bucket([element])
                self.buckets.append(bucket)
                continue
            else:
                for bucket in self.buckets:
                    if euclidean_distance(bucket.average_color, element.color) < DIST_MAX_COLOR_BUCKET:
                        bucket.add_element(element)
                        break
                    else:
                        bucket = Bucket([element])
                        self.buckets.append(bucket)
                        break

    def image_to_mosaic(self, image):

        bucket_colors = np.array(
            [bucket.average_color for bucket in self.buckets])

        height, width, _ = image.shape
        image_reshaped = image.reshape((height * width, 3))

        image_norms = np.sqrt(np.sum(image_reshaped**2, axis=1))
        bucket_norms = np.sqrt(np.sum(bucket_colors**2, axis=1))
        image_normed = image_reshaped / image_norms[:, np.newaxis]
        bucket_normed = bucket_colors / bucket_norms[:, np.newaxis]

        cos_sim = np.dot(image_normed, bucket_normed.transpose())
        closest_bucket_indices = np.argmax(cos_sim, axis=1)

        return closest_bucket_indices.reshape((height, width))

    def build_img_from_matrix(self, matrix, buckets, size_img):
        final_image_result = None

        for index_row, row in enumerate(matrix):
            row_image_result = None
            for index_col, element in enumerate(row):

                if index_col == 0:
                    img_to_add = buckets[element].elements[0].image
                    img_to_add = cv2.resize(
                        img_to_add, (size_img[1], size_img[0]))
                    row_image_result = img_to_add
                else:
                    img_to_add = buckets[element].elements[0].image
                    img_to_add = cv2.resize(
                        img_to_add, (size_img[1], size_img[0]))
                    row_image_result = cv2.hconcat(
                        [row_image_result, img_to_add])

            if index_row == 0:
                final_image_result = row_image_result
            else:
                final_image_result = cv2.vconcat(
                    [final_image_result, row_image_result])

        return final_image_result

    def make(self, image):
        matrix = self.image_to_mosaic(image)
        img_result = self.build_img_from_matrix(
            matrix, self.buckets, (30, 30))
        return img_result
