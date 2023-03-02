import numpy as np
import cv2
# Description: PostProcess class used to post process the mosaic image after building it


class PostProcess:
    def __init__(self) -> None:
        pass

    def overlay_model_mosaic(self, image_model, image_mosaic) -> np.ndarray:
        """
        Overlay the model image on the mosaic image to get better colors
        :param image_model: the model image
        :param image_mosaic: the mosaic image
        :return: the final image
        """
        final_image = None
        return final_image

    def blend_normal(self):
        pass
