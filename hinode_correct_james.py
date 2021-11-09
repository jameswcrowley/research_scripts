# arguments are: data in, data out
# use like: hinode_correct_james.py

import numpy as np 
from astropy.io import fits 
import sys 


# no longer checks for SBP shift, pulls it from the header
# otherwise, this part is the same.
cube_name = sys.argv[1]
output_cube_name = sys.argv[2]

stokes = fits.open(cube_name)[0]
SPBSHIFT = stokes.header[103]
stokes = stokes.data
stokes = stokes.astype('double')


stokesI = np.copy(stokes[:,:,0,:])
if (SPBSHFT > 0):
	stokesI *= 2
negative = np.where(stokesI < 0.0)
stokesI[negative] += 65536.
stokes[:,:,0,:] = stokesI

if (SPBSHFT > 1):
	stokes[:,:,3,:] *= 2

if (SPBSHFT > 2):
	stokes[:,:,1,:] *= 2
	stokes[:,:,2,:] *= 2

    
stokes_corrected = np.copy(stokes)

for i in range(stokes_corrected.shape[0]):
    for j in range(stokes_corrected.shape[1]):
        for l in range(stokes_corrected.shape[2]):
            if (stokes[i,j, 0, l] > (stokes[i,j,0,10] + 7000.)): # to figure out what is "core"
                stokes_corrected[i,j, 0, l] = stokes_corrected[i,j, 0, l] - 65536 
                
            else:
                stokes_corrected[i,j, 0, l] = stokes[i,j, 0, l]
        stokes_corrected[i,j,0,:] += 65536


xxx = fits.PrimaryHDU(stokes_corrected)
xxx.writeto(output_cube_name,overwrite=True)