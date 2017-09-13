"""
.. module:: Process

Process
*************

:Description: Process



:Authors: bejar


:Version:

:Created on: 31/08/2017 8:26

"""

from __future__ import print_function
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.layers import LSTM
from keras.optimizers import RMSprop, SGD
from keras.utils import np_utils
from sklearn.metrics import confusion_matrix, classification_report

if __name__ == '__main__':
    train = np.loadtxt('ElectricDevices_TRAIN.csv', delimiter=',')
    print(train.shape)
    train_x =  train[:, 1:]
    train_x = np.reshape(train_x,(train_x.shape[0], train_x.shape[1], 1))
    train_y = train[:, 0] - 1
    #print(np.unique(train_y))
    nclasses = len(np.unique(train_y))
    train_y_c = np_utils.to_categorical(train_y, nclasses)
    test= np.loadtxt('ElectricDevices_TEST.csv', delimiter=',')

    print(test.shape)
    test_x = test[:, 1:]
    test_x = np.reshape(test_x,(test_x.shape[0], test_x.shape[1], 1))
    test_y = test[:, 0] - 1
    test_y_c = np_utils.to_categorical(test_y, nclasses)

    lstm_size = 512
    batch_size = 100
    epochs = 50

    model = Sequential()
    model.add(LSTM(lstm_size, input_shape=(train_x.shape[1], 1), implementation=2, dropout=0.2))
#    model.add(LSTM(lstm_size, input_shape=(train_x.shape[0], train_x.shape[1]), implementation=2, dropout=0.2, return_sequences=True))
#    model.add(LSTM(lstm_size, implementation=2, dropout=0.2))
    model.add(Dense(nclasses))
    model.add(Activation('softmax'))

    #optimizer = RMSprop(lr=0.01)
    optimizer = SGD(lr=0.01, momentum=0.95)
    model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])

    model.fit(train_x, train_y_c,
          batch_size=batch_size,
          epochs=epochs,
          validation_data=(test_x, test_y_c))

    score, acc = model.evaluate(test_x, test_y_c, batch_size=batch_size)

    print()
    print('ACC= ',acc)

    test_pred = model.predict_classes(test_x)

    print(confusion_matrix(test_y, test_pred))
    print(classification_report(test_y, test_pred))