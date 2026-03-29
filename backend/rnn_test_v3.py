#-------------------------------------------------------------------
#-------------------------------------------------------------------
#-------------------------------------------------------------------
#-------------------------------------------------------------------
#-------------------------------------------------------------------
# TO USE WITH SINGLE GPU
#-------------------------------------------------------------------
#-------------------------------------------------------------------
#-------------------------------------------------------------------
#-------------------------------------------------------------------
#-------------------------------------------------------------------
#-------------------------------------------------------------------


import csv
import pandas as pd
import os
import os.path
import sys
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
# os.environ["CUDA_VISIBLE_DEVICES"] = "1"
import numpy as np
# import wandb
# from wandb.keras import WandbCallback
import random
# import itertools
# from itertools import permutations
# from itertools import combinations
# import mido
# from mido import MidiFile
import sys
import pprint
import tensorflow as tf
gpu_devices = tf.config.experimental.list_physical_devices('GPU')
# tf.config.experimental.set_memory_growth(gpu_devices[1], True)

from tensorflow import keras
from tensorflow.keras import layers
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import accuracy_score
# import sklearn
import pickle
# import autosklearn
# import autosklearn.classification
# from autosklearn.experimental.askl2 import AutoSklearn2Classifier
# from autosklearn.classification import AutoSklearnClassifier
# from autosklearn.metrics import (accuracy,
#                                  f1,
#                                  roc_auc,
#                                  precision,
#                                  average_precision,
#                                  recall,
#                                  log_loss)

import tf2onnx
import onnx



# wdb = False

gpus = tf.config.experimental.list_physical_devices('GPU')
for gpu in gpus:
  print(gpu)
  tf.config.experimental.set_memory_growth(gpu, True)

# os.environ["WANDB_API_KEY"] = '6f720b3db3f1b25127a1f84f7bc898f79085cdca'



class EarlyStopping(tf.keras.callbacks.Callback):
  def on_epoch_end(self, epoch, logs={}):
    '''
    Stops training when 95% accuracy is reached
    '''
    # Get the current accuracy and check if it is above 95%
    if(logs.get('accuracy') > 0.95):

      # Stop training if condition is met
      print("\nThreshold reached. Stopping training...")
      self.model.stop_training = True

early_stopping = EarlyStopping()


# musician ID
art_id = 52

# name to save the tensorflow model + onnx model
filename = "saved_models/greg"

print(filename)

