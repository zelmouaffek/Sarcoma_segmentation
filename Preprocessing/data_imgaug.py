# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 12:27:08 2020

@author: zelmouaffek
"""



import imgaug.augmenters as iaa
import skimage.io as io
import numpy as np
train_len=len(io.imread("C:\\Users\\zelmouaffek\\Desktop\\Data_Lipos\\\dataset_tif\\train-volume.tif"))
stack_im=io.imread("C:\\Users\\zelmouaffek\\Desktop\\Data_Lipos\\dataset_tif\\train-volume.tif")
satck_mask=io.imread("C:\\Users\\zelmouaffek\\Desktop\\Data_Lipos\\dataset_tif\\train-labels.tif")
#empty list with the size of the new number of training images
stack_train = np.zeros((3504,512,512),np.uint8)
stack_labels = np.zeros((3504,512,512),np.uint8)

#Loop to ass to the new stacks the original images
for i in range(2732):
    stack_train[i,:,:]= stack_im[i,:,:]
    stack_labels[i,:,:]= satck_mask[i,:,:]
    print(3904-i)

#Data augmentation applied(elastic_transformm + noise )
seq = iaa.Sequential([
    iaa.Fliplr(0.5), # horizontal flips
    iaa.Crop(percent=(0, 0.1)), # random crops
    # Small gaussian blur with random sigma between 0 and 0.5.
    # But we only blur about 50% of all images.
    iaa.Sometimes(
        0.5,
        iaa.GaussianBlur(sigma=(0, 0.5))
    ),
    # Strengthen or weaken the contrast in each image.
    iaa.LinearContrast((0.75, 1.5)),
    # Add gaussian noise.
    # For 50% of all images, we sample the noise once per pixel.
    # For the other 50% of all images, we sample the noise per pixel AND
    # channel. This can change the color (not only brightness) of the
    # pixels.
    iaa.AdditiveGaussianNoise(loc=0, scale=(0.0, 0.05*255), per_channel=0.5),
    # Make some images brighter and some darker.
    # In 20% of all cases, we sample the multiplier once per channel,
    # which can end up changing the color of the images.
    iaa.Multiply((0.8, 1.2), per_channel=0.2),
    # Apply affine transformations to each image.
    # Scale/zoom them, translate/move them, rotate them and shear them.
    iaa.Affine(
        scale={"x": (0.8, 1.2), "y": (0.8, 1.2)},
        translate_percent={"x": (-0.2, 0.2), "y": (-0.2, 0.2)},
        rotate=(-25, 25),
        shear=(-8, 8)
    )
], random_order=True)

#apply the data augmentation to the training images
images=[]
for i in range(2732,3504):
    images.append(stack_im[i-2732])
images_seq= seq(images=images)

#apply the data augmentation to the training masks
images=[]
for i in range(2732,3504):
    images.append(satck_mask[i-2732])
masks_affine = seq(images=images)


#fill the blank in the stack with the new images
for i in range(2732,3504):
   
    stack_train[i,:,:]= images_seq[i-2732]
    stack_labels[i,:,:]= masks_affine[i-2732]
    print(3904-i)

    
    

 #Save the new stacks   
io.imsave('C:\\Users\\zelmouaffek\\Desktop\\\\Data_Lipos\\\dataset_tif\\train-volume_7.tif',stack_train)
io.imsave("C:\\Users\\zelmouaffek\\Desktop\\\\Data_Lipos\\\dataset_tif\\train-labels_7.tif",stack_labels)