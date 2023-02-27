import pythomosaic as pm

import cv2
import glob
import time
import numpy as np

if __name__ == "__main__":
    # Load data
    loader = pm.ImageLoader()
    # loader.load_tileset_image('assets/dataset_pokemon.png', 80)
    loader.load_folder_images('assets/blocks/')
    # Prepare data
    maker = pm.Maker(loader)

    # Load image to mosaic
    image = cv2.imread('target/squirtle.png')
    image = cv2.resize(image, (50, 50))

    time_process = time.time()

    # Mosaic image
    image = maker.make(image)

    print('Time process: ', time.time() - time_process)

    # Save the result
    cv2.imwrite('result/result.png', image)
