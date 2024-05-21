from selenium import webdriver
from selenium.webdriver.common.by import By
import pytesseract
import time
import cv2
from PIL import Image
import math
import numpy as np
import datetime
import csv
import pandas as pd
from tensorflow import keras
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
from sklearn.preprocessing import MinMaxScaler
from datetime import timedelta
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
driver = webdriver.Edge()
def Login():
    

    driver.get('https://binomo.com/trading')

    time.sleep(3)

    element = driver.find_element(By.CSS_SELECTOR, ".text_text-input__JsoR6 > input:nth-child(1)")

    element.send_keys("motiha3837@fashlend.com")

    element = driver.find_element(By.CSS_SELECTOR, ".password_password-input__1CSCP > input:nth-child(1)")

    element.send_keys("faruk1234")

    element = driver.find_element(By.CSS_SELECTOR, "#qa_auth_LoginBtn > button:nth-child(1)")

    element.click()

    input("Press enter to contiune...")
data = {}
average_forecast = None
df = None
train = 0
def Model():
    global train
    if train % 5 == 0:
        time.sleep(1)
        global df
        df = pd.read_csv('data.csv')

        df['Date'] = pd.to_datetime(df['Date'])

        df = df.set_index('Date')

        df['Value'] = pd.to_numeric(df['Value'], errors='coerce')

        df = df.dropna(subset=['Value'])

        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_data = scaler.fit_transform(df['Value'].values.reshape(-1,1))

        train_length = int(len(scaled_data) * 0.8)
        train_data = scaled_data[0:train_length]
        test_data = scaled_data[train_length:]

        def create_dataset(dataset, look_back=1):
            X, Y = [], []
            for i in range(len(dataset)-look_back-1):
                a = dataset[i:(i+look_back), 0]
                X.append(a)
                Y.append(dataset[i + look_back, 0])
            return np.array(X), np.array(Y)

        look_back = 50
        X_train, Y_train = create_dataset(train_data, look_back)
        X_test, Y_test = create_dataset(test_data, look_back)

        X_train = np.reshape(X_train, (X_train.shape[0], 1, X_train.shape[1]))
        X_test = np.reshape(X_test, (X_test.shape[0], 1, X_test.shape[1]))

        model = Sequential()
        model.add(LSTM(100, input_shape=(X_train.shape[1], X_train.shape[2])))
        model.add(Dropout(0.25))
        model.add(Dense(1))
        model.compile(loss='mean_squared_error', optimizer='adam')

        model.fit(X_train, Y_train, epochs=25, batch_size=1, verbose=2)

        forecasts = []
        for _ in range(10):
            input_data = df['Value'].values[-look_back:].reshape(-1,1)
            input_data = scaler.transform(input_data)
            input_data = np.reshape(input_data, (1, 1, look_back))

            forecast = []
            for _ in range(1):
                prediction = model.predict(input_data)
                forecast.append(scaler.inverse_transform(prediction)[0][0])
                input_data = np.append(input_data[0][0][1:], prediction)
                input_data = np.reshape(input_data, (1, 1, look_back))
            
            forecasts.append(forecast[-1])
        global average_forecast
        average_forecast = np.mean(forecasts)
def Predict():
    global train
    train += 1
    print(f"1 dakika sonraki ortalama BTC değeri tahmini: {average_forecast}")
    if average_forecast > df['Value'].values[-1]:
        print("BTC değerinin artacağı tahmin ediliyor.")
        element = driver.find_element(By.CSS_SELECTOR, "#qa_trading_dealUpButton > button")
        element.click()
    else:
        print("BTC değerinin düşeceği tahmin ediliyor.")
        element = driver.find_element(By.CSS_SELECTOR, "#qa_trading_dealDownButton > button")
        element.click()
    driver.get('https://binomo.com/trading')
    time.sleep(10)
Login()
while True:
    Model()
    Predict()