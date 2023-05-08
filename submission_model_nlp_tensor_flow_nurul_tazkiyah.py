# -*- coding: utf-8 -*-
"""Submission model NLP tensor flow - Nurul Tazkiyah.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1rgsjY6dpWaGhjXw9lwienx0wtNaVMexz

## **Submission Klasifikasi Teks Model NLP Tensor Flow oleh Nurul Tazkiyah Adam**
"""

# memastikan tensorflow yang digunakan versi 2 atau lebih
import tensorflow as tf
print(tf.__version__)

# download dataset dari google drive https://drive.google.com/file/d/1KiijiWW5fcmGYHza8hnVfG_3Cbv9AnyW/view?usp=sharing
!gdown 1KiijiWW5fcmGYHza8hnVfG_3Cbv9AnyW

import pandas as pd

df = pd.read_csv("bbc-text.csv")
df.head()

category = pd.get_dummies(df['category'])
df_new = pd.concat([df, category], axis=1)
df_new = df_new.drop(columns='category')
df_new

import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))

def remove_stopwords(new_df):
    filtered_words = [word.lower() for word in new_df.split() if word.lower() not in stop_words]
    return " ".join(filtered_words)

print(stop_words)

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

#proses tokenizer, filter simbol, dan mengubah tulisan menjadi kecil
tokenizer = Tokenizer(num_words=5000, oov_token='x', 
                      filters='!#$%&()*+,-./:;<=>?@[\]^_`{|}~', lower=True) 
tokenizer.fit_on_texts(df_new['text'])
word_index = tokenizer.word_index #identifikasi kata unik
print('Found %s unique tokens / words' %len(word_index))


X = tokenizer.texts_to_sequences(df_new['text'])
X = pad_sequences(X, maxlen=250)
print('Shape of data tensor:', X.shape)

Y = pd.get_dummies(df['category']).values
print('Shape of label tensor:', Y.shape) #untuk mengetahui jumlah label

from sklearn.model_selection import train_test_split

#melatih data latih dan data uji 
x_train, x_test, y_train, y_test = train_test_split(X, Y, train_size=0.8, random_state=42)
print(x_train.shape, y_train.shape)
print(x_test.shape, y_test.shape)

from keras.models import Sequential

model = tf.keras.Sequential([
    tf.keras.layers.Embedding(input_dim=5000, output_dim=100, input_length=X.shape[1]), # input_dim mengikuti jumlah num_words di tokenizer
    tf.keras.layers.LSTM(64),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.Dense(64, activation='relu'),    
    tf.keras.layers.Dense(5, activation='softmax') # Sesuaikan dengan banyaknya kelas
])

model.compile(loss='categorical_crossentropy', 
              optimizer='adam', 
              metrics=['accuracy'])

class berhenti(tf.keras.callbacks.Callback):
  def on_epoch_end(self, epoch, logs={}):
    if (logs.get('val_accuracy') >= 0.9):
      print('\nalhamdulillah akurasi mencapai lebih 90%')
      self.model.stop_training = True
iniCallback = berhenti()

history = model.fit(x_train, y_train,  
                    epochs = 50, batch_size=64,
                    validation_data = (x_test, y_test), # menampilkan akurasi pengujian data validasi
                    validation_steps = 5,
                    verbose = 2,
                    callbacks = [iniCallback])

import matplotlib.pyplot as plt

acc = history.history['accuracy']
val_acc = history.history['val_accuracy']

loss = history.history['loss']
val_loss = history.history['val_loss']

epochs_range = range(len(acc))

plt.figure(figsize=(20, 8))
plt.subplot(1, 2, 1)
plt.plot(epochs_range, acc, label='Training Accuracy')
plt.plot(epochs_range, val_acc, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.title('Training and Validation Accuracy')

plt.subplot(1, 2, 2)
plt.plot(epochs_range, loss, label='Training Loss')
plt.plot(epochs_range, val_loss, label='Validation Loss')
plt.legend(loc='upper right')
plt.title('Training and Validation Loss')

"""## **Referensi**


1.   [Tutorial Klasifikasi Teks dengan Long Short-term Memory (LSTM): Studi Kasus Teks Review E-Commerce](https://youtu.be/RYI0tqngVy4)
2.   [TensorFlow Tutorial 11 - Text Classification - NLP Tutorial](https://youtu.be/kxeyoyrf2cM)
3.   [Dasar Text Preprocessing dengan Python](https://ksnugroho.medium.com/dasar-text-preprocessing-dengan-python-a4fa52608ffe)
4.   [Fadillahnanda / Membuat-Model-NLP-dengan-TensorFlow-Klasifikasi-Teks-twitter-sentiment-data
](https://github.com/Fadillahnanda/Membuat-Model-NLP-dengan-TensorFlow-Klasifikasi-Teks-twitter-sentiment-data/blob/e59198357686a96eabb778398389cbb0d5c8b995/Proyek_Pertama_Membuat_Model_NLP_dengan_TensorFlow_Klasifikasi_Teks_.ipynb)



"""