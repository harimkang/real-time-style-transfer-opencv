"""
Programmer: Dahsom Jang
Description: Face Detection and Segmentation
"""

import tensorflow as tf
import numpy as np
import cv2


class ImageSegmentation:

    def __init__(self, width, height):

        self.width, self.height = width, height
        self.input_size = (256, 256)

        self.model = tf.keras.models.load_model('./models/unet_no_drop.h5')
        # self.model=tf.keras.models.load_model('./models/unet.h5')

    def predict(self, image):
        input_image = self.image_ready(image)
        seg_mask = self.model.predict(input_image)
        mask = self.generate_mask(seg_mask)
        return mask

    def image_ready(self, image):
        if type(image) != np.ndarray:
            pil_image = image.convert('RGB')
            open_cv_image = np.array(pil_image)
            open_cv_image = open_cv_image[:, :, ::-1].copy()
            image = open_cv_image
        else:
            image = image

        img = image
        width, height = self.input_size

        im = np.zeros((width, height, 3), dtype=np.uint8)
        if img.shape[0] >= img.shape[1]:
            scale = img.shape[0] / height
            new_width = int(img.shape[1] / scale)
            diff = (width - new_width) // 2
            img = cv2.resize(img, (new_width, height))
            im[:, diff:diff + new_width, :] = img

        else:
            scale = img.shape[1] / width
            new_height = int(img.shape[0] / scale)
            diff = (height - new_height) // 2
            img = cv2.resize(img, (width, new_height))
            im[diff:diff + new_height, :, :] = img

        input_image = im.reshape((width, height, 3))
        input_image = image_sharpening(input_image)
        input_image = input_image.reshape((1, width, height, 3)).astype(np.float32) / 255.

        return input_image

    def generate_mask(self, seg_mask, threshold=0.5):
        height, width = self.height, self.width
        prediction = seg_mask
        mask_ori = (prediction.squeeze()[:, :, 1] > threshold).astype(np.uint8)
        max_size = max(width, height)
        result_mask = cv2.resize(mask_ori, dsize=(max_size, max_size))
        if height >= width:
            diff = (max_size - width) // 2
            if diff > 0:
                result_mask = result_mask[:, diff:-diff]
        else:
            diff = (max_size - height) // 2
            if diff > 0:
                result_mask = result_mask[diff:-diff, :]
        result_mask = cv2.resize(result_mask, dsize=(width, height))
        return result_mask


def image_sharpening(image):
    sharpening = np.array([[-1, -1, -1, -1, -1],
                           [-1, 2, 2, 2, -1],
                           [-1, 2, 9, 2, -1],
                           [-1, 2, 2, 2, -1],
                           [-1, -1, -1, -1, -1]]) / 9.0

    dst = cv2.filter2D(image, -1, sharpening)
    return dst
