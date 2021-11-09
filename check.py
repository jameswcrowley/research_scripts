# a script to read in and quickly check a fits file against data

# want to check chi-sq and (?)

import numpy as np 
from astropy.io import fits 
import sys 

cube = fits.open(sys.argv[1])[0].data
data = fits.open(sys.argv[2])[0].data
output_cube_name = sys.argv[3]

# format of both should be (4, 60, x, y)
# checking if datacube is normalized yet:

weights = np.array([1,3,3,3])

if np.mean(data[0]) > 1.2:
    #normalize data
    for i in range(4):
        data[i] = np.truedivide(data[i], np.mean(data[i, :10])

chi2 = np.sum((data - cube)**2, axis=(1))/(10**-4 * 60)
    
chi2 = chi2/(weights[:, None, None]**2)
chi2_mean = np.mean(chi2[:, :])

print("chi-sq of inversion: " + str(sys.argv[1]) + " with observation: " + str(sys.argv[2]) + " is:"))
print(chi2_mean)
