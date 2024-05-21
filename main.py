from selenium import webdriver
from selenium.webdriver.common.by import By
import pytesseract
import time
import joblib
import cv2
from PIL import Image
import math
import numpy as np
import datetime
import csv
import pandas as pd
import pytesseract
from keras.models import load_model
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
driver_ = webdriver.Edge()
driver = webdriver.Edge()
def Login():
    driver_.get('https://tradingpoin.com/chart?pair=CRYIDX.B&source=Binomo&val=Z-CRY%2FIDX&timeframe=60&description=CRYPTO%20/%20IDX')
    driver.get('https://binomo.com/trading')
    time.sleep(3)

    element = driver.find_element(By.CSS_SELECTOR, ".text_text-input__JsoR6 > input:nth-child(1)")

    element.send_keys("motiha3837@fashlend.com")

    element = driver.find_element(By.CSS_SELECTOR, ".password_password-input__1CSCP > input:nth-child(1)")

    element.send_keys("faruk1234")

    element = driver.find_element(By.CSS_SELECTOR, "#qa_auth_LoginBtn > button:nth-child(1)")

    element.click()

    input("Press enter to contiune...")
    time.sleep(5)
data = {}
arr = []
a = 0
count = 0
def ScreenShot():
    global a, count
    driver_.save_screenshot('screenshot.png')
    img = cv2.imread('screenshot.png')
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
    if text.strip() != '':
        if len(text) == 6:
            pass
        text = text.replace('\n', '').replace('.', '').replace(' ', '')
        parça2 = text[6:]
        text = parça2
        if text not in arr:
            arr.append(text)
            data[datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")] = arr[len(arr) - 1]
            with open('test.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Date", "Value"])
                for key, value in data.items():
                    writer.writerow([key, value])
            count += 1
        
    # if len(parca2) != 6:
    #     driver_.save_screenshot('ScreenShots\\screenshot{num}.png'.format(num = a))
    #     a += 1
    #     #print(text)
    time.sleep(1)

def clean_value(x):
    try:
        return float(x)
    except ValueError:
        return np.nan

model = load_model('model.keras')
scaler = joblib.load('scaler.gz')
def Predict():
    df_test = pd.read_csv('test.csv')
    df_test['Value'] = df_test['Value'].apply(clean_value)
    scaled_data_test = scaler.fit_transform(df_test['Value'].values.reshape(-1,1))
    look_back = 16
    predictions = []
    input_data = scaled_data_test[-look_back:]
    print(int(datetime.datetime.now().strftime("%S")), end=' ')
    if int(datetime.datetime.now().strftime("%S")) >= 0 and int(datetime.datetime.now().strftime("%S")) < 30:
        print('First')
        for _ in range(5):
            input_data = np.reshape(input_data, (1, 1, look_back))
            prediction = model.predict(input_data)
            predictions.append(prediction[0][0])
            input_data = np.append(input_data[0][0][1:], prediction)
    else:
        print('Second')
        for _ in range(5):
            input_data = np.reshape(input_data, (1, 1, look_back))
            prediction = model.predict(input_data)
            predictions.append(prediction[0][0])
            input_data = np.append(input_data[0][0][1:], prediction)
    # Tahmin edilen değeri ölçeklendirmenin tersini yap
    predicted_values = scaler.inverse_transform(np.array(predictions).reshape(-1, 1))

    #print(f"Sonraki 60 dakika için BTC değeri tahminleri: {predicted_values}")
    if predicted_values[-1] > df_test['Value'].values[-1]:
        print("BTC değerinin artacağı tahmin ediliyor.", f"Mevcut Değer{df_test['Value'].values[-1]}", f"Tahmini Değer{predicted_values[-1]}")
        element = driver.find_element(By.CSS_SELECTOR, "#qa_trading_dealUpButton > button")
        element.click()
    else:
        print("BTC değerinin düşeceği tahmin ediliyor.", f"Mevcut Değer{df_test['Value'].values[-1]}", f"Tahmini Değer{predicted_values[-1]}")
        element = driver.find_element(By.CSS_SELECTOR, "#qa_trading_dealDownButton > button")
        element.click()
    driver.get('https://binomo.com/trading')

Login()
# ScreenShot()
start = False
while True:
    if len(data) >= 16:
        Predict()
        data.clear()
        arr.clear()
    if int(datetime.datetime.now().strftime("%S")) == 0:
        start = True
    if start:
        ScreenShot()


