# FLIR-Calibration
## FLIR ResearchIR
10 - 50 [C] in steps of 5 [C] on blackbody. 
Using the FLIR software record for 3 min at each temperature. 
Save .ats files in new folder.
Export .ats as multiple images 32 float.tif for each temperature.
### Example file structure
```
-calibration/
  -10/
    -file01.tif
    -file02.tif
  -15/
    -file01.tif
    -file02.tif
  -20/
    -file01.tif
    -file02.tif
```
cal_processing looks specifically for folders named after the temperatures for the images.tif.

## cal_processing.py
This script will generate a csv of the calibration coefficients for each pixel using the calibration images. 
It will ask for the lowest and higest temperatures and also the step. 
It will also aso for a path to the calibration folder, so in this case path to calibration in above example. 
These should match the folder names. 
Once done the coeff.csv will be saved in the same folder. 

## dc_to_rad.py
This will use the coeff.csv to convert dc images to radiance.
This requires a path to the folder with the dc images.
It will save the radiance images in a new folder with the dc images. 
## Note 
May be some bugs in saving the radiance files if the same images are ran over and over...
