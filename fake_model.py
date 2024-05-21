import numpy as np
from keras.models import Sequential
from keras.layers import LSTM, Dense

# Örnek veri oluşturma (ardışık olmayan)
X_train = np.arange(1, 201, 2)  # 1'den 200'e kadar olan tek sayılar
X_train = X_train.reshape(100, 1)  # LSTM için 2 boyutlu veri
y_train = 2 * X_train + 10  # Her sayının 2 ile çarpılıp 10 eklenmiş hali

# Model oluşturma
model = Sequential()
model.add(Dense(10, input_dim=1, activation='relu'))  # Giriş katmanı
model.add(Dense(10, activation='relu'))  # Gizli katman
model.add(Dense(1))  # Çıkış katmanı

# Modeli derleme
model.compile(loss='mean_squared_error', optimizer='adam')

# Modeli eğitme
model.fit(X_train, y_train, epochs=1000, batch_size=10, verbose=0)

# Tahmin yapma
X_test = np.array([[202]])  # 202 sayısını tahmin etmek için
prediction = model.predict(X_test)
print("Tahmin:", prediction)
