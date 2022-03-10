import pyautogui
import time

import pyscreenshot as ImageGrab
import cv2
import numpy as np
import argparse

def template_matching(screen, button):
    res = cv2.matchTemplate(screen, button, cv2.TM_CCOEFF_NORMED)
    minval, maxval, minloc, maxloc = cv2.minMaxLoc(res)
    if maxval > 0.7:
        cv2.rectangle(screen, maxloc, (maxloc[0] + w, maxloc[1] + h), (0, 0, 255), -1)
        w, h = button.shape[::-1]
        location = maxloc[0] + int(w/2), maxloc[1] + int(h/2)
        return location

def screenrecording(args):
    while True:
        if args.multiscale:
            screen = cv2.cvtColor(np.asarray(ImageGrab.grab()), cv2.COLOR_BGR2GRAY)
            button = cv2.imread("button.png", cv2.IMREAD_GRAYSCALE)
            location = template_matching(screen, button)
        else:
            location = pyautogui.locateOnScreen("button.png")

        if location:
            print(f"Found button at {location}")
            pyautogui.click(location)

        time.sleep(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--multiscale", action="store_true")
    screenrecording(parser.parse_args())
