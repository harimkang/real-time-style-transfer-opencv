"""
Programmer: Harim Kang
Description: Button and Manager Class for UI
"""

import cv2
from Style import Color, Size, Font


class Button:
    def __init__(self, x=None, y=None):
        self.x = x
        self.y = y
        self.w = 0
        self.h = 0
        self.text = ""
        self.icon = None

        self.text_size = Size.button_text_size
        self.text_color = Color.button_base_color
        self.button_font = Font.font[0]
        self.button_color = Color.button_off_color

        self.button_toggle = False
        self.background = False

    def set_location(self, x, y):
        self.x = x
        self.y = y

    def get_location(self):
        return self.x, self.y

    def set_text(self, text):
        self.text = text

    def get_text(self):
        return self.text

    def set_size(self, w, h):
        self.w = w
        self.h = h

    def get_size(self):
        return self.w, self.h

    def calculate_size(self, image):
        height, width, channels = image.shape
        self.w = int(width * Size.button_width_rate)
        self.h = int(height * Size.button_height_rate)

    def toggle(self):
        self.button_toggle = not self.button_toggle

    def draw(self, image, single=False):
        if single:
            self.calculate_size(image)
        if self.background or (self.icon is None):
            if self.button_toggle:
                self.button_color = Color.blue1
            else:
                self.button_color = Color.button_off_color
            cv2.rectangle(image, (self.x, self.y), (self.x + self.w, self.y + self.h), color=self.button_color,
                          thickness=cv2.FILLED)
        if self.icon is None:
            size = cv2.getTextSize(self.text, self.button_font, self.text_size, 1)
            cv2.putText(image, self.text, (self.x + int(self.w / 2 - size[0][0] / 2), self.y + int(self.h / 2) + 10),
                        self.button_font, self.text_size, self.text_color, 2, cv2.LINE_AA)
        else:
            if self.background:
                set_icon(image, self.icon, x=int(self.x + (self.w / 2) - int(self.w * 0.0625 / 2)),
                              y=self.y + 5, white=False)
            else:
                set_icon(image, self.icon, x=self.x, y=self.y, white=False)

    def on_click(self, x, y):
        if (self.x <= x <= self.x + self.w) and (self.y <= y <= self.y + self.h):
            return True
        else:
            return False


class ButtonManager:
    def __init__(self, w, h, loc=0):
        self.img_w = w
        self.img_h = h

        self.btn_interval_x = int(w * Size.btn_interval_x)
        self.btn_interval_y = int(h * Size.btn_interval_y)

        self.start_x = 0
        self.start_y = 0

        self.loc_x = 0
        self.loc_y = 0

        self.button_width = 0
        self.button_height = 0

        self.button_list = []
        self.button_flag = []

        self.loc = loc
        if self.loc == 0:
            self.loc_x = 0.02
            self.loc_y = 10
            self.start_x = int(self.img_w * self.loc_x)
            self.start_y = self.loc_y

    def set_button_location(self, image):
        for i in range(len(self.button_list)):
            if i == 0:
                self.button_list[i].calculate_size(image)
                self.button_list[i].set_location(self.start_x, self.start_y)
            else:
                if self.loc == 0:
                    pre_x, pre_y = self.button_list[i - 1].get_location()
                    wid, hei = self.button_list[i - 1].get_size()
                    self.button_list[i].calculate_size(image)
                    self.button_list[i].set_location(int(pre_x + wid + self.btn_interval_x), pre_y)

    def draw(self, image):
        self.set_button_location(image)
        self.check_flag()
        for button in self.button_list:
            button.draw(image)

    def add_button(self, button):
        self.button_list.append(button)
        self.button_flag.append(0)

    def add_button_list(self, button_list):
        self.button_list = button_list
        self.button_flag = [0 for _ in self.button_list]

    def del_button(self, index):
        self.button_list.pop(index)

    def button_clear(self):
        self.button_list = []

    def button_setting(self):
        btn2 = Button()
        btn2.set_text("GOGH")
        btn3 = Button()
        btn3.set_text("VK1913")
        btn4 = Button()
        btn4.set_text("MONET")
        btn_list = [btn2, btn3, btn4]
        self.add_button_list(btn_list)

    def btn_on_click(self, x, y):
        for i in range(len(self.button_list)):
            if self.button_list[i].on_click(x, y):
                if self.button_flag[i] == 1:
                    self.button_flag = [0 for _ in self.button_list]
                else:
                    self.button_flag = [0 for _ in self.button_list]
                    self.button_flag[i] = 1
                break

    def check_flag(self):
        for i in range(len(self.button_flag)):
            if self.button_flag[i] == 1:
                self.button_list[i].button_toggle = True
            else:
                self.button_list[i].button_toggle = False


def set_icon(image, icon, x, y, white=True, icon_size=50):
    icon_img = cv2.resize(icon, dsize=(icon_size, icon_size), interpolation=cv2.INTER_AREA)
    width = icon_img.shape[0]
    height = icon_img.shape[1]
    roi = image[y:y + height, x:x + width]
    mask = cv2.bitwise_not(icon_img)
    if white:
        image = cv2.add(roi, mask)
    else:
        gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)
        image = cv2.bitwise_and(roi, roi, mask=mask_inv)
    image[y:y + height, x:x + width] = image


# if __name__ == "__main__":
#     cam = Camera()
#     cam.stream()
#     img_w = 640
#     img_h = 480
#     bm = ButtonManager(img_w, img_h)
#     bm.button_setting()
#
#     while True:
#         frame = cam.data
#         if frame is not None:
#             bm.draw(frame)
#             cv2.imshow('SMS', frame)
#         key = cv2.waitKey(1)
#         if key == ord('q'):
#             # q : close
#             cam.release()
#             cv2.destroyAllWindows()
#             break
