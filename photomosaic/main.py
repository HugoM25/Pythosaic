import pythomosaic as pm

import cv2
import glob
import time
import numpy as np


def style1():
    time_process = time.time()

    # Load data
    loader = pm.ImageLoader()
    # loader.load_tileset_image('assets/dataset_emoji.png', 66)
    loader.load_folder_images('assets/Cats/')

    print('Loading time: ', time.time() - time_process)

    # Prepare data
    time_process = time.time()
    maker = pm.Maker(loader)

    print('Prepare time : ', time.time() - time_process)

    # Load image to mosaic
    image = cv2.imread('target/logo.png', cv2.IMREAD_UNCHANGED)
    image = cv2.resize(image, (30, 30))

    time_process = time.time()

    # Mosaic image
    image = maker.make(image)

    print('Time process: ', time.time() - time_process)

    # Save the result
    cv2.imwrite('result/result.png', image)


def style2():
    # Load the image
    image = cv2.imread("target/A-Cat.jpg", cv2.IMREAD_UNCHANGED)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
    image = cv2.resize(image, (1000, 1000))

    # Load data
    loader = pm.ImageLoader()
    loader.load_folder_images('assets/Cats/')
    # loader.load_tileset_image('assets/dataset_pokemon.png', 80)
    # Prepare data
    maker = pm.MakerStyle2(loader)

    time_process = time.time()
    # Mosaic image
    processed_img = maker.make(image)

    print('Time process: ', time.time() - time_process)

    # Save the result
    cv2.imwrite('result/result_test.png', processed_img)


if __name__ == "__main__":

    style2()
