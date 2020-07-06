"""
Programmer: Harim Kang
Description: Style Transfer Class
Reference: https://wikidocs.net/79287
Style transfer Model: https://tfhub.dev/google/lite-model/magenta/arbitrary-image-stylization-v1-256/fp16/transfer/1
"""

import tensorflow as tf
import cv2
import numpy as np
from PIL import Image


class StyleTransfer:
    # This class takes an image and converts it to a specified style.
    def __init__(self, width, height):
        self.model = None
        # current: This is an index to select a style belonging to style_img.
        self.current = 1

        # Style type.
        self.style_img = [
            Image.open("./style/gogh.jpg"),
            Image.open("./style/VK1913.jpg"),
            Image.open("./style/monet.jpg")
        ]
        self.WIDTH = width
        self.HEIGHT = height

    def load(self, use_hub=False):
        # Load the model by using tensor-flow_hub or using the local model.
        if use_hub:
            import tensorflow_hub as hub
            module_path = 'https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2'
            self.model = hub.load(module_path)
        else:
            self.model = tf.saved_model.load("./models/magenta_arbitrary-image-stylization-v1-256_2", tags=None)

    def change_style(self, i):
        # Change the index of style_img by changing the current variable.
        self.current = i

    def convert_style_img(self, image):
        # The image's pre-processing function.
        image = image.convert('RGB')
        image = image.resize((self.WIDTH, self.HEIGHT))
        image_numpy = np.array(image)
        image = np.array([image_numpy])
        return image

    def predict(self, frame):
        # Takes an image, converts it to the currently set style, and returns it.
        img = self.convert_style_img(self.style_img[self.current])
        img = image2constant(img)

        content_image = np.array([cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)])
        content_image = image2constant(content_image)

        y_predict = self.model.signatures['serving_default'](placeholder=content_image,
                                                             placeholder_1=img)['output_0'].numpy()
        image = cv2.cvtColor((y_predict[0] * 255).astype(np.uint8), cv2.COLOR_RGB2BGR)
        return image


def image2constant(image):
    # Convert an image to a tensor-flow constant.
    image = image / 255
    image = image.astype(dtype=np.float32)
    image = tf.constant(image)
    return image
