# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 12:16:26 2020

@author: melharchaoui

this script remove all images where the mask is all black. the script compute
the proportion of white on black in an image and return a proportion coef
if the coef equal to zero which means no white portion, the image is deleted
"""

import os
from glob import glob
import nibabel as nib
import numpy as np
#import matplotlib.pyplot as plt
import skimage.io as io
from scipy import stats

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



GT_Zscore_dir=r'C:\Users\zelmouaffek\Desktop\osteo2\GT_Z_score_slices'
mask_dir=r'C:\Users\zelmouaffek\Desktop\osteo2\Mask_slices'


# get list of visible tumour and remove those who are not visible                    
fns = sorted(glob(os.path.join(mask_dir, '*.nii*')))

#save data in a dict
Mask_density_status={}
visible_tumour=[]
not_visible_tumour=[]
# scan all files and compute density coefficient
for fn in fns:
    _, base, ext = split_filename(fn)
    img_nifti = nib.load(fn).get_fdata().astype(np.float64)
    # compute the coef
    d_coef=np.count_nonzero(img_nifti)/img_nifti.size
    short_name=get_short_name(base)
    if d_coef==0.0:
        not_visible_tumour.append(short_name)
        os.remove(fn)
    else:
        visible_tumour.append(short_name)
    # fulfil the dict with related data
    Mask_density_status[base]=d_coef
    
# remove GT correspended
fns = sorted(glob(os.path.join(GT_Zscore_dir, '*.nii*')))

# scan all files and compute density coefficient
for fn in fns:
    _, base, ext = split_filename(fn)
    short_name=get_short_name(base)
    if short_name in not_visible_tumour:
        os.remove(fn)