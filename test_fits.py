from __future__ import print_function
import pyspeckit
import numpy as np

if not 'interactive' in globals():
    interactive=False
if not 'savedir' in globals():
    savedir = ''

try:
    input = raw_input
except NameError:
    raw_input = input

sp = pyspeckit.Spectrum('sample_13CO.fits')
print("Does it have an axis? ",sp.plotter.axis)
sp.plotter()
print("How about now? ",sp.plotter.axis)
assert sp.plotter.xlabel == 'Velocity (m / s)'
assert sp.plotter.ylabel == "Brightness Temperature $T$ (K)"


# set the baseline to zero to prevent variable-height fitting
# (if you don't do this, the best fit to the spectrum is dominated by the
# background level)
sp.baseline.order = 0
sp.specfit.peakbgfit(vheight=False)
if savedir != "":
    sp.plotter.figure.savefig(savedir+'fits_gaussfit.png')
print("Guesses: ", sp.specfit.guesses)
print("Best fit: ", sp.specfit.modelpars)
print("specfit:", sp.specfit)
fitted_fwhm = sp.specfit.parinfo.WIDTH0*np.sqrt(np.log(2)*8)
print("Fitted FWHM: ", fitted_fwhm)

measured_fwhm2 = sp.specfit.measure_approximate_fwhm(interpolate_factor=10)
print("Measured FWHM (x10 accuracy): ", measured_fwhm2)
assert np.abs(measured_fwhm2.value-fitted_fwhm) < 200 # interpolating makes smaller fwhm in this case

measured_fwhm = sp.specfit.measure_approximate_fwhm()
print("Measured FWHM: ", measured_fwhm)
assert np.abs(measured_fwhm.value-fitted_fwhm) < 50 # i.e., close enough...

# # Fit a baseline, excluding the velocities with data, and don't subtract it
sp.baseline(exclude=[12000,98000],subtract=False)
# print("Baseline: ",sp.baseline.baselinepars)
# print("Excludepix: ",sp.baseline.excludepix)

sp.specfit(interactive=True)
if interactive:
    raw_input('Press enter to printguesses and best fit and end code')
if savedir != "":
    sp.plotter.figure.savefig(savedir+'fits_interactive_fit.png')
print("Guesses: ", sp.specfit.guesses)
print("Best fit: ", sp.specfit.modelpars)

# don't try this for a zero-baseline spectrum print("EQW: ",sp.specfit.EQW())

print("Attempting to write to test.fits: ")
sp.write('test.fits')

sptest = pyspeckit.Spectrum('test.fits')
sptest.plotter()
sptest.plotter(figure=1,clear=False,color='b',offset=0.1)
if interactive:
    raw_input('Test fits done.')
sp.xarr.convert_to_unit('GHz',center_frequency=110201.3541, center_frequency_unit='MHz', velocity_convention='radio')
sp.write('test_GHz.fits')

sptestGHz = pyspeckit.Spectrum('test_GHz.fits')
sptestGHz.plotter()

#This test fails locally due to unknown errors in hdf5:
#"TypeError: No conversion path for dtype: dtype('<U3')"
# print("Attempting to write to test.hdf5: ")
# sp.write('test.hdf5')

# try to add something to header
pyspeckit.history.write_history(sp.header, "history test")

#from matplotlib import pyplot

