# -*- coding: utf-8 -*-

import sys
import win32clipboard as wc
import pip

try:
    from win32api import GetSystemMetrics
except:
    pip.main(["install", "pywin32"])

try:
    import cv2
except:
    pip.main(["install", "opencv-python"])
import numpy as np
import time
from PIL import Image, ImageGrab
import pyautogui
from matplotlib import pyplot as plt


def setCP(s):
    wc.OpenClipboard()
    wc.EmptyClipboard()
    wc.SetClipboardText(s)
    wc.CloseClipboard()


def getCP():
    st = ''
    wc.OpenClipboard()
    try:
        st = wc.GetClipboardData()
    except:
        print(sys.exc_info(), 'func')
    finally:
        wc.CloseClipboard()
        # print('close func "'+st+'"')
    # wc.EmptyClipboard()
    return st


def get_Metrics():
    return GetSystemMetrics(0), GetSystemMetrics(1)


def make_photo():
    obj = ImageGrab.grab()
    image = obj.load()
    return image


# по вертикали 691 716
# по горизонтали 1070 1205
def where_pix(image):
    good = 0
    x, y = get_Metrics()
    color = (0, 230, 203)
    color1 = (0, 230, 204)
    x1 = x - 296
    x2 = x - 161
    y1 = y - 77
    y2 = y - 52
    for i in range(x1, x2):
        for j in range(y1, y2):
            if image[i, j] == color or image[i, j] == color1:
                for k in range(20):
                    if image[i + k, j] == color or image[i + k, j] == color1:
                        good += 1
                        if good >= 20:
                            return i, j
                    else:
                        good = 0
    return False


def append_in_file(inf):
    with open('log.txt', mode='a', encoding='UTF-8') as file:
        file.write(inf)


def get_url() -> str:
    sp_start = getCP()
    pyautogui.press("f6")
    pyautogui.keyDown('ctrl')
    pyautogui.press('c')
    pyautogui.keyUp('ctrl')
    cp_new = getCP()
    setCP("")
    setCP(sp_start)
    return cp_new


if __name__ == '__main__':
    while True:
        time.sleep(6)
        start = pyautogui.position()
        photo = make_photo()
        try:
            x, y = where_pix(photo)
            url = get_url()
            pyautogui.click(x, y)
            pyautogui.moveTo(start)
            print(f"есть 50| {url} | {time.time()} | {time.ctime()}")
            append_in_file(f"есть 50| {url} | {time.time()} | {time.ctime()}\n")
        except TypeError:
            print("нет 50")
