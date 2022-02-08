import numpy as np 
from astropy.io import fits 

import os
import sys

filenames = []

for file in sorted(os.listdir (".")):
	if file.endswith(".fits"):
		print (file)
		filenames.append(file)
print (len(filenames))


print (filenames[0])
stokes = fits.open(filenames[0])[0].data
print (stokes.shape)
SLITSIZE = stokes.shape[2]
print ('Slitlength = ', SLITSIZE)
stokes = stokes.reshape(1,4,SLITSIZE,112)

filenames=filenames[1:]
for name in filenames:
	stokes_temp = fits.open(name)[0].data
	stokes_temp = stokes_temp.reshape(1,4,SLITSIZE,112)
	stokes = np.concatenate((stokes,stokes_temp),axis=0)

stokes = stokes.transpose(2,0,1,3)
print (stokes.shape)

output = sys.argv[1]
hdu = fits.PrimaryHDU(stokes)
hdu.header = fits.open(name)[0].header
hdu.writeto(output,overwrite=True)



	
