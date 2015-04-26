########################################################################
# This test checks if the moments() method for every model             #
# in Registry.multifitters produces the correct number of paramerters. #
########################################################################

from pyspeckit.spectrum.units import SpectroscopicAxis
from pyspeckit import Spectrum
import numpy as np
import pytest
from astropy import units as u

xvals = np.linspace(-100,100,200) * u.km/u.s
# Some models will fail without a center frequency and a velocity convention
xarr = SpectroscopicAxis(xvals, velocity_convention='radio', center_frequency=100*u.GHz)
rawdata = np.random.randn(xarr.size)

# creating a sample Spectrum from a .fits file
sp = Spectrum('test.fits')
for model_name in sp.specfit.Registry.multifitters.iterkeys():
    try:
        print 'testing:', model_name
        model = sp.specfit.Registry.multifitters[model_name]
        moments = getattr(model, 'moments')
        # creating the random data which are not relevant
        params = model.moments(xarr, rawdata)
        print 'params from moments:',params
        # if this call does not raise an Exception then moments() produced
        # the correct number of parameters 
        model.n_modelfunc(pars=params)(xarr)
    except Exception as e:
        pytest.fail(e)
