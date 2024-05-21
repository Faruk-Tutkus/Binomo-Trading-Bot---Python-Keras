import numpy as np
import pandas as pd
from keras.models import Sequential, load_model
from keras.layers import LSTM, Dense, Dropout
from keras.callbacks import EarlyStopping
from sklearn.preprocessing import MinMaxScaler
import joblib
from sklearn.metrics import mean_squared_error, mean_absolute_error
df = pd.read_csv('data.csv')
df['Date'] = pd.to_datetime(df['Date'], format="%d/%m/%Y, %H:%M:%S", dayfirst=True)
df = df.set_index('Date')
df['Value'] = pd.to_numeric(df['Value'], errors='coerce')
df = df.dropna(subset=['Value'])

scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(df['Value'].values.reshape(-1,1))

train_length = int(len(scaled_data) * 0.8)
train_data = scaled_data[:train_length]
test_data = scaled_data[train_length:]

valid_length = int(len(train_data) * 0.2)
valid_data = train_data[-valid_length:]
train_data = train_data[:-valid_length]
def create_dataset(dataset, look_back):
    X, Y = [], []
    for i in range(len(dataset)-look_back-1):
        a = dataset[i:(i+look_back), 0]
        X.append(a)
        Y.append(dataset[i + look_back, 0])
    return np.array(X), np.array(Y)
look_back = 16
X_train, Y_train = create_dataset(train_data, look_back)
X_valid, Y_valid = create_dataset(valid_data, look_back)
X_test, Y_test = create_dataset(test_data, look_back)

X_train = np.reshape(X_train, (X_train.shape[0], 1, X_train.shape[1]))
X_valid = np.reshape(X_valid, (X_valid.shape[0], 1, X_valid.shape[1]))
X_test = np.reshape(X_test, (X_test.shape[0], 1, X_test.shape[1]))

model = Sequential()
model.add(LSTM(units=256, return_sequences=True, input_shape=(X_train.shape[1], X_train.shape[-1])))
model.add(Dropout(0.2))
model.add(LSTM(units=128, return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(units=64, return_sequences=True))
model.add(Dropout(0.1))
model.add(LSTM(units=32, return_sequences=True))
model.add(Dropout(0.1))
model.add(LSTM(units=16, return_sequences=True))
model.add(Dropout(0.1))
model.add(LSTM(units=8, return_sequences=True))
model.add(Dropout(0.1))
model.add(LSTM(units=4))
model.add(Dense(1, activation='sigmoid'))
model.compile(loss='mean_absolute_error', optimizer='adam')

es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=100)

model.fit(X_train, Y_train, epochs=300, batch_size=64, verbose=1, callbacks=[es], validation_data=(X_valid, Y_valid))

predictions = model.predict(X_test)
predicted_values = scaler.inverse_transform(predictions)
real_values = scaler.inverse_transform(Y_test.reshape(-1, 1))
mse = mean_squared_error(real_values, predicted_values)
abs = mean_absolute_error(real_values, predicted_values)
print(f"Test veri seti üzerindeki hata (MSE): {mse}")
print(f"Test veri seti üzerindeki hata (ABS): {abs}")

model.save('model.keras')
joblib.dump(scaler, 'scaler.gz')


# Test veri seti üzerindeki hata (MSE): 45923473.42637311
# Test veri seti üzerindeki hata (ABS): 6759.084848484848

# Test veri seti üzerindeki hata (MSE): 15214320.05659411
# Test veri seti üzerindeki hata (ABS): 3194.9069940476174