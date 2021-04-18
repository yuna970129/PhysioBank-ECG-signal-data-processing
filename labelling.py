import os
import csv
import gc
import cloudpickle as pickle
import operator
import pandas as pd

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import medfilt
import scipy.stats
import pywt
import time
import sklearn
from sklearn import decomposition
from sklearn.decomposition import PCA, IncrementalPCA

from tqdm.notebook import tqdm

path = 'C:/Users/CSD/Desktop/CPR_project/mitdb_mV'

# the records with paced beats were not considered (102, 104, 107, and 217)
DS = [101, 106, 108, 109, 112, 114, 115, 116, 118, 119, 122, 124, 201, 203, 205, 207, 208, 209, 215, 220, 223, 230, 100, 103, 105,
      111, 113, 117, 121, 123, 200, 202, 210, 212, 213, 214, 219, 221, 222, 228, 231, 232, 233, 234]

fRecords = list()
fAnnotations = list()
lst = os.listdir(path)
lst.sort()

for file in lst:
    if file.endswith(".csv"):
        if int(file[0:3]) in DS:
            fRecords.append(file)
    elif file.endswith(".txt"):
        if int(file[0:3]) in DS:
            fAnnotations.append(file)  

# non-shockable_index: 0, shockable_index: 1
rhythm_classes = [['N', 'B', 'T', 'SVTA', 'NOD', 'IVR', 'AFIB', 'AFL', 'AB', 'PREX', 'BII', 'SBR'], ['VFL', 'VT']]
class_ID = [[] for i in range(len(DS))]
R_poses = [ np.array([]) for i in range(len(DS))]

for r in range(0, len(fRecords)):
    filename = path + "/" + fAnnotations[r]
    f = open(filename, 'rb')
    next(f) # skip first line!

    annotations = []
    for line in f:
        annotations.append(line)
    f.close
    
    filename = path + "/" + fRecords[r]
    f = open(filename, 'rt')
    reader = csv.reader(f, delimiter=',')
    next(reader) # skip first line
    MLII_index = 1
    if int(fRecords[r][0:3]) == 114:
        MLII_index = 2
    MLII=[]
    for row in reader:
        MLII.append((float(row[MLII_index])))
    f.close()

    for a in annotations:
        aS = a.split()
        pos = int(aS[1])
        
        if '(' in str(a):
            classAnttd = str(a).split('(')[-1].split('\\')[0]
            
            for i in range(0,len(rhythm_classes)):
                if classAnttd in rhythm_classes[i]:
                    class_AAMI = i
                    break 
            class_ID[r].append(class_AAMI)

            R_poses[r] = np.append(R_poses[r], pos)
            
for r in range(len(DS)):
    print(r)
    R_poses[r] = list(R_poses[r])
    class_ID[r].insert(0, class_ID[r][0])
    R_poses[r].insert(0, 0)
    
    difference = []
    for i in range(0, len(R_poses[r])-1):
        difference.append(R_poses[r][i+1]-R_poses[r][i])
    print('1')
    label = []
    for i in range(0, len(difference)):
        label += [class_ID[r][i]] * int(difference[i])
    label += [class_ID[r][-1]] * int(len(MLII) - R_poses[r][-1])
    print(len(label))
    df = pd.read_csv('./' +str(fRecords[r][0:3])+ '.csv')
    print('1.6')
    df.head()
    df['classes'] = np.nan
    for i in tqdm(range(0, len(label))):
        df.loc[i, ['classes']] = label[i]
    print('2')
    df.to_csv('C:/Users/CSD/Desktop/CPR_project/mitdb_label_mV/'+ str(fRecords[r][0:3]) +'_rhythm' +'.csv', index = False, header=True)
    print(str(fRecords[r][0:3]) + ' done')