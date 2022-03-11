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
        w, h = button.shape[::-1]
        location = maxloc[0] + int(w / 2), maxloc[1] + int(h / 2)
        return location

def color_shape_approx(screen):
    color1 = np.asarray([1, 1, 140])
    color2 = np.asarray([10, 10, 200])
    mask = cv2.inRange(screen, color1, color2)
    cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        perimeter = cv2.arcLength(c, True)
        if perimeter > 100:
            approx = cv2.approxPolyDP(c, 0.02 * perimeter, True)
            if len(approx) == 4:
                return cv2.boundingRect(approx)

def autoclicker(args):
    while True:
        location = None
        if args.match == "color":
            screen = cv2.cvtColor(np.array(ImageGrab.grab()), cv2.COLOR_BGR2RGB)
            location = color_shape_approx(screen)
        elif args.match == "template":
            screen = cv2.cvtColor(np.asarray(ImageGrab.grab()), cv2.COLOR_BGR2GRAY)
            button = cv2.imread("button.png", cv2.IMREAD_GRAYSCALE)
            location = template_matching(screen, button)
        elif args.match == "pyautogui":
            location = pyautogui.locateOnScreen("button.png")

        if location:
            print(f"Found button at {location}")
            pyautogui.click(location)
            pyautogui.moveTo(location[0] + 400, location[1])

        time.sleep(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--match", type=str, choices=["color", "template", "pyautogui"], default="color")
    autoclicker(parser.parse_args())
