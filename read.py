import os
import cv2
from PIL import Image
import csv
import numpy as np
import pytesseract
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

def Zaman(gün, ay, yıl, saat, dakika, saniye):
    # Tarih ve saat bilgisini formatlayarak string olarak döndürür
    return f"{gün:02d}/{ay:02d}/{yıl}, {saat:02d}:{dakika:02d}:{saniye:02d}"

def process_image(file_path, gün, ay, yıl, saat, dakika, saniye, csv_file):
    with open(file_path, 'rb') as file:
        img = cv2.imread(file_path)
        roi = img[205:235, 540:710]  

        lower = np.array([100, 100, 100])
        upper = np.array([255, 255, 255])
        mask = cv2.inRange(roi, lower, upper)
        roi[mask != 255] = [100,100,100]

        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        binary = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,0)

        cv2.imwrite('roi_2.png',binary)

        img = Image.open('roi_2.png')

        custom_config = r'--oem 3 --psm 1'
        text = pytesseract.image_to_string(img, config=custom_config)
        text = text.replace('\n', '').replace('.', '').replace(' ', '')
        parça2 = text[6:]
        text = parça2

    # Zaman bilgisini hesapla
    gün, ay, yıl, saat, dakika, saniye = update_time(gün, ay, yıl, saat, dakika, saniye)

    # CSV'ye yaz
    date = Zaman(gün, ay, yıl, saat, dakika, saniye)
    with open(csv_file, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if csvfile.tell() == 0:  # Dosya boşsa sadece başlık satırını yazın
            writer.writerow(["Date", "Value"])
        writer.writerow([date, text])

    return gün, ay, yıl, saat, dakika, saniye
def process_images(folder_path, csv_file):
    file_list = os.listdir(folder_path)
    print(len(file_list))
    gün, ay, yıl, saat, dakika, saniye = 17, 12, 2023, 20, 0, -5
    for i in range(len(file_list)):
        file_name = folder_path + "\\screenshot_{num}.png".format(num = i)
        if file_name.endswith('.png'):
            print(file_name)
            file_path = os.path.join(folder_path, file_name)
            gün, ay, yıl, saat, dakika, saniye = process_image(file_path, gün, ay, yıl, saat, dakika, saniye, csv_file)
def update_time(gün, ay, yıl, saat, dakika, saniye):
    saniye += 5
    if saniye >= 60:
        saniye = 0
        dakika += 1
    if dakika >= 60:
        dakika = 0
        saat += 1
    if saat >= 24:
        saat = 0
        gün += 1
    # Burada ay ve yıl güncellemeleri eklenmeli
    return gün, ay, yıl, saat, dakika, saniye

# Klasör yolunu belirtin
folder_path = "D:\\ScreenShots"
csv_file = 'data.csv'

# PNG dosyalarını işle
process_images(folder_path, csv_file)
