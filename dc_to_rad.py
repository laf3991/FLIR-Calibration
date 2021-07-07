# -*- coding: utf-8 -*-
"""
Created on Thu Jun 24 09:57:54 2021

@author: Lucy
"""

import numpy as np 
import glob
import cv2 
import os 
import sys
import matplotlib.pyplot as plt

#Uses calibration coefficients to convert FLIR DC images to radiance

# read in cal coeff
if os.path.exists('coeff.csv')  == False:
    print("No file with calibration coefficients found")
    sys.exit()    
    
data = np.genfromtxt('coeff.csv',delimiter=',')#images need to be same size as cal images 
m = data[:,0]
b = data[:,1]

#calculate radiance images 



val = input("Enter path to collected DC images: ")

isDir = os.path.isdir(val) 
while isDir == False:
    val = input("Enter VALID path to calibration images dir: ")
    
    check = os.path.isdir(val) 
    if check == False:
        continue 
    else:
        isDir = True 
  
if os.path.exists('dead_pixel.tif')  == False:
    print("No dead pixel map found")
    sys.exit() 
    
dead_pixels = cv2.imread('dead_pixel.tif',-1)
#calculate dc to rad 
filenames =  glob.glob(val+"\*.tif")
output = val+"\Radiance"
if not os.path.exists(output):
    os.makedirs(output)

idx = np.where(dead_pixels == np.max(dead_pixels))

for i in range(len(filenames)):
    
    image = cv2.imread(filenames[i],-1) 
    dims = image.shape

    rad_image = (image - np.array(b).reshape((dims[0],dims[1])))/np.array(m).reshape(((dims[0],dims[1])))
    
    
    #carls old code    
    dead_im = (dead_pixels/np.max(dead_pixels)) * rad_image
    inter = (np.roll(dead_im,  1, axis=1) + \
                    np.roll(dead_im, -1, axis=1) + \
                    np.roll(dead_im,  1, axis=0) + \
                    np.roll(dead_im, -1, axis=0)) / 4
    
    index = np.where(dead_pixels == 0.0)
    if len(index[0]) > 0:
    
        dead_im[index] = inter[index]
    
    rad_image[idx] = dead_im[idx]

    
    plt.figure()
    plt.imshow(rad_image)
    plt.colorbar()
    im_name = os.path.basename(filenames[i])
    filename = os.path.join(output,im_name)
    cv2.imwrite(filename,rad_image.astype(np.float32)) 