if ((os.path.exists('sampled_data/train_data_'+ str(art_id) + '.csv')  == True)):
        
    print(" ")
    print(" ")
    print("------------------------------------------------------------------------------------------------------------------------")
    print("------------------------------------------------------------------------------------------------------------------------")
    print(" ")
    print(" ")
    print(art_id)


    # TRAIN DATA------------------------------------------
    # ----------------------------------------------------
    #  read the sampled data from csv
    csvfile_0 = 'sampled_data/train_data_'+ str(art_id) + '.csv'

    df_train = pd.read_csv(csvfile_0, dtype=np.float16)
    df_train = df_train.replace(np.nan,0)
    df_train = df_train.to_numpy()
    print('train data len: ', len(df_train))


    x_train = []
    y_train = []

    for i in range (0, len(df_train)):
        x_train.append(df_train[i][:-1])
        y_train.append(int(df_train[i][-1]))


    num_labels = 3

    print("x_train: \t", len(x_train))
    print("y_train: \t", len(y_train))
    print("len seq: ", len(x_train[0]))
    print("num_labels: ", num_labels)


    x_train = np.asarray(x_train)
    y_train = np.asarray(y_train)

    x_train = np.stack([x_train], axis=2)



    with tf.device('GPU:1'):
      model = keras.Sequential()
      model.add(layers.Masking(mask_value=0, input_shape=(x_train.shape[1], x_train.shape[2])))
      model.add(layers.LSTM(128, return_sequences=True, input_shape=(x_train.shape[1], x_train.shape[2])))
      model.add(layers.GRU(64, return_sequences=True))
      model.add(layers.SimpleRNN(128))
      model.add(layers.Dense(num_labels, activation='relu'))

    # model = keras.Sequential()
    # model.add(layers.Masking(mask_value=0, input_shape=(x_train.shape[1], x_train.shape[2])))
    # model.add(layers.LSTM(64, return_sequences=True, input_shape=(x_train.shape[1], x_train.shape[2])))
    # model.add(layers.GRU(32, return_sequences=True))
    # model.add(layers.SimpleRNN(64))
    # model.add(layers.Dense(num_labels, activation='relu'))


    # model = keras.Sequential()
    # model.add(layers.Masking(mask_value=0, input_shape=(x_train.shape[1], x_train.shape[2])))
    # model.add(layers.LSTM(128, input_shape=(x_train.shape[1], x_train.shape[2])))
    # # model.add(layers.GRU(32)
    # # model.add(layers.SimpleRNN(64))
    # model.add(layers.Dense(num_labels))


      model.compile(optimizer='adam',
          loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
          metrics=['accuracy'])

      model.summary()


      history = model.fit(x_train, 
                  y_train, 
                  epochs=30, 
                  batch_size = 512,
                  callbacks = [early_stopping])


    print(history.history.keys())
    print(history.history['accuracy'])
    print(history.history['loss'])

    # filename = "saved_models/greg"
    model.save(filename)

    onnx_model, _ = tf2onnx.convert.from_keras(model, opset=12)
    onnx.save(onnx_model, filename + ".onnx")










    
    # activations = ['relu', 'sigmoid', 'tanh', 'softmax']
    # batch_sizes = [1024, 512, 256, 128]


    # for act in activations:
    #   for btc in batch_sizes:

    #     # with tf.device('GPU:1'):
    #     model = keras.Sequential()
    #     model.add(layers.Masking(mask_value=0, input_shape=(x_train.shape[1], x_train.shape[2])))
    #     model.add(layers.LSTM(128, return_sequences=True, input_shape=(x_train.shape[1], x_train.shape[2])))
    #     model.add(layers.GRU(64, return_sequences=True))
    #     model.add(layers.SimpleRNN(128))
    #     model.add(layers.Dense(num_labels, activation=act))


    #     model.compile(optimizer='adam',
    #         loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    #         metrics=['accuracy'])


    #     history = model.fit(x_train, 
    #                 y_train, 
    #                 epochs=20, 
    #                 batch_size = btc,
    #                 callbacks = [early_stopping])


    #     print(history.history.keys())
    #     print(history.history['accuracy'])
    #     print(history.history['loss'])


    #     f = open("stats.txt", "a")
    #     f.write("batch size : ")
    #     f.write(str(btc))
    #     f.write("\n")
    #     f.write("activation : ")
    #     f.write(act)
    #     f.write("\n")
    #     f.write("accuracy : ")
    #     f.write(str(history.history['accuracy'][0]))
    #     f.write("\n")
    #     f.write("loss : ")
    #     f.write(str(history.history['loss'][0]))
    #     f.write("\n\n")
    #     f.write("--------------------------------------------")
    #     f.write("\n\n")
    #     f.close()

    #     filename = "saved_models/model_50_" + act + "_" + str(btc)
    #     model.save(filename)

    #     onnx_model, _ = tf2onnx.convert.from_keras(model)
    #     onnx.save(onnx_model, filename + ".onnx")



    # model_name = 'saved_models/model' + str(art_id) + '_10_512_2'
    # model.save(model_name)





    # ppp = model.predict(x_train)
    # for i in range(0, 100):
    #   p = random.randint(0, len(x_train)-1)
    #   print(p, '\t', y_train[p], np.argmax(ppp[p]), '\t', ppp[p])
    #   # wandb.finish()




