# -*- coding: utf-8 -*-
"""
Created on Thu Jun 24 09:57:54 2021

@author: Lucy
"""

import numpy as np 
import glob
import cv2 
import os 

#Uses calibration coefficients to convert FLIR DC images to radiance 

# read in cal coeff       
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

filenames =  glob.glob(val+"\*.tif")


output = val+"\Radiance"
if not os.path.exists(output):
    os.makedirs(output)

for i in range(len(filenames)):
    
    image = cv2.imread(filenames[i],-1) 
    dims = image.shape
    
    rad_image = (image - np.array(b).reshape((dims[0],dims[1])))/np.array(m).reshape(((dims[0],dims[1])))
    im_name = os.path.basename(filenames[i])
    filename = os.path.join(output,"Radiance_"+im_name)
    cv2.imwrite(filename,rad_image) 


