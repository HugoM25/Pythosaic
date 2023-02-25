from Element import Element
from Bucket import Bucket
from Maker import Maker
import cv2
import glob
import time

import numpy as np


def load_images(path):
    images = []

    files_path = glob.glob(path + '*[.jpg, .png, .jpeg]')

    for file_path in files_path:
        image = cv2.imread(file_path)
        images.append(image)

    return images


def images_to_elements(images):
    elements = []

    for image in images:
        color = cv2.mean(image)
        size = image.shape
        element = Element(image, color, size)
        elements.append(element)

    return elements


if __name__ == "__main__":
    # Load data
    images = load_images('assets/')
    elements = images_to_elements(images)

    # Prepare data
    maker = Maker()
    maker.elements_to_buckets(elements)

    # Load image to mosaic
    image = cv2.imread('target/bulb.png')
    image = cv2.resize(image, (50, 50))
    time_process = time.time()

    # Mosaic image
    image = maker.make(image)

    print('Time process: ', time.time() - time_process)

    # Show the result
    cv2.imshow('image', image)
    cv2.waitKey(0)

    # Save the result
    cv2.imwrite('result/result.png', image)
