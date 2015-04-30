#####################################################################
# This script tests the ammonia fitter                              #
# with fake data produced by ammonia_model.n_modelfunc              #
# using the xarr from G031.947+00.076_nh3_11_Tastar.fits [for now]  #
#####################################################################

from pyspeckit.spectrum.models import ammonia
from pyspeckit import Spectrum
from pyspeckit.spectrum.units import SpectroscopicAxis
from astropy import units as u
import numpy as np
import matplotlib.pyplot as plt

passes = []
fails = []
passdiff = []
faildiff = []
results = {'pass': passes, 'pass difference': passdiff,
           'fail': fails, 'fail difference': faildiff}

def generate_guesses(starting_params, parameter_error_amplitude):
    guesses = [starting_params[0] + (np.random.randn() * parameter_error_amplitude[0]), 
               starting_params[1] + (np.random.randn() * parameter_error_amplitude[1]),
               starting_params[2] + (np.random.randn() * parameter_error_amplitude[2]),
               starting_params[3] + (np.random.randn() * parameter_error_amplitude[3]),
               starting_params[4] + (np.random.randn() * parameter_error_amplitude[4]),
               (np.random.randn() * parameter_error_amplitude[5])]
    return guesses    

parameter_error_amplitude = [0.2, 0.5, 1e2, 1., 1., 1.]
starting_params = [3.73,4.73,8.3e14,0.84,96.2,0.43]
for i in range(1):
    xarr = SpectroscopicAxis(np.linspace(-250, 385, 8192)*u.km/u.s, refX=23694500000.0*u.Hz, velocity_convention='radio')
    guesses = generate_guesses(starting_params, parameter_error_amplitude)
    while guesses[0] < 2.73 or guesses[1] < 2.73 or guesses[5] > 1 or guesses[5] < 0:
        guesses = generate_guesses(starting_params, parameter_error_amplitude)

    # producing the fake data using the sample file
    # the above defined xarr produces an array of zeroes (and a nan around the middle)
    # try:
    rawdata = ammonia.ammonia_model().n_modelfunc(pars=starting_params)(xarr)
    # noise = np.ones(xarr.size)/100.
    # rawdata_guesses = ammonia.ammonia_model().n_modelfunc(pars=guesses)(sp.xarr)
    sp = Spectrum(xarr=xarr, data=rawdata)
    # plt.ion()
    # sp.plotter(axis=plt.gca())
    # plt.show()
    try:
        sp.specfit(fittype='ammonia', guesses=guesses)
    except:
        print "skipping ",guesses
        continue
    assertion = ((np.array(sp.specfit.fitter.mpp)-np.array(starting_params)))**2
    difference = abs(np.array(starting_params) - np.array(guesses))
    lessthan2 = True
    print '(mpp - params / param_noise )^2 = ', assertion
    for par in assertion:
        if par > 2:
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

