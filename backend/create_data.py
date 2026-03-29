import numpy as np
# import tensorflow as tf
# from tensorflow import keras
# from tensorflow.keras import layers
# from sklearn.model_selection import train_test_split
import csv
import pandas as pd
import os
import os.path
# import wandb
# from wandb.keras import WandbCallback
import random
import itertools
from itertools import permutations
from itertools import combinations
import mido
from mido import MidiFile


aug_chg = 50
var_chg = 50


art_id = 54
pat_id = 0



def read_file(path):
    # print("reading file")
    cur_not = 0
    cur_vel = 0
    cur_ptc = 0
    abs_tim = 0  
    seq_not = []
    seq_vel = []
    seq_tim = []
    mid = MidiFile(path)
    for i in range(0, len(mid.tracks)):
        for j in range(0, len(mid.tracks[i])-1):
            msg = mid.tracks[i][j]
            
            if(msg.type=='note_on') and (msg.velocity>0):
                cur_not = float(msg.note)
                cur_vel = msg.velocity
                cur_tim = mid.tracks[i][j+1].time
                seq_not.append(cur_not)
                seq_vel.append(cur_vel)
                seq_tim.append(cur_tim)
                
            if(msg.type=='note_on' and msg.velocity==0) or (msg.type=='note_off'):
                if(mid.tracks[i][j+1].time > 0):
                    cur_not = float(0)
                    cur_vel = 0
                    cur_tim = mid.tracks[i][j+1].time
                    seq_not.append(cur_not)
                    seq_vel.append(cur_vel)
                    seq_tim.append(cur_tim)
            
            if(msg.type=='pitchwheel'):
                cur_tim = mid.tracks[i][j+1].time
                seq_not.append(cur_not)
                seq_vel.append(cur_vel)
                seq_tim.append(cur_tim)

            if(msg.type=='modulation'):
                cur_tim = mid.tracks[i][j+1].time
                seq_not.append(cur_not)
                seq_vel.append(cur_vel)
                seq_tim.append(cur_tim)

            # if(msg.type=='pitchwheel') and (cur_not!=0):
            #     cur_ptc = msg.pitch
            #     tmp_not = cur_not + cur_ptc/8192
            #     cur_tim = mid.tracks[i][j+1].time
            #     seq_not.append(tmp_not)
            #     seq_vel.append(cur_vel)
            #     seq_tim.append(cur_tim)

    return seq_not, seq_vel, seq_tim


def sample_file(path):
    # print("reading file")
    cur_not = 0
    cur_vel = 0
    cur_ptc = 0
    abs_tim = 0  
    seq_not = []
    seq_vel = []
    seq_tim = []
    mid = MidiFile(path)
    for i in range(1, 2):
        for j in range(0, len(mid.tracks[i])-1):
            msg = mid.tracks[i][j]
            
            if(msg.type=='note_on') and (msg.velocity>0):
                cur_not = float(msg.note)
                cur_vel = msg.velocity
                cur_tim = mid.tracks[i][j+1].time
                for k in range(0, mid.tracks[i][j+1].time):
                    seq_not.append(cur_not)
                # seq_not.append(cur_not)
                # seq_vel.append(cur_vel)
                # seq_tim.append(cur_tim)
                
            if(msg.type=='note_on' and msg.velocity==0) or (msg.type=='note_off'):
                if(mid.tracks[i][j+1].time > 0):
                    cur_not = float(0)
                    cur_vel = 0
                    cur_tim = mid.tracks[i][j+1].time
                    for k in range(0, mid.tracks[i][j+1].time):
                        seq_not.append(cur_not)
                    # seq_not.append(cur_not)
                    # seq_vel.append(cur_vel)
                    # seq_tim.append(cur_tim)

            if(msg.type=='pitchwheel'):
                cur_tim = mid.tracks[i][j+1].time
                seq_not.append(cur_not)
                seq_vel.append(cur_vel)
                seq_tim.append(cur_tim)

            if(msg.type=='modulation'):
                cur_tim = mid.tracks[i][j+1].time
                seq_not.append(cur_not)
                seq_vel.append(cur_vel)
                seq_tim.append(cur_tim)
            
            # if(msg.type=='pitchwheel') and (cur_not!=0):
            #     cur_ptc = msg.pitch
            #     tmp_not = cur_not + cur_ptc/8192
            #     cur_tim = mid.tracks[i][j+1].time
            #     for k in range(0, mid.tracks[i][j+1].time):
            #         seq_not.append(tmp_not)
                # seq_not.append(tmp_not)
                # seq_vel.append(cur_vel)
                # seq_tim.append(cur_tim)
    return seq_not, seq_vel, seq_tim


