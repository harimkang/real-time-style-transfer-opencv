import tensorflow as tf
from PIL import Image
import numpy as np
import cv2

class ImageSegmentation:
     
  def __init__(self,image):
    if type(image)!=np.ndarray:
      pil_image = image
      pil_image=image.convert('RGB') 
      open_cv_image = np.array(pil_image) 
      open_cv_image = open_cv_image[:, :, ::-1].copy() 
      self.image=open_cv_image
    else:
      self.image=image
    self.height,self.width,_=self.image.shape
    self.input_size = (256, 256)
    self.input_image=None
    self.pred=None
    self.mask=None


  def predict(self):
    self.model=tf.keras.models.load_model('./models/unet_no_drop.h5')
    #self.model=tf.keras.models.load_model('./models/unet.h5')
    self.input_image = self.image_preprocess()
    self.pred = self.model.predict(self.input_image)

  def get_mask(self):
    self.mask=self.generate_mask()
    return self.mask

  def image_preprocess(self):
    img=self.image
    width,height=self.input_size

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

    input_image=im.reshape((width,height,3))
    input_image=self.image_sharpening(im)
    input_image=im.reshape((1, width, height, 3)).astype(np.float32) / 255.
    
    
    return input_image
  
  def generate_mask(self,threshold=0.5):
    height,width=self.height,self.width
    prediction=self.pred
    original_image=self.image
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
    result_mask      
    return result_mask

  def image_sharpening(self,image):
    sharpening= np.array([[-1, -1, -1, -1, -1],
                             [-1, 2, 2, 2, -1],
                             [-1, 2, 9, 2, -1],
                             [-1, 2, 2, 2, -1],
                             [-1, -1, -1, -1, -1]]) / 9.0

    dst = cv2.filter2D(image, -1, sharpening)
    return dst
