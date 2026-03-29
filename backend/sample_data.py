import numpy as np
# import tensorflow as tf
# from tensorflow.keras import layers
# from sklearn.model_selection import train_test_split
import csv
import pandas as pd
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
from tensorflow import keras
import os.path
# import wandb
# from wandb.keras import WandbCallback
import random
import itertools
from itertools import permutations
from itertools import combinations
# import mido
# from mido import MidiFile


art_id = 54
pat_id = 0



def write_files(filename, arr):   
    with open(filename, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(arr)
    f.close()



if os.path.exists('data/' + str(art_id) + '/neg_notes.csv'):

    dir_folder = "data/" + str(art_id)   
    print('--------------------------')
    print(dir_folder)
    print('--------------------------')

    notes = []
    times = []
    labels = []

    print("read data - negatives")
    with open(dir_folder + '/neg_notes.csv')as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
            for row in spamreader:
                notes.append(row)
                labels.append(0)

    with open(dir_folder + '/neg_times.csv')as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
            for row in spamreader:
                times.append(row)


    print("read data - patterns")
    for i in range(0, 30):    
        if(os.path.exists(dir_folder + '/pat' + str(i) + '_notes.csv')):
            with open(dir_folder + '/pat' + str(i) + '_notes.csv')as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
                for row in spamreader:
                    notes.append(row)
                    labels.append(i+1)
                                            
            with open(dir_folder + '/pat' + str(i) + '_times.csv')as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
                for row in spamreader:
                    times.append(row)




    print("len notes ", len(notes))
    print("len times ", len(times))


    for i in range(0, len(notes)):
        for j in range(0, len(notes[i])):
            notes[i][j]=notes[i][j]+1


    num_labels = labels[-1]+1
    print("num labels: ", num_labels)



    #--------------------------------------------------------------sampling
    sampled_notes = []
    sampled_val = []
    max_length = 0
    min_length = 99999

    # for i in range(0, len(notes)):
    #     tmp = []
        # for j in range(0, len(notes[i])):
    #         for k in range(0, int(times[i][j]), 240):
    #             tmp.append(notes[i][j])
    #     sampled_notes.append(tmp)
        
        
    sampled_notes = notes.copy()

    # ln = 0
    for i in range(0, len(sampled_notes)):
        ln = len(sampled_notes[i])
        if(ln > 100) :
            print(ln)
        if ln >= max_length:
            max_length = ln
        elif ln <= min_length:
            min_length = ln
            # print("min", ln, i)

    print("min_length", min_length)
    print("max_length", max_length)



    notes = sampled_notes.copy()
    val_notes = sampled_val.copy()
    #--------------------------------------------------------------sampling
    
    print("data - padding")
    notes = keras.preprocessing.sequence.pad_sequences(notes, maxlen=max_length)
    val_notes = keras.preprocessing.sequence.pad_sequences(val_notes, maxlen=max_length)



    train_file = "sampled_data/train_data_" + str(art_id) + ".csv"
    if os.path.exists(train_file):
        os.remove(train_file)


    
    head = []
    for i in range(0, len(notes[0])):
        head.append(str(i))
    head.append('lbl')

    

    # write_files(train_file, head)
    # for i in range(0, len(notes)):
    #     # tmp = train_data[i].copy()
    #     tmp = []
    #     for j in range(0, len(notes[i])):
    #         tmp.append([notes[i][j], veloc[i][j], times[i][j]])
    #     tmp = np.append(tmp, labels[i])
    #     write_files(train_file, tmp)


    # write_files(val_file, head)
    # for i in range(0, len(val_notes)):
    #     # tmp = val_data[i].copy()
    #     tmp = []
    #     for j in range(0, len(notes[i])):
    #         tmp.append([val_notes[i][j], val_veloc[i][j], val_times[i][j]])
    #     tmp = np.append(tmp, val_labels[i])
    #     write_files(val_file, tmp)



    print("writing to file")
    # FOR SAMPLING!!!-------------------------------------------
    write_files(train_file, head)
    for i in range(0, len(notes)):
        tmp = notes[i].copy()
        # tmp = []
        # for j in range(0, len(notes[i])):
        #     tmp.append(notes[i][j])
        tmp = np.append(tmp, labels[i])
        write_files(train_file, tmp)




