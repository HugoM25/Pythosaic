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
        image = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)

        images.append(image)

    return images


def load_images_from_tileset(tileset_path, tile_size):
    images = []

    tileset_img = cv2.imread(tileset_path, cv2.IMREAD_UNCHANGED)
    tileset_img = cv2.cvtColor(tileset_img, cv2.COLOR_BGR2BGRA)

    for row in range(0, tileset_img.shape[0], tile_size):
        for col in range(0, tileset_img.shape[1], tile_size):
            image = tileset_img[row:row + tile_size, col:col + tile_size]
            images.append(image)

    return images


def images_to_elements(images):
    elements = []
    i = 0
    for image in images:
        size = image.shape
        element = Element(image, size)
        elements.append(element)
        i += 1

    return elements


def image_from_bucket(bucket, size_pics):
    final_size = (size_pics[0] * len(bucket.elements), size_pics[1])
    image = np.zeros((final_size[0], final_size[1], 4), dtype=np.uint8)
    for i in range(len(bucket.elements)):
        tmp_img = cv2.resize(bucket.elements[i].image, size_pics)
        image[i * size_pics[0]:(i + 1) * size_pics[0],
              :] = tmp_img
        # Draw a rectangle of the average color
        color_tmp = (
            int(bucket.elements[i].color[0]), int(bucket.elements[i].color[1]), int(bucket.elements[i].color[2]))
        cv2.rectangle(image, (0, i * size_pics[0]), (size_pics[1],
                      (i + 1) * size_pics[0]), color_tmp, 5)

    return image


if __name__ == "__main__":
    # Load data
    images = load_images_from_tileset('assets/dataset_pokemon.png', 80)
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
