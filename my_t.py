import functools

from style_transfer import StyleTransfer
import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np


def crop_center(image):
    """Returns a cropped square image."""
    shape = image.shape
    new_shape = min(shape[1], shape[2])
    offset_y = max(shape[1] - shape[2], 0) // 2
    offset_x = max(shape[2] - shape[1], 0) // 2
    image = tf.image.crop_to_bounding_box(
        image, offset_y, offset_x, new_shape, new_shape)
    return image


@functools.lru_cache(maxsize=None)
def load_image(image_path, image_size=(256, 256), preserve_aspect_ratio=True):
    """Loads and preprocesses images."""
    # Load and convert to float32 numpy array, add batch dimension, and normalize to range [0, 1].
    img = plt.imread(image_path).astype(np.float32)[np.newaxis, ...]
    if img.max() > 1.0:
        img = img / 255.
    if len(img.shape) == 3:
        img = tf.stack([img, img, img], axis=-1)
    img = crop_center(img)
    img = tf.image.resize(img, image_size, preserve_aspect_ratio=True)
    return img


output_image_size = 384
content_img_size = (output_image_size, output_image_size)
style_img_size = (256, 256)

st = StyleTransfer()
st.load()

content = load_image("./images/cvui_20200324_155702_00001.png")
style = load_image("./style/VK1913.jpg")
# style_image = tf.nn.avg_pool(style, ksize=[3, 3], strides=[1, 1], padding='SAME')

output = st.predict(content, style)

plt.imshow(output)
