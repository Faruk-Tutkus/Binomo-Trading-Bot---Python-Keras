import pyautogui
import pytesseract
import cv2
from PIL import Image
import numpy as np
import datetime
import csv
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
count = 0
for _ in range(4):
    x, y = 1670, 400
    pyautogui.moveTo(x, y, duration=0.2)
    new_x, new_y = 727, 400
    pyautogui.dragTo(new_x,duration=5)
    count += 1
    if count == 5:
        x, y = 1670, 400
        pyautogui.moveTo(x, y, duration=0.2)
        new_x, new_y = 1668, 400
        pyautogui.dragTo(new_x,duration=5)
        count = 0
    x, y = 1670, 400
    for i in range(21):
        pyautogui.moveTo(x, y)
        img = cv2.imread('screenshot.png')
        height, width, _ = img.shape
        data = {}
        roi = img[200:242, 110: 1270] 

        lower = np.array([100, 100, 100])
        upper = np.array([255, 255, 255])
        mask = cv2.inRange(roi, lower, upper)
        roi[mask != 255] = [100,100,100]

        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

        binary = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,0)

        cv2.imwrite('roi.png',binary)

        img = Image.open('roi.png')

        custom_config = r'--oem 3 --psm 1'
        text = pytesseract.image_to_string(img, config=custom_config)
        data[datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")] = text
        with open('test.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Value"])
            for key, value in data.items():
                writer.writerow([key, value])
        x -= 45
    x = 1670