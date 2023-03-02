import pythomosaic as pm

import cv2
import glob
import time
import numpy as np

if __name__ == "__main__":

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
