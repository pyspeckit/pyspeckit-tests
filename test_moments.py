########################################################################
# This test checks if the moments() method for every model             #
# in Registry.multifitters produces the correct number of paramerters. #
########################################################################

from pyspeckit.spectrum.units import SpectroscopicAxis
from pyspeckit import Spectrum
import numpy as np
import pytest

xarr = np.linspace(-100,100,200)

# creating a sample Spectrum from a .fits file
sp = Spectrum('test.fits')
for model_name in sp.specfit.Registry.multifitters.iterkeys():
    try:
        print 'testing:', model_name
        model = sp.specfit.Registry.multifitters[model_name]
        moments = getattr(model, 'moments')
        # creating the random data which are not relevant
        rawdata = np.random.randn(xarr.size)
        params = model.moments(xarr, rawdata)
        print 'params from moments:',params
        xarr = SpectroscopicAxis(xarr)
        # if this call does not raise an Exception then moments() produced
        # the correct number of parameters 
        model.n_modelfunc(pars=params)(xarr)
    except Exception as e:
        pytest.fail(e)
