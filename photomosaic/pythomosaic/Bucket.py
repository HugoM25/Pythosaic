from __future__ import annotations
import random
from . import utils
from . import Element


class Bucket:
    def __init__(self, elements=[]):
        self.elements = elements
        self.average_color = self.calculate_average_color()

    def reset_count(self) -> None:
        """
        Reset the use count of all the elements in the bucket
        """
        for element in self.elements:
            element.use_count = 0

    def calculate_average_color(self) -> tuple:
        """
        Calculate the average color of the elements in the bucket
        :return: the average color
        """
        if len(self.elements) == 0:
            return (0, 0, 0, 1)

        average_color = [0, 0, 0, 1]
        for element in self.elements:
            average_color[0] += element.color[0]
            average_color[1] += element.color[1]
            average_color[2] += element.color[2]

        average_color[0] /= len(self.elements)
        average_color[1] /= len(self.elements)
        average_color[2] /= len(self.elements)

        return average_color

    def add_element(self, element: Element) -> None:
        """
        Add an element to the bucket and update the average color
        :param element: the element to add
        """
        self.elements.append(element)
        self.average_color = self.calculate_average_color()

    def get_element(self, method: str = "random", color: tuple = None) -> Element:
        """
        Get an element from the bucket
        :param method: "random", "least_used", "closest"
        :param color: the color to compare to
        :return: an element
        """
        if method == "least_used":
            return self.get_least_used_element()
        elif method == "closest" and color is not None:
            return self.get_closest_element(color)
        else:
            return self.get_random_element()

    def get_random_element(self) -> Element:
        """
        Get a random element from the bucket
        :return: an element
        """
        return random.choice(self.elements)

    def get_least_used_element(self) -> Element:
        """
        Get the element that has been used the least and update its use count
        :return: an element
        """
        element = min(self.elements, key=lambda x: x.use_count)
        element.use_count += 1
        return element

    def get_closest_element(self, color: tuple) -> Element:
        """
        Get the element that is closest to the given color
        :param color: the color to compare to
        :return: an element
        """
        return min(self.elements, key=lambda x: utils.euclidean_distance(x.color, color))

    def __str__(self) -> str:
        return "Bucket: " + str(self.average_color) + " " + str(len(self.elements))

    def __repr__(self) -> str:
        return str(self)
