import numpy as np


class Element:
    def __init__(self, image: np, size) -> None:
        self.image = image
        self.color = self.compute_mean_color(image)
        self.size = size
        self.use_count = 0

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
            return (0, 0, 0)

        color = np.mean(image_masked, axis=0)
        return tuple(color[:3])

    def __str__(self) -> str:
        return "Element: " + str(self.color) + " " + str(self.size)

    def __repr__(self) -> str:
        return str(self)
