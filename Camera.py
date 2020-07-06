"""
Programmer: Harim Kang, Dahsom Jang
Description: Streaming Camera with zoom function, face segmentation, and style transfer function
"""

import cv2
import time
import os
import datetime
from threading import Thread
from queue import Queue
import numpy as np

from style_transfer import StyleTransfer
from image_segmentation import ImageSegmentation
from Button import ButtonManager


class Camera:
    # Camera class for streaming
    def __init__(self, mirror=False, style=False):
        """
        mirror: Support camera mirror mode
        style: Style transfer application
        """
        self.data = None
        self.cam = cv2.VideoCapture(0)

        self.style = style
        self.mirror = mirror

        self.WIDTH = 640
        self.HEIGHT = 480

        # This parameter is used to know the center position when the zoom function is in use.
        self.center_x = self.WIDTH / 2
        self.center_y = self.HEIGHT / 2
        self.touched_zoom = False

        # Queue for image capture and video recording.
        self.image_queue = Queue()
        self.video_queue = Queue()

        # Button manager object for creating UI buttons.
        self.btn_manager = ButtonManager(self.WIDTH, self.HEIGHT)

        # scale is a variable that determines zoom of the screen.
        self.scale = 1

        # It is a variable to check whether it is currently recording.
        self.recording = False

        # Whether to apply the style transfer to the face only.
        self.face_transfer = False
        # An object that performs style transfers.
        self.style_transfer = StyleTransfer(self.WIDTH, self.HEIGHT)
        # It is an object that recognizes the face and segments it.
        self.image_segmentation = ImageSegmentation(self.WIDTH, self.HEIGHT)

        self.__setup()

    def __setup(self):
        # Prepare the camera settings, button manager, and style transfer objects.
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, self.WIDTH)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, self.HEIGHT)

        self.btn_manager.button_setting()
        self.style_transfer.load()
        time.sleep(2)

    def get_location(self, x, y):
        # Specifies the center of the current screen.
        self.center_x = x
        self.center_y = y
        self.touched_zoom = True

    def stream(self):
        # Streaming thread Function
        def streaming():
            self.ret = True
            while self.ret:
                self.ret, np_image = self.cam.read()
                if np_image is None:
                    continue
                if self.mirror:
                    # Mirror mode function
                    np_image = cv2.flip(np_image, 1)
                if self.touched_zoom:
                    # When using the double-click zoom function,
                    np_image = self.__zoom(np_image, (self.center_x, self.center_y))
                else:
                    # When not zoomed,
                    if not self.scale == 1:
                        np_image = self.__zoom(np_image)

                if self.style:
                    # Convert image to style transfer
                    image_result = self.transform(np_image)

                    np_image = image_result

                self.data = np_image
                k = cv2.waitKey(1)
                if k == ord('q'):
                    self.release()
                    break

        Thread(target=streaming).start()

    def __zoom(self, img, center=None):
        # This function calculates various values ​​according to the scale of the current screen
        # and applies them to the screen.
        height, width = img.shape[:2]
        if center is None:
            # When the center is the initial value,
            center_x = int(width / 2)
            center_y = int(height / 2)
            radius_x, radius_y = int(width / 2), int(height / 2)
        else:
            # When the center is not the initial value (when the zoom function is activated)
            rate = height / width
            center_x, center_y = center

            # Calculate center value according to ratio
            if center_x < width * (1 - rate):
                center_x = width * (1 - rate)
            elif center_x > width * rate:
                center_x = width * rate
            if center_y < height * (1 - rate):
                center_y = height * (1 - rate)
            elif center_y > height * rate:
                center_y = height * rate

            center_x, center_y = int(center_x), int(center_y)
            left_x, right_x = center_x, int(width - center_x)
            up_y, down_y = int(height - center_y), center_y
            radius_x = min(left_x, right_x)
            radius_y = min(up_y, down_y)

        # Calculate position according to proportion
        radius_x, radius_y = int(self.scale * radius_x), int(self.scale * radius_y)

        # Size calculation
        min_x, max_x = center_x - radius_x, center_x + radius_x
        min_y, max_y = center_y - radius_y, center_y + radius_y

        # Crop the image to fit the calculated size.
        cropped = img[min_y:max_y, min_x:max_x]
        # Stretch the cropped image to the original image size.
        new_cropped = cv2.resize(cropped, (width, height))

        return new_cropped

    def touch_init(self):
        # Initialize state
        self.center_x = self.WIDTH / 2
        self.center_y = self.HEIGHT / 2
        self.touched_zoom = False
        self.scale = 1

    def zoom_out(self):
        # Zoom-out by increasing the scale value
        if self.scale < 1:
            self.scale += 0.1
        if self.scale == 1:
            self.center_x = self.WIDTH
            self.center_y = self.HEIGHT
            self.touched_zoom = False

    def zoom_in(self):
        # Zoom-in function by reducing scale value
        if self.scale > 0.2:
            self.scale -= 0.1

    def zoom(self, num):
        # Zoom in & out according to index
        if num == 0:
            self.zoom_in()
        elif num == 1:
            self.zoom_out()
        elif num == 2:
            self.touch_init()

    def transform(self, img):
        # Functions that perform style transfers
        copy_img = img.copy()
        copy_img2 = img.copy()
        # 1. Get a converted image with style transfer
        style_img = self.style_transfer.predict(copy_img)
        # 2. Getting a mask with face segmentation
        seg_mask = self.image_segmentation.predict(copy_img2)
        mask = cv2.cvtColor(seg_mask, cv2.COLOR_GRAY2RGB)

        # 3. Combine face only with image converted to style transfer
        if self.face_transfer:
            image_result = np.where(mask, style_img, img)
        else:
            image_result = np.where(mask, img, style_img)
        return image_result

    def event(self, i):
        # Function to change style according to button event
        self.style = True
        self.style_transfer.change_style(i)

    def save_picture(self):
        # Save Image Function
        ret, img = self.cam.read()
        if ret:
            now = datetime.datetime.now()
            date = now.strftime('%Y%m%d')
            hour = now.strftime('%H%M%S')
            user_id = '00001'
            filename = './images/mevia_{}_{}_{}.png'.format(date, hour, user_id)
            cv2.imwrite(filename, img)
            self.image_queue.put_nowait(filename)

    def record_video(self):
        # Recording Function
        fc = 20.0
        record_start_time = time.time()
        now = datetime.datetime.now()
        date = now.strftime('%Y%m%d')
        t = now.strftime('%H')
        num = 1
        filename = 'videos/mevia_{}_{}_{}.avi'.format(date, t, num)
        while os.path.exists(filename):
            num += 1
            filename = 'videos/mevia_{}_{}_{}.avi'.format(date, t, num)
        codec = cv2.VideoWriter_fourcc('D', 'I', 'V', 'X')
        out = cv2.VideoWriter(filename, codec, fc, (int(self.cam.get(3)), int(self.cam.get(4))))
        while self.recording:
            if time.time() - record_start_time >= 600:
                self.record_video()
                break
            ret, frame = self.cam.read()
            if ret:
                if len(os.listdir('./videos')) >= 100:
                    name = self.video_queue.get()
                    if os.path.exists(name):
                        os.remove(name)
                out.write(frame)
                self.video_queue.put_nowait(filename)
            k = cv2.waitKey(1)
            if k == ord('q'):
                break

    def show(self):
        # Function to show streaming screen
        # Provides various functions using keyboard keys
        """
        q: Close & Quit
        z: Zoom-in
        x: Zoom-out
        p: Save Picture
        v: Return initial State
        r: Video recording
        """
        while True:
            frame = self.data
            if frame is not None:
                self.btn_manager.draw(frame)
                cv2.imshow('Mevia', frame)
                cv2.setMouseCallback('Mevia', self.mouse_callback)
            key = cv2.waitKey(1)
            if key == ord('q'):
                # q : close
                self.release()
                cv2.destroyAllWindows()
                break

            elif key == ord('z'):
                # z : zoom - in
                self.zoom_in()

            elif key == ord('x'):
                # x : zoom - out
                self.zoom_out()

            elif key == ord('p'):
                # p : take picture and save image (image folder)
                self.save_picture()

            elif key == ord('v'):
                # v : original state
                self.touch_init()

            elif key == ord('r'):
                # r : recording
                self.recording = not self.recording
                if self.recording:
                    t = Thread(target=cam.record_video)
                    t.start()

    def release(self):
        self.cam.release()
        cv2.destroyAllWindows()

    def mouse_callback(self, event, x, y, flag, param):
        # Mouse click event handling function
        if event == cv2.EVENT_LBUTTONDOWN:
            # Left click once (or touch)
            # Determining whether a button is clicked by passing the click position to the button manager
            self.btn_manager.btn_on_click(x, y)
            if self.btn_manager.button_flag[-1] == 0:
                self.face_transfer = False
            else:
                self.face_transfer = True
            if 1 in self.btn_manager.button_flag:
                # If the button was clicked, On style transfer
                for i in range(len(self.btn_manager.button_flag)):
                    if self.btn_manager.button_flag[i] == 1 and i != 6:
                        # Change the style to suit the clicked button
                        self.event(i)
                        break
            else:
                self.style = False

        elif event == cv2.EVENT_LBUTTONDBLCLK:
            # When double-clicking the left button, activate the zoom function
            self.get_location(x, y)
            self.zoom_in()
        elif event == cv2.EVENT_RBUTTONDOWN:
            # Right click, zoom out
            self.zoom_out()


if __name__ == '__main__':
    cam = Camera(mirror=True, style=False)
    cam.stream()
    cam.show()
