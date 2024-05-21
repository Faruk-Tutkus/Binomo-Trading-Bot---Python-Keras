import joblib
import numpy as np
import datetime
import pandas as pd
from keras.models import load_model
def clean_value(x):
    try:
        return float(x)
    except ValueError:
        return np.nan
model = load_model('model.keras')
scaler = joblib.load('scaler.gz')

df_test = pd.read_csv('test.csv')
df_test['Value'] = df_test['Value'].apply(clean_value)
scaled_data_test = scaler.fit_transform(df_test['Value'].values.reshape(-1,1))
look_back = 16
predictions = []
input_data = scaled_data_test[-look_back:]
print(int(datetime.datetime.now().strftime("%S")), end=' ')
if int(datetime.datetime.now().strftime("%S")) >= 0 and int(datetime.datetime.now().strftime("%S")) < 30:
    print('First')
    for _ in range(1):
        input_data = np.reshape(input_data, (1, 1, look_back))
        prediction = model.predict(input_data)
        predictions.append(prediction[0][0])
        input_data = np.append(input_data[0][0][1:], prediction)
else:
    print('Second')
    for _ in range(1):
        input_data = np.reshape(input_data, (1, 1, look_back))
        prediction = model.predict(input_data)
        predictions.append(prediction[0][0])
        input_data = np.append(input_data[0][0][1:], prediction)
# Tahmin edilen değeri ölçeklendirmenin tersini yap
predicted_values = scaler.inverse_transform(np.array(predictions).reshape(-1, 1))

#print(f"Sonraki 60 dakika için BTC değeri tahminleri: {predicted_values}")
if predicted_values[-1] > df_test['Value'].values[-1]:
    print("BTC değerinin artacağı tahmin ediliyor.", f"Mevcut Değer{df_test['Value'].values[-1]}", f"Tahmini Değer{predicted_values[-1]}")
else:
    print("BTC değerinin düşeceği tahmin ediliyor.", f"Mevcut Değer{df_test['Value'].values[-1]}", f"Tahmini Değer{predicted_values[-1]}")