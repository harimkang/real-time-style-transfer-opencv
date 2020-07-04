# import tensorflow_hub as hub
import tensorflow as tf
import cv2
import numpy as np
from PIL import Image
import logging
import os


class StyleTransfer:
    def __init__(self, width, height):
        self.model = None
        self.style_img = Image.open("./style/VK1913.jpg")
        self.WIDTH = width
        self.HEIGHT = height

    def load(self):
        logging.info('===== Style Transfer Loading=====')
        # module_path = 'https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2'
        # self.model = hub.load(module_path)

        self.model = tf.saved_model.load("./models/magenta_arbitrary-image-stylization-v1-256_2", tags=None)
        logging.info('===== Style Transfer Loaded=====')

        self.style_img = self.convert_style_img(self.style_img)
        self.style_img = image2constant(self.style_img)

    def convert_style_img(self, image):
        image = image.convert('RGB')
        image = image.resize((self.WIDTH, self.HEIGHT))
        image_numpy = np.array(image)
        image = np.array([image_numpy])
        return image

    def predict(self, frame):
        content_image = np.array([cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)])
        content_image = image2constant(content_image)

        y_predict = self.model.signatures['serving_default'](placeholder=content_image,
                                                             placeholder_1=self.style_img)['output_0'].numpy()
        image = cv2.cvtColor((y_predict[0] * 255).astype(np.uint8), cv2.COLOR_RGB2BGR)
        return image


def image2constant(image):
    image = image / 255
    image = image.astype(dtype=np.float32)
    image = tf.constant(image)
    return image
