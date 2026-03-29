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




model = tf.keras.models.load_model('saved_models/test2')

# Show the model architecture
model.summary()
