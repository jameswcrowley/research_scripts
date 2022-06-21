# arguments are: data in, data out
# use like: hinode_correct_james.py name_in name_out

import numpy as np 
from astropy.io import fits 
import sys 


# no longer checks for SBP shift, pulls it from the header
# otherwise, this part is the same.
cube_name = sys.argv[1]
output_cube_name = sys.argv[2]
#sir = sys.argv[3] # idea: if TRUE, reshape for SIR... 

stokes = fits.open(cube_name)[0]
SPBSHIFT = stokes.header[103]
stokes = stokes.data
stokes = stokes.astype('float')


stokesI = np.copy(stokes[:,:,0,:])
if (SPBSHIFT > 0):
    stokes[:,:,0,:] *= 2.0
    negative = np.where(stokesI < 0.0)
    stokesI[negative] += 65536.
    stokes[:,:,0,:] = stokesI

if (SPBSHIFT > 1):
    stokes[:,:,3,:] *= 2.0

if (SPBSHIFT > 2):
    stokes[:,:,1,:] *= 2.0
    stokes[:,:,2,:] *= 2.0

#stokes_corrected = np.zeros((stokes.shape), dtype = 'float')
#stokes_corrected[:, :, 1:, :] = stokes[:, :, 1:, :]

#for i in range(stokes.shape[0]):
#    for j in range(stokes.shape[1]):
#        for l in range(stokes.shape[3]):
#            if stokes[i,j,0,l] < 0:
#                stokes_corrected[i,j,0,l] = stokes[i,j,0,l] + 65536
#            else: 
#                stokes_corrected[i,j,0,l] = stokes[i,j,0,l]
                
                
stokes = np.swapaxes(np.swapaxes(stokes[:, 1:, :, :], 0, 2), 1, 3)
stokes[:] = np.true_divide(stokes[:], np.mean(stokes[0, :10, :, :]))

xxx = fits.PrimaryHDU(stokes)
xxx.writeto(output_cube_name,overwrite=True)
