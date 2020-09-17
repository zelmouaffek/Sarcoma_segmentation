# -*- coding: utf-8 -*-
"""
Created on Tue May  5 12:07:19 2020

@author: melharchaoui

This script perfome the transformation from ".img" format to ".nii" format of all images.
there is two kind of image, patien IRM and thier correspending mask
note that each image is stocked in independent folder that has the number of patient
the script apply also some operation to images before transformation which are
zero padding and z_score
"""



import os
from pathlib import Path
import nibabel as nib
import numpy as np
#import matplotlib.pyplot as plt
import skimage.io as io
from scipy import stats
import cv2


def zero_padd(im_array, new_size) :
    
    desired_size = (new_size)

    #I_nifti=nib.load(path_to_image)

    #im = np.array(I_nifti.dataobj)
    old_size = im_array.shape[:2] # old_size is in (height, width) format

    ratio = float(desired_size)/max(old_size)
    new_size = tuple([int(x*ratio) for x in old_size])

    # new_size should be in (width, height) format

    im_array = cv2.resize(im_array, (new_size[1], new_size[0]))

    delta_w = desired_size - new_size[1]
    delta_h = desired_size - new_size[0]
    top, bottom = delta_h//2, delta_h-(delta_h//2)
    left, right = delta_w//2, delta_w-(delta_w//2)

    color = [0, 0, 0]
    new_im = cv2.copyMakeBorder(im_array, top, bottom, left, right, cv2.BORDER_CONSTANT,
                                value=color)
    #new_image = nib.Nifti1Image(new_im , affine=np.eye(4))
    return new_im

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


# List all files in a directory using scandir()
basepath = Path(r'C:\Users\zelmouaffek\Desktop\osteo2\GT_and_mask_nifti')
GT_Zscore_dir=r'C:\Users\zelmouaffek\Desktop\osteo2\GT_Z_score_slices'
mask_dir=r'C:\Users\zelmouaffek\Desktop\osteo2\Mask_slices'
for entry in basepath.iterdir():
    #print(entry.name)
    for subentry in entry.iterdir():
        #print(subentry.name)
        if subentry.name=='Data':
            #print(subentry.name)
            for file in subentry.iterdir():
                #print(file)
                if file.name.endswith('.img'):
                    #print(file.name)
                    img_data = nib.load(file)
                    img_data = img_data.get_fdata()
                    slices_n=img_data.shape[2]
                    for i in range(slices_n):
                        im_slice=img_data[:,:,i]
                        #apply Z_score
                        im_slicez=stats.zscore(im_slice,axis=None)
                        # apply the zero padding
                        im_slicez_zp=zero_padd(im_slicez,512)
                        # convert back to nifiti
                        im_slicez=nib.Nifti1Image(im_slicez_zp,affine=np.eye(4))
                        #save data in format name 'Osteo_patient_number_GT_slice_nbr
                        j=int(entry.name)+55
                        name='Osteo_'+str(j)+'_GT_Zscore_slice_'+str(i)+'.nii'
                        print(name)
                        #io.imsave(os.path.join(GT_Zscore_dir,name) ,im_slicez)
                        nib.save(im_slicez, os.path.join(GT_Zscore_dir,name))
                elif file.name.endswith('.gz'):
                    img_data = nib.load(file)
                    img_data = img_data.get_fdata()
                    slices_n=img_data.shape[2]
                    for i in range(slices_n):
                        im_slice=img_data[:,:,i]
                        #apply Z_score
                        im_slicez=stats.zscore(im_slice,axis=None)
                        # apply the zero padding
                        im_slicez_zp=zero_padd(im_slicez,512)
                        # convert back to nifiti
                        im_slicez=nib.Nifti1Image(im_slicez_zp,affine=np.eye(4))
                        #save data in format name 'Osteo_patient_number_GT_slice_nbr
                        name='Osteo_'+entry.name+'_GT_Zscore_slice_'+str(i)+'.nii'
                        print(name)
                        #io.imsave(os.path.join(GT_Zscore_dir,name) ,im_slicez)
                        nib.save(im_slicez, os.path.join(GT_Zscore_dir,name))
        if subentry.name=='Mask':
            #print(subentry.name)
            for file in subentry.iterdir():
                #print(file)
                if file.name.endswith('.nii'):
                    #print(file.name)
                    img_data = nib.load(file)
                    img_data = img_data.get_fdata()
                    slices_n=img_data.shape[2]
                    for i in range(slices_n):
                        im_slice=img_data[:,:,i]
                        
                        # apply the zero padding
                        im_slice_zp=zero_padd(im_slice,512)
                        im_slice=nib.Nifti1Image(im_slice_zp,affine=np.eye(4))

                        #save data in format name 'Osteo_patient_number_Mask_slice_nbr
                        j=int(entry.name)+55
                        name='Osteo_'+str(j)+'_Mask_slice_'+str(i)+'.nii'
                        print(name)
                        #io.imsave(os.path.join(mask_dir,name) ,im_slice)
                        nib.save(im_slice, os.path.join(mask_dir,name))