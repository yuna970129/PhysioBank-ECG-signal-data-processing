import os
import csv
import gc
import cloudpickle as pickle
import operator

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

size_RR_max = 20

rhythmAnno = []
classAnttd= None

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
    next(reader) # skip first line!
    MLII_index = 1
    if int(fRecords[r][0:3]) == 114:
        MLII_index = 2
    MLII=[]
    for row in reader:
        MLII.append((float(row[MLII_index])))
    f.close()
    
    # preprocess 과정 일단은 생략

    classAnttd= None
    
    for a in annotations:
        if '(' in str(a):
            classAnttd = str(a).split('(')[-1].split('\\')[0]
            if classAnttd not in rhythmAnno:
                rhythmAnno.append(classAnttd)
            if classAnttd not in rhythmDict:
                rhythmDict[classAnttd] = 1
            else:
                rhythmDict[classAnttd] += 1
    
print(rhythmAnno)

