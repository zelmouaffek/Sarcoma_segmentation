# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 12:16:26 2020

@author: melharchaoui

this script allow the creation of datasets in ".tif" format of training, labels,
and test volumes. it also split the dataset based on number of patients
"""


import os
from pathlib import Path
from glob import glob
import nibabel as nib
import numpy as np
import skimage.io as io


def split_filename(filepath):
    path = os.path.dirname(filepath)
    filename = os.path.basename(filepath)
    base, ext = os.path.splitext(filename)
    if ext == '.gz':
        base, ext2 = os.path.splitext(base)
        ext = ext2 + ext
    return path, base, ext

def get_short_name(base):
    base_l = base.split('_')
    return base_l[1]+base_l[-1]

def get_patient_id(base):
    base_l = base.split('_')
    return base_l[1]

GT_Zscore_jpeg_dir=r'C:\Users\zelmouaffek\Desktop\osteo2\GT_Z_score_jpeg_slices'
mask_jpeg_dir=r'C:\Users\zelmouaffek\Desktop\osteo2\Mask_jpeg_slices'
dataset_tif=r'C:\Users\zelmouaffek\Desktop\osteo2\dataset_tif'

# get how many patient we have
fns = sorted(glob(os.path.join(GT_Zscore_jpeg_dir, '*.jpeg*')))
patients=set()
for fn in fns:
    _, base, ext = split_filename(fn)
    patient_id=get_patient_id(base)
    patients.add(patient_id)

patients=list(patients)
#select Training, test and Label
len_pall=len(patients)
train_plen=int(len_pall*0.7)
train_plst=patients[0:train_plen]
test_plst=patients[train_plen:]

train_lst=[]
for fn in fns:
    _, base, ext = split_filename(fn)
    patient_id=get_patient_id(base)
    short_name=get_short_name(base)
    if patient_id in train_plst:
        train_lst.append(short_name)

len_all=len(fns)
train_len=len(train_lst)
try:
    #Prepare Train-volume & test-volume
    fns = sorted(glob(os.path.join(GT_Zscore_jpeg_dir, '*.jpeg*')))
    stack_train = np.zeros((train_len,512,512),np.uint8)
    stack_test = np.zeros((len_all-train_len,512,512),np.uint8)
    n_train=0
    n_test=0
    for fn in fns:
        _, base, ext = split_filename(fn)
        print(base,ext)
        short_name=get_short_name(base)
        I=io.imread(fn)
        if short_name in train_lst:
            stack_train[n_train,:,:]= I
            n_train+=1
        else:
            stack_test[n_test,:,:]= I
            n_test+=1
    io.imsave(os.path.join(dataset_tif,'train-volume.tif') ,stack_train)
    io.imsave(os.path.join(dataset_tif,'test-volume.tif') ,stack_test) 
    
    
    #Prepare Train-label & test-label
    fns = sorted(glob(os.path.join(mask_jpeg_dir, '*.jpeg*')))
    stack_train = np.zeros((train_len,512,512),np.uint8)
    stack_test = np.zeros((len_all-train_len,512,512),np.uint8)
    n_train=0
    n_test=0
    for fn in fns:
        _, base, ext = split_filename(fn)
        print(base,ext)
        short_name=get_short_name(base)
        I=io.imread(fn)
        if short_name in train_lst:
            stack_train[n_train,:,:]= I
            n_train+=1
        else:
            stack_test[n_test,:,:]= I
            n_test+=1
    io.imsave(os.path.join(dataset_tif,'train-labels.tif') ,stack_train)
    io.imsave(os.path.join(dataset_tif,'test-labels.tif') ,stack_test) 

except Exception as e:
    print(e)