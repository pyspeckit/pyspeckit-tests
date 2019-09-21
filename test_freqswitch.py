from __future__ import print_function
from astropy import units as u
from six import iteritems
import astropy
try:
    from astropy.io import fits as pyfits
except ImportError:
    import pyfits
import numpy as np

# generate an X-array in MHz units
x = np.linspace(100,110,101)
# generate a blank array
y = np.zeros(101)
# set a few known frequencies to have nonzero values
y[x==101.0] = 1.0
y[x==102.0] = 2.0
y[x==105.0] = -1.0

header = pyfits.Header()
for k,v in iteritems({'CUNIT1':'MHz','CTYPE1':'FREQ','CDELT1':0.1,'CRVAL1':100.0,'CRPIX1':1.0}):
    header.update(k,v)

HDU = pyfits.PrimaryHDU(data=y,header=header)

if astropy.version.major >= 2 or (astropy.version.major==1 and astropy.version.minor>=3):
    HDU.writeto('test_freqswitch.fits',overwrite=True)
else:
    HDU.writeto('test_freqswitch.fits',clobber=True)

import pyspeckit
import pylab

sp = pyspeckit.Spectrum('test_freqswitch.fits')
sp.plotter()
pylab.plot(x,y,'k--',drawstyle='steps-mid')

print(("First test - do the FITS version and the input match up?"))
# import pdb; pdb.set_trace()

assert(sp.xarr.unit is not u.dimensionless_unscaled)
sp.xarr = sp.xarr.as_unit('km/s', center_frequency=105.0, center_frequency_unit='MHz', velocity_convention='optical')

sp.plotter(reset_xlimits=True)

print(("Test two - what happens when we set the reference frequency to be 105?"))
print("The positive lines should be on the right side.  So they are.  OK.")
# import pdb; pdb.set_trace()
