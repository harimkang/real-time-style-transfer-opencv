import tensorflow_hub as hub
import tensorflow as tf
import numpy as np
import PIL.Image
import logging


class StyleTransfer:
    def __init__(self):
        self.hub_module = None

    def load(self):
        logging.info('===== Style Transfer Loading=====')
        module_path = 'https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2'
        self.hub_module = hub.load(module_path)
        logging.info('===== Style Transfer Loaded=====')

    def predict(self, frame, style):

        # content_image = frame.astype(np.float32)[np.newaxis, ...] / 255.
        # style_image = style.astype(np.float32)[np.newaxis, ...] / 255.
        #
        # style_image = tf.image.resize(style_image, (256, 256))

        # outputs = self.hub_module(tf.constant(frame), tf.constant(style))[0]
        outputs = self.hub_module(frame, style)[0]
        outputs = tensor_to_image(outputs)

        return outputs


def tensor_to_image(tensor):
    tensor = tensor * 255
    # tensor = np.array(tensor)
    # if np.ndim(tensor) > 3:
    #     assert tensor.shape[0] == 1
    #     tensor = tensor[0]
    return PIL.Image.fromarray(tensor)
