#####################################################################
# This script tests the ammonia fitter                              #
# with fake data produced by ammonia_model.n_modelfunc              #
# using the xarr from G031.947+00.076_nh3_11_Tastar.fits [for now]  #
#####################################################################

from pyspeckit.spectrum.models import ammonia
from pyspeckit.spectrum.models.ammonia_constants import freq_dict
from pyspeckit import Spectrum
from pyspeckit.spectrum.units import SpectroscopicAxis
from astropy import units as u
import numpy as np
import matplotlib.pyplot as plt
import pytest

strict_assertion = True
passes = []
fails = []
passdiff = []
faildiff = []
results = {'pass': passes, 'pass difference': passdiff,
           'fail': fails, 'fail difference': faildiff}

parameter_error_amplitude = [0.2, 0.5, 1e2, .4, 1., .2]
starting_params = [3.73,4.73,8.3e14,0.84,96.2,0.43]
xarr11 = SpectroscopicAxis(np.linspace(-250, 385, 8192)*u.km/u.s, refX=freq_dict['oneone'], velocity_convention='radio')

def generate_guesses(starting_params, parameter_error_amplitude):
    guesses = [starting_params[0] + (np.random.randn() * parameter_error_amplitude[0]), 
               starting_params[1] + (np.random.randn() * parameter_error_amplitude[1]),
               starting_params[2] + (np.random.randn() * parameter_error_amplitude[2]),
               starting_params[3] + (np.random.randn() * parameter_error_amplitude[3]),
               starting_params[4] + (np.random.randn() * parameter_error_amplitude[4]),
               (np.random.randn() * parameter_error_amplitude[5])]
    return guesses    

@pytest.mark.parametrize(('rawdata'),
                         [ammonia.ammonia_model().n_modelfunc(pars=starting_params)(xarr11)])
def test_ammonia_model(rawdata):
    for i in range(1):
        # xarr22 = SpectroscopicAxis(np.linspace(-250, 385, 8192)*u.km/u.s, refX=freq_dict['twotwo'], velocity_convention='radio')
        # xarr33 = SpectroscopicAxis(np.linspace(-250, 385, 8192)*u.km/u.s, refX=freq_dict['threethree'], velocity_convention='radio')

        guesses = generate_guesses(starting_params, parameter_error_amplitude)
        while guesses[0] < 2.73 or guesses[1] < 2.73 or guesses[5] > 1 or guesses[5] < 0:
            guesses = generate_guesses(starting_params, parameter_error_amplitude)

        # producing the fake data using the sample file
        # the above defined xarr produces an array of zeroes (and a nan around the middle)
        # try:
        # rawdata = ammonia.ammonia_model().n_modelfunc(pars=starting_params)(xarr11)
        sp = Spectrum(xarr=xarr11, data=rawdata)
        try:
            sp.specfit(fittype='ammonia', guesses=guesses)
        except:
            print "skipping ",guesses
            continue
        assertion = ((np.array(sp.specfit.fitter.mpp)-np.array(starting_params))/np.array(starting_params))**2
        difference = abs(np.array(starting_params) - np.array(guesses))
        lessthan2 = True
        print '(mpp - params / param_noise )^2 = ', assertion
        for par in assertion:
            if par > 2:
                if strict_assertion:
                    raise AssertionError
                lessthan2 = False
        
        if lessthan2:
            results['pass'].append(assertion)
            results['pass difference'].append(difference)
        else:
            results['fail'].append(assertion)
            results['fail difference'].append(difference)

    for key in results:
        print key
        print results[key]

