from __future__ import print_function
import numpy as np
from astropy import units as u
from pyspeckit import Spectrum
from pyspeckit.spectrum.units import SpectroscopicAxis

########################################################################
# This test checks if the moments() method for every model             #
# in Registry.multifitters produces the correct number of paramerters. #
########################################################################


def test_moments():
    xvals = np.linspace(-100,100,200) * u.km/u.s
    # Some models will fail without a center frequency and a velocity convention
    xarr = SpectroscopicAxis(xvals, velocity_convention='radio', center_frequency=100*u.GHz)
    # creating the random data
    rawdata = np.random.randn(xarr.size)

    # creating a sample Spectrum from a .fits file
    sp = Spectrum('test.fits')
    for model_name in sp.specfit.Registry.multifitters.keys():
        print('testing:', model_name)
        model = sp.specfit.Registry.multifitters[model_name]
        params = model.moments(xarr, rawdata, vheight=False)
        print('params from moments:',params)
        assert len(params) == model.npars
        # if this call does not raise an Exception then moments() produced
        # the correct number of parameters
        model.n_modelfunc(pars=params)(xarr)

if __name__ == "__main__":
    test_moments()
