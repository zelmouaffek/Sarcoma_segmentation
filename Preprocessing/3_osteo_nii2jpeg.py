# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 12:16:26 2020

@author: melharchaoui

this script simply convert ".nii" to ."jpeg" format

"""

import os
from glob import glob
import nibabel as nib
import numpy as np
#import matplotlib.pyplot as plt
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

#Convert all nifitis to JPEG
GT_Zscore_dir=r'C:\Users\zelmouaffek\Desktop\osteo2\GT_Z_score_slices'
mask_dir=r'C:\Users\zelmouaffek\Desktop\osteo2\Mask_slices'

GT_Zscore_jpeg_dir=r'C:\Users\zelmouaffek\Desktop\osteo2\GT_Z_score_jpeg_slices'
mask_jpeg_dir=r'C:\Users\zelmouaffek\Desktop\osteo2\Mask_jpeg_slices'

try:
    fns = glob(os.path.join(GT_Zscore_dir, '*.nii*'))
    for fn in fns:
        _, base, ext = split_filename(fn)
        print(base,ext)
        img_nifti = nib.load(fn).get_fdata().astype(np.float64)
        #I_arr = np.array(img_nifti.dataobj)
        I_arr = np.array(img_nifti)
        I_new = np.flipud(I_arr)
        
        name=base+'.jpeg'
        io.imsave(os.path.join(GT_Zscore_jpeg_dir, name),I_new)
    
    fns = glob(os.path.join(mask_dir, '*.nii*'))
    for fn in fns:
        _, base, ext = split_filename(fn)
        print(base,ext)
        img_nifti = nib.load(fn).get_fdata().astype(np.float64)
        #I_arr = np.array(img_nifti.dataobj)
        I_arr = np.array(img_nifti)
        I_new = np.flipud(I_arr)
        
        name=base+'.jpeg'
        io.imsave(os.path.join(mask_jpeg_dir, name),I_new)

except Exception as e:
    print(e)