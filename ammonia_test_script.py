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

parameter_error_amplitude = [5., 5., 5., 5., 5., 5.]
params = [2.3,2,0.,0.84,0.2,0.43]

sp = Spectrum('G031.947+00.076_nh3_11_Tastar.fits')
xarr = SpectroscopicAxis(np.linspace(-250, 385, 8192), refX=23694500000.0*u.Hz)
# adding very very tiny noise
parameter_noise = [params[0] + abs(np.random.randn()/1000.) * parameter_error_amplitude[0], 
                   params[1] + abs(np.random.randn()/1000.) * parameter_error_amplitude[1],
                   params[2] + abs(np.random.randn()/1000.) * parameter_error_amplitude[2],
                   params[3] + abs(np.random.randn()/1000.) * parameter_error_amplitude[3],
                   params[4] + abs(np.random.randn()/1000.) * parameter_error_amplitude[4],
                   params[5] + abs(np.random.randn()/1000.) * parameter_error_amplitude[5]]
guesses = np.array(params)+parameter_noise
# producing the fake data using the sample file
# the above defined xarr produces an array of zeroes (and a nan around the middle)
print "Using parameters:", params
rawdata = ammonia.ammonia_model().n_modelfunc(pars=params)(sp.xarr)
noise = np.ones(xarr.size)/100.
sp = Spectrum(xarr=xarr, data=rawdata)#+noise)
# the next line raises an exception in plotters.py:370
# where the ymin.value is accessed but ymin is a float
#TODO : needs checking.
# sp.plotter()
sp.specfit(fittype='ammonia', guesses=guesses, fixed=[False, False, False, False, True, True])
assertion = ((np.array(sp.specfit.fitter.mpp)-np.array(params)))**2
print '(mpp - params / param_noise )^2 = ', assertion
# plt.show()