#---------------------------------------------------------------------------
def write_files(filename, arr):   
    with open(filename, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(arr)
    f.close()

#---------------------------------------------------------------------------
def augment(notes_arr, veloc_arr, times_arr, notes_file, veloc_file, times_file, aug):
    tmp_not = notes_arr.copy()
    tmp_vel = veloc_arr.copy()
    tmp_tim = times_arr.copy()
    write_files(notes_file, tmp_not)
    write_files(veloc_file, tmp_vel)
    write_files(times_file, tmp_tim)
    # aug = False
    aug_no = 0

    if(aug == True):
        # # velocity changes
        # for h in range(0, aug_chg):
        #     tmp_not = notes_arr.copy()
        #     tmp_vel = veloc_arr.copy()
        #     tmp_tim = times_arr.copy()
        #     rd1 = random.randint(1, len(tmp_not))    #number of notes
        #     for i in range(0, rd1):
        #         rd2 = random.randint(0, len(tmp_not)-1)  #note
        #         rd3 = random.randint(-10,10)   #velocity change
        #         if(tmp_vel[rd2]+rd3>0 and tmp_vel[rd2]+rd3<127):
        #             tmp_vel[rd2] = tmp_vel[rd2]+rd3
        #     write_files(notes_file, tmp_not)
        #     write_files(veloc_file, tmp_vel)
        #     write_files(times_file, tmp_tim)
            
    #     duration changes    
        for h in range(0, aug_chg):
            tmp_not = notes_arr.copy()
            tmp_vel = veloc_arr.copy()
            tmp_tim = times_arr.copy()
            rd1 = random.randint(1, len(tmp_not))    #number of notes
            for i in range(0, rd1):
                rd2 = random.randint(0, len(tmp_not)-1)  #note
                rd3 = random.randint(-10,10)   #duration change
                if(tmp_tim[rd2]+rd3>0):
                    tmp_tim[rd2] = tmp_tim[rd2]+rd3
            write_files(notes_file, tmp_not)
            write_files(veloc_file, tmp_vel)
            write_files(times_file, tmp_tim)
            aug_no = aug_no+1
            
    #     transpositions
        # for i in range(-3,4):
        #     tmp_not = notes_arr.copy()
        #     tmp_vel = veloc_arr.copy()
        #     tmp_tim = times_arr.copy()
        #     for j in range(0, len(tmp_not)):
        #         tmp_not[j] = tmp_not[j]+1
        #     write_files(notes_file, tmp_not)
        #     write_files(veloc_file, tmp_vel)
        #     write_files(times_file, tmp_tim)

    



def write_val_data(seq_not, seq_vel, seq_tim, pat_id, dir_folder):
    seq_not_spl = seq_not.copy()
    seq_vel_spl = seq_vel.copy()
    seq_tim_spl = seq_tim.copy()

    pat_val = dir_folder + "/val_notes.csv"
    vel_val = dir_folder + "/val_veloc.csv"
    tim_val = dir_folder + "/val_times.csv"
    lbl_val = dir_folder + "/val_labels.csv"

    write_files(pat_val, seq_not_spl)
    write_files(vel_val, seq_vel_spl)
    write_files(tim_val, seq_tim_spl)
    write_files(lbl_val, [pat_id+1])

    




def create_variations(seq_not, seq_vel, seq_tim, pat_id, dir_folder):
    pp = 0
    print("creating variations")
    pat_file = dir_folder + "/pat" + str(pat_id) + "_notes.csv"
    vel_file = dir_folder + "/pat" + str(pat_id) + "_veloc.csv"
    tim_file = dir_folder + "/pat" + str(pat_id) + "_times.csv"

    # if(os.path.exists(pat_file)):
    #     os.remove(pat_file)
    # if(os.path.exists(vel_file)):
    #     os.remove(vel_file)
    # if(os.path.exists(tim_file)):
    #     os.remove(tim_file)

    seq_not_spl = seq_not.copy()
    seq_vel_spl = seq_vel.copy()
    seq_tim_spl = seq_tim.copy()

    # double notes - starting from one note until all notes
    for i in range(1, var_chg):
        tmp_not = seq_not_spl.copy()
        tmp_vel = seq_vel_spl.copy()
        tmp_tim = seq_tim_spl.copy()
        r1 = random.randint(0, int(len(seq_not_spl)*0.25))  #random number of notes
        for j in range(0, r1):
            r2 = random.randint(0, len(seq_not_spl)-1)  #randomly selected note index
            tmp_not.insert(r2+1, tmp_not[r2])
            tmp_vel.insert(r2+1, tmp_vel[r2])
            tmp_tim[r2] = int(tmp_tim[r2]/2)
            tmp_tim.insert(r2+1, tmp_tim[r2])
        augment(tmp_not, tmp_vel, tmp_tim, pat_file, vel_file, tim_file, True)
        pp=pp+1

    # remove up to 25% of the notes
    for i in range(1, var_chg):
        tmp_not = seq_not_spl.copy()
        tmp_vel = seq_vel_spl.copy()
        tmp_tim = seq_tim_spl.copy()
        r1 = random.randint(0, len(seq_not_spl)-1)  #random number of notes
        for j in range(0, r1):
            r2 = random.randint(0, len(tmp_not)-1)  #randomly selected note index
            tmp_not.pop(r2)
            tmp_vel.pop(r2)
            tmp_tim.pop(r2)
        augment(tmp_not, tmp_vel, tmp_tim, pat_file, vel_file, tim_file, True)
        pp=pp+1

    # halve every note
    for i in range(1, var_chg):
        tmp_not = seq_not_spl.copy()
        tmp_vel = seq_vel_spl.copy()
        tmp_tim = seq_tim_spl.copy()
        r1 = random.randint(0, len(seq_not_spl)-1)  #random number of notes
        for j in range(0, r1):
            r2 = random.randint(0, len(tmp_not)-1)  #randomly selected note index
            tmp_tim[r2] = int(tmp_tim[r2]*0.5)
        augment(tmp_not, tmp_vel, tmp_tim, pat_file, vel_file, tim_file, True)
        pp=pp+1

    # insert randomly selected notes from the pattern to random locations in the pattern
    for i in range(0, var_chg):
        tmp_not = seq_not_spl.copy()
        tmp_vel = seq_vel_spl.copy()
        tmp_tim = seq_tim_spl.copy()
        for j in (0, random.randint(0, int(len(tmp_not)*0.3))): # select a random number of notes to add
            rd1 = seq_not_spl[random.randint(0, len(seq_not_spl)-1)]      # note to add
            rd2 = random.randint(0, len(tmp_not))            #index of destination
            tmp = [seq_tim_spl[k] for k in range(len(seq_tim_spl))]
            rd3 = random.randint(min(tmp), max(tmp))               #length of random note
            rd4 = random.randint(20,127)         #velocity of random note
            tmp_not.insert(rd2, rd1)
            if (rd1 == 0):
                tmp_vel.insert(rd2, 0)
            else:
                tmp_vel.insert(rd2, rd4)
            # tmp_tim[rd2] = int(tmp_tim[rd2]/2)
            tmp_tim.insert(rd2, rd3)
        augment(tmp_not, tmp_vel, tmp_tim, pat_file, vel_file, tim_file, True)
        pp=pp+1

    # insert random notes from the ouside the pattern, but within the boundary of its min and max, to random locations in the pattern
    tmp0 = [i for i in seq_not_spl if i != 0]   # list of all the notes in pattern, minus zero
    tmp1 = list(set([i for i in range(int(min(tmp0)), int(max(tmp0))+1)]) - set(tmp0))   # list of all other notes between the min note and the max note
    for i in range(0, var_chg):
        tmp_not = seq_not_spl.copy()
        tmp_vel = seq_vel_spl.copy()
        tmp_tim = seq_tim_spl.copy()
        for j in (0, random.randint(0, int(len(tmp_not)*0.3))): # select a random number of notes to add
            rd1 = tmp1[random.randint(0, len(tmp1)-1)]     # note to add
            rd2 = random.randint(0, len(tmp_not))            #index of destination
            tmp = [seq_tim_spl[k] for k in range(len(seq_tim_spl))]
            rd3 = random.randint(min(tmp), max(tmp))               #length of random note
            rd4 = random.randint(20,127)         #velocity of random     note
            tmp_not.insert(rd2, rd1)
            if (rd1 == 0):
                tmp_vel.insert(rd2, 0)
            else:
                tmp_vel.insert(rd2, rd4)
            # tmp_tim[rd2] = int(tmp_tim[rd2]/2)
            tmp_tim.insert(rd2, rd3)
        augment(tmp_not, tmp_vel, tmp_tim, pat_file, vel_file, tim_file, True)
        pp=pp+1

    # swap two notes
    for i in range(0, len(seq_not_spl)-1):
        tmp_not = seq_not_spl.copy()
        tmp_vel = seq_vel_spl.copy()  
        tmp_tim = seq_tim_spl.copy()
        tmp = tmp_not[i]
        del(tmp_not[i])
        tmp_not.insert(i+1, tmp)
        tmp = tmp_vel[i]
        del(tmp_vel[i])
        tmp_vel.insert(i+1, tmp)
        tmp = tmp_tim[i]
        del(tmp_tim[i])
        tmp_tim.insert(i+1, tmp)
        augment(tmp_not, tmp_vel, tmp_tim, pat_file, vel_file, tim_file, True)
        pp=pp+1

    # transpose one note by an octave
    for i in range(0, len(seq_not_spl)):
        tmp_not = seq_not_spl.copy()
        tmp_vel = seq_vel_spl.copy()     
        tmp_tim = seq_tim_spl.copy()
        rd1 = random.randint(0, len(tmp_not)-1)
        if(tmp_not[rd1] < 127-12):
            tmp_not[rd1] = tmp_not[rd1]+12
        augment(tmp_not, tmp_vel, tmp_tim, pat_file, vel_file, tim_file, True)
        pp=pp+1

    return pp





# max_pat_len = 0
# min_pat_len = 9999999
total_pat = 0


dir_folder = "data/" + str(art_id)
if os.path.exists(dir_folder) == False:
    os.mkdir(dir_folder)


for pat_id in range(0, 10):
    if(os.path.exists(dir_folder + "/pat" + str(pat_id) + "_notes.csv")):
        os.remove(dir_folder + "/pat" + str(pat_id) + "_notes.csv")
    if(os.path.exists(dir_folder + "/pat" + str(pat_id) + "_veloc.csv")):
        os.remove(dir_folder + "/pat" + str(pat_id) + "_veloc.csv")
    if(os.path.exists(dir_folder + "/pat" + str(pat_id) + "_times.csv")):
        os.remove(dir_folder + "/pat" + str(pat_id) + "_times.csv")


    max_pat_len = 0
    min_pat_len = 9999999


    pat_filename = 'midi_in/' + str(art_id) + '_' + str(pat_id) + '_0.mid'
    if os.path.exists(pat_filename):
        print(pat_filename)
        print("CREATING VARIATIONS")
        seq_not, seq_vel, seq_tim = read_file(pat_filename)
        print("Pattern ", pat_id, " length : ", len(seq_not))
        ppp = create_variations(seq_not, seq_vel, seq_tim, pat_id, dir_folder)
        total_pat = total_pat+ppp

        if(len(seq_not) >= max_pat_len):
            max_pat_len = len(seq_not)
        if(len(seq_not) <= min_pat_len):
            min_pat_len = len(seq_not)


        # max_pat_len = int(min_pat_len*1.2)
        # min_pat_len = int(min_pat_len*0.8)

        print("min_pat_len", min_pat_len)
        print("max_pat_len", max_pat_len)


        print("CREATING NEGATIVES")
        neg_pat_file = dir_folder + "/neg_notes.csv"
        neg_vel_file = dir_folder + "/neg_veloc.csv"
        neg_tim_file = dir_folder + "/neg_times.csv"

        if(os.path.exists(neg_pat_file)):
            os.remove(neg_pat_file)
        if(os.path.exists(neg_vel_file)):
            os.remove(neg_vel_file)
        if(os.path.exists(neg_tim_file)):
            os.remove(neg_tim_file)
        

        notes_dict = []
        for i in range(1,127):
            notes_dict.append(i)
        for i in range(0,50):
            notes_dict.append(0)
            
        # for h in range(0, int(total_pat)):
        for h in range(0, 15000):
            tmp_not = []
            tmp_vel = []
            tmp_tim = []
            ln = random.randint(4, max_pat_len)
            #adding the first note
            tmp_not.append(notes_dict[random.randint(0, 126)])
            tmp_vel.append(random.randint(30, 128))
            tmp_tim.append(random.randint(10, 30))
            for j in range(0, ln):
                note = notes_dict[random.randint(0, len(notes_dict)-1)]
                dur = random.randint(10, 30)
                if(note==0 and tmp_not[-1]!=0):
                    tmp_not.append(0)
                    tmp_vel.append(0)
                    tmp_tim.append(dur)
                else:
                    tmp_not.append(note)
                    tmp_vel.append(random.randint(30, 128))
                    tmp_tim.append(dur)
            augment(tmp_not, tmp_vel, tmp_tim, neg_pat_file, neg_vel_file, neg_tim_file, False)


        

        # for h in range(0, 20):
        #     tmp_not = []
        #     tmp_vel = []
        #     tmp_tim = []
        #     seq_not_spl = seq_not.copy()
        #     seq_vel_spl = seq_vel.copy()
        #     seq_tim_spl = seq_tim.copy()
        #     for i in range(0, int(len(seq_not)/2)):
        #         for j in range(0, i):
        #             tmp_not.append(notes_dict[random.randint(0, 126)])
        #             tmp_vel.append(random.randint(30, 128))
        #             tmp_tim.append(random.randint(10, 30))
        #         for j in range(i, i+int(len(seq_not)/2)):
        #             tmp_not.append(seq_not_spl[j])
        #             tmp_vel.append(seq_vel_spl[j])
        #             tmp_tim.append(seq_tim_spl[j])
        #         for j in range(i+int(len(seq_not)/2), len(seq_not)):
        #             tmp_not.append(notes_dict[random.randint(0, 126)])
        #             tmp_vel.append(random.randint(30, 128))
        #             tmp_tim.append(random.randint(10, 30))
        #         augment(tmp_not, tmp_vel, tmp_tim, neg_pat_file, neg_vel_file, neg_tim_file, False)



        metadata_file = dir_folder + "/meta.csv"
        write_files(metadata_file, [total_pat])
        write_files(metadata_file, [min_pat_len])
        write_files(metadata_file, [max_pat_len])