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

        self.WIDTH = 640
        self.HEIGHT = 480

        self.center_x = self.WIDTH / 2
        self.center_y = self.HEIGHT / 2
        self.touched_zoom = False

        self.image_queue = Queue()
        self.video_queue = Queue()

        self.btn_manager = ButtonManager(self.WIDTH, self.HEIGHT)

        self.scale = 1
        self.__setup()

        self.recording = False

        self.style = style
        self.face_transfer = False

        self.style_transfer = StyleTransfer(self.WIDTH, self.HEIGHT)
        self.style_transfer.load()

        self.image_segmentation = ImageSegmentation(self.WIDTH, self.HEIGHT)

        self.mirror = mirror

    def __setup(self):
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, self.WIDTH)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, self.HEIGHT)
        self.btn_manager.button_setting()
        time.sleep(2)

    def get_location(self, x, y):
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
        # zoom 하는 실제 함수
        height, width = img.shape[:2]
        if center is None:
            #   중심값이 초기값일 때의 계산
            center_x = int(width / 2)
            center_y = int(height / 2)
            radius_x, radius_y = int(width / 2), int(height / 2)
        else:
            #   특정 위치 지정시 계산
            rate = height / width
            center_x, center_y = center

            #   비율 범위에 맞게 중심값 계산
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

        # 실제 zoom 코드
        radius_x, radius_y = int(self.scale * radius_x), int(self.scale * radius_y)

        # size 계산
        min_x, max_x = center_x - radius_x, center_x + radius_x
        min_y, max_y = center_y - radius_y, center_y + radius_y

        # size에 맞춰 이미지를 자른다
        cropped = img[min_y:max_y, min_x:max_x]
        # 원래 사이즈로 늘려서 리턴
        new_cropped = cv2.resize(cropped, (width, height))

        return new_cropped

    def touch_init(self):
        self.center_x = self.WIDTH / 2
        self.center_y = self.HEIGHT / 2
        self.touched_zoom = False
        self.scale = 1

    def zoom_out(self):
        # scale 값을 조정하여 zoom-out
        if self.scale < 1:
            self.scale += 0.1
        if self.scale == 1:
            self.center_x = self.WIDTH
            self.center_y = self.HEIGHT
            self.touched_zoom = False

    def zoom_in(self):
        # scale 값을 조정하여 zoom-in
        if self.scale > 0.2:
            self.scale -= 0.1

    def zoom(self, num):
        if num == 0:
            self.zoom_in()
        elif num == 1:
            self.zoom_out()
        elif num == 2:
            self.touch_init()

    def transform(self, img):
        copy_img = img.copy()
        # 1. Get a converted image with style transfer
        style_img = self.style_transfer.predict(copy_img)
        # 2. Getting a mask with face segmentation
        seg_mask = self.image_segmentation.predict(copy_img)
        mask = cv2.cvtColor(seg_mask, cv2.COLOR_GRAY2RGB)

        # 3. Combine face only with image converted to style transfer
        if self.face_transfer:
            image_result = np.where(mask, style_img, copy_img)
        else:
            image_result = np.where(mask, copy_img, style_img)
        return image_result

    def event(self, i):
        self.style_transfer.change_style(i)

    def save_picture(self):
        # Save Image Function
        ret, img = self.cam.read()
        if ret:
            now = datetime.datetime.now()
            date = now.strftime('%Y%m%d')
            hour = now.strftime('%H%M%S')
            user_id = '00001'
            filename = './images/cvui_{}_{}_{}.png'.format(date, hour, user_id)
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
        filename = 'videos/cvui_{}_{}_{}.avi'.format(date, t, num)
        while os.path.exists(filename):
            num += 1
            filename = 'videos/cvui_{}_{}_{}.avi'.format(date, t, num)
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
        while True:
            frame = self.data
            if frame is not None:
                self.btn_manager.draw(frame)
                cv2.imshow('SMS', frame)
                cv2.setMouseCallback('SMS', self.mouse_callback)
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

            elif key == ord('s'):
                self.style = True

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
        if event == cv2.EVENT_LBUTTONDOWN:
            self.btn_manager.btn_on_click(x, y)
            if 1 in self.btn_manager.button_flag:
                self.style = True
                for i in range(len(self.btn_manager.button_flag)):
                    if self.btn_manager.button_flag[i] == 1:
                        self.event(i)
                        break
            else:
                self.style = False

        elif event == cv2.EVENT_LBUTTONDBLCLK:
            self.get_location(x, y)
            self.zoom_in()
        elif event == cv2.EVENT_RBUTTONDOWN:
            self.zoom_out()


if __name__ == '__main__':
    cam = Camera(mirror=True, style=False)
    cam.stream()
    cam.show()
