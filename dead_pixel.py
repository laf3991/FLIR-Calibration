# -*- coding: utf-8 -*-
"""
Spyder Editor

author: Lucy Falcon
"""
import os 
import numpy as np 
import glob
import cv2

val = input("Enter path to collected FLIR dark images: ")

isDir = os.path.isdir(val) 
while isDir == False:
    val2 = input("Enter VALID path to calibration images dir: ")
    
    check = os.path.isdir(val2) 
    if check == False:
        continue 
    else:
        isDir = True 

filenames =  glob.glob(val+"\*.tif")


#SOMEONES CODE FOR DEAD PIXEL MAPPING 
popper_thresh = 0.01
sd_count = 4
image_list = os.listdir(val)

popper_val = popper_thresh * len(filenames)

#reading an image to know what size to make the mask
dim = cv2.imread(filenames[0],-1).astype("float32")

mask_sum = np.zeros((np.shape(dim)[0], np.shape(dim)[1]), np.float)
for image in filenames:
    img = cv2.imread(image,-1).astype("float32")
    img_gray = img#cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    m, s = cv2.meanStdDev(img_gray)
    #thresholding both below and above the mean value by the set number of stdevs
    ret, threshold = cv2.threshold(img_gray, m+sd_count*s, 255, cv2.THRESH_BINARY)
    ret, inv_threshold = cv2.threshold(img_gray, m-sd_count*s, 255, cv2.THRESH_BINARY_INV)
    #adding 1 at the thresholded pixel locations to a sum matrix of masks, so at each pixel
    #location it displays a value of how many times a dead pixel was detected there
    mask_sum += threshold/255
    mask_sum += inv_threshold/255

kernel = np.ones((5,5), np.uint8)

#creating a matrix of just the values that fell below the max
#since the pixels that have the max value are presumed to be actually dead pixels
poppers = cv2.inRange(mask_sum, 1, np.max(mask_sum) - popper_val)
#clipping the matrix to be all 255 so it's a real mask
poppers[np.all(poppers > 0)] = 255
#these dilation matrices are just useful to easily see where the marked pixels are
dilate = True
if dilate == True:
    poppers = cv2.dilate(poppers, kernel)

#only accepting mask values that have the max number of detected pixels in the mask
ret, dead_pixels = cv2.threshold(mask_sum, np.max(mask_sum) - 1, 255, cv2.THRESH_BINARY)
dead_pixels[np.all(dead_pixels > 0)] = 255
dead_pixels = dead_pixels.astype(np.uint8)
if dilate == True:
    dead_pixels = cv2.dilate(dead_pixels, kernel)
    
    
    
    
