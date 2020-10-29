import cv2
import numpy as np
import time
from PIL import Image, ImageGrab
import pyautogui
from matplotlib import pyplot as plt


def make_photo():
    obj = ImageGrab.grab()
    image = obj.load()
    return image


def find_patt(image, patt, thres):
    img_grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    (patt_H, patt_W) = patt.shape[:2]
    res = cv2.matchTemplate(img_grey, patt, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res > thres)
    return patt_H, patt_W, zip(*loc[::-1])


def find_pic(where, what):
    img_rgb = cv2.imread(where)  # где ищем
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(what, 0)  # что ищем
    w, h = template.shape[::-1]

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)

    threshold = 0.8
    loc = np.where(res >= threshold)
    print(loc)
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

    cv2.imwrite('res.png', img_rgb)


if __name__ == '__main__':
    #time.sleep(2)
    #find_pic("50.png", make_photo())
    #find_pic('window.png', 'w_circle.png')
    screenshot = ImageGrab.grab()
    img = np.array(screenshot.getdata(), dtype='uint8').reshape((screenshot.size[1], screenshot.size[0], 3))

    patt = cv2.imread('50.png', 0)
    h, w, points = find_patt(img, patt, 0.90)
    points = list(points)
    print(points)
    if len(points) != 0:
        # pyautogui.moveTo(points[0][0] + w / 2, points[0][1] + h / 2)
        pyautogui.moveTo(points[0][0], points[0][1])
        print(points[0][-2], points[0][-1])
        #pyautogui.click()