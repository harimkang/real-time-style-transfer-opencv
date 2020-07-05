"""
Programmer: Harim Kang
Description: Color, Font, Size for button UI
"""

import cv2


class Color:
    red = (0, 0, 255)
    gr = (0, 255, 0)
    button_off_color = (169, 169, 169)
    button_base_color = (50, 50, 50)
    silver = (100, 100, 100)
    light_gray = (211, 211, 211)
    white = (255, 255, 255)
    black_silver = (50, 50, 50)
    black = (0, 0, 0)
    yellow = (0, 255, 255)
    cyan = (255, 255, 0)
    magenta = (255, 0, 255)
    blue1 = (255, 178, 96)
    blue3 = (232, 198, 77)
    blue2 = (247, 255, 84)


class Font:
    font = [cv2.FONT_HERSHEY_SIMPLEX, cv2.FONT_HERSHEY_PLAIN, cv2.FONT_HERSHEY_DUPLEX,
            cv2.FONT_HERSHEY_COMPLEX, cv2.FONT_HERSHEY_TRIPLEX, cv2.FONT_HERSHEY_COMPLEX_SMALL]


class Size:
    button_text_size = 0.5
    button_width_rate = 0.1
    button_height_rate = 0.06

    btn_interval_x = 0.0325
    btn_interval_y = 0.12

    bottom_bound = 0.93
    top_bound = 0.01
    left_bound = 0.07
    side_up_bound = 0.2
