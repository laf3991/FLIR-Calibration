# -*- coding: utf-8 -*-
"""
Created on Mon Jun 21 11:39:27 2021

@author: Lucy
"""
import numpy as np 
import cv2
import glob
from scipy.stats import norm
import csv
import os 

#Flir Calibration 

def bb(wave,temp):
    #returns radiance
    h = 6.626 * 10**(-34)
    c = 2.998 * 10**8
    k = 1.381 * 10**(-23)
    wave = wave * 1e-6 #um to m 
    emission = 2*h*c**(2) / (wave**(5) * (np.exp((h*c) / (wave * temp * k))-1)) * 10**(-6)
    
    return emission #W/m^2 sr um  

def create_RSR(center, FWHM):

    #wave = np.arange(center-2,center+2,0.01)
    wave = np.arange(7.5,10.5,0.01)
    rsr = norm.pdf(wave,center,FWHM/2.3548)
    rsr = rsr/max(rsr)
    #plt.plot(wave,rsr)

    return rsr

val = input("Enter Temperature min [C]: ")
val1 = input("Enter Temperature max [C]: ")
val2 = input("Enter Temperature step [C]: ")
temps = np.arange(int(val),int(val1) +int(val2),int(val2))


mean_images = []
tot_rad = []
std = []
val = input("Enter path to calibration images dir: ")

isDir = os.path.isdir(val) 
while isDir == False:
    val = input("Enter VALID path to calibration images dir: ")
    
    check = os.path.isdir(val) 
    if check == False:
        continue 
    else:
        isDir = True 

# print(val)


#probs need to do error checking 
for t in range(len(temps)):
    folders = glob.glob(val+"\*")       
    filenames =  glob.glob(folders[t]+"\*.tif")
    all_images = []
    for i in filenames:
        im = cv2.imread(i,-1) 
        # means.append(np.mean(im))
        # tot_signal.append(np.mean(means))
        all_images.append(im)
        
    mean_image = np.mean(np.array(all_images),axis = 0)
    STD = np.std(np.array(all_images),axis = 0)
    # print(mean_image.shape)
    std.append(STD)
    flat = mean_image.flatten()
    mean_images.append(flat)
    # print(flat.shape)
    
    wave = np.arange(7.5,10.5,.01)
    radiance = bb(wave, temps[t] + 273.15)
    
    #no response of the camera 
    rsr = create_RSR(9,1)
    
    eff_rad = np.trapz(list(rsr * radiance),x=list(wave),axis=0)/np.trapz(list(rsr),x=list(wave),axis=0)
    
    tot_rad.append(eff_rad)
    
    print(eff_rad)
    
# y = mx + b
#should have 4 flattened mean images 
m = []
b = []
# path = r"C:\Users\lucyf\Desktop\cal2123\Test\hand.tif"
# real_image = cv2.imread(path,-1)
# im = real_image.flatten()
# rad_image = []
for i in range(len(mean_images[0])):
    
    pix_array = np.array((mean_images[0][i],mean_images[1][i],mean_images[2][i],mean_images[3][i]))
    
    fit = np.polyfit(tot_rad,pix_array,1)

    m.append(fit[0])
    b.append(fit[1])
    

with open('coeff.csv', 'w', newline='') as csvfile:
    file = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for i in range(len(m)):


        file.writerow((m[i],b[i]))
    
