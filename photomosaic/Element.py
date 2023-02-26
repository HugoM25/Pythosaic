import time
import numpy as np
import cv2


class Element:
    def __init__(self, image, size):
        self.image = image
        self.color = self.compute_mean_color(image)
        self.size = size

    def compute_mean_color(self, image):

        mask = image[:, :, 3] != 0
        image_masked = image[mask]

        # Check if image_masked is empty
        if image_masked.size == 0:
            return [0, 0, 0]

        color = np.mean(image_masked, axis=0)
        return color[:3]

    def __str__(self):
        return "Element: " + str(self.color) + " " + str(self.size)

    def __repr__(self):
        return str(self)
