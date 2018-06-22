'''
A Recurrent Neural Network (LSTM) implementation example using TensorFlow library.
This example is using the MNIST database of handwritten digits (http://yann.lecun.com/exdb/mnist/)
'''

from __future__ import absolute_import, division, print_function

from tensorflow.python.keras.preprocessing import sequence
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense, Embedding
from tensorflow.python.keras.layers import LSTM
from tensorflow.python.keras.datasets import imdb

from tensorflow.python.keras.optimizers import Adam

data_size = 20000
input_size = 128
maxlen = 80  # cut texts after this number of words (among top max_features most common words)

params = {'batch_size':32,
          'dropout':0.2,
          'recurrent_dropout':0.2,
          'activation':'sigmoid',
          'loss':'binary_crossentropy',
          'optimizer':Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False),
          'metrics':['accuracy'],
          'epochs':10,
          }

print('Loading data...')
(x_train, y_train), (x_test, y_test) = imdb.load_data(num_words=data_size) #20000 is max_features
print(len(x_train), 'train sequences')
print(len(x_test), 'test sequences')

print('Pad sequences (samples x time)')
x_train = sequence.pad_sequences(x_train, maxlen=maxlen)
x_test = sequence.pad_sequences(x_test, maxlen=maxlen)
print('x_train shape:', x_train.shape)
print('x_test shape:', x_test.shape)

print('Build model...')
model = Sequential()
model.add(Embedding(data_size, input_size))

model.add(LSTM(input_size, dropout=params['dropout'], recurrent_dropout=params['recurrent_dropout']))
model.add(Dense(1, activation=params['activation']))

# try using different optimizers and different optimizer configs
model.compile(loss=params['loss'],
              optimizer=params['optimizer'],
              metrics=params['metrics'])

print('Train...')
model.fit(x_train, y_train,
          batch_size=params['batch_size'],
          epochs=params['epochs'],
          validation_data=(x_test, y_test))
score, acc = model.evaluate(x_test, y_test,
                            batch_size=params['batch_size'])
print('Test score:', score)
print('Test accuracy:', acc)
