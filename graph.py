import pytesseract
import cv2
from PIL import Image
import numpy as np
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
img = cv2.imread('screenshot.png')
height, width, _ = img.shape
data = {}
roi = img[130:170, 635:810]

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
print(text)