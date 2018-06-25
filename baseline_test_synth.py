# regression testing for issue 123

import pyspeckit
import numpy as np
import pylab as pl

length = 50
x = np.linspace(0.0,0.15, length)
# create a baseline based on pixel coordinates (which is how it gets fit unless
# a unit is specified)
# alternative: baseline = np.polyval([2.0, 1.0], x) will lead to assertion
# errors below
baseline = np.polyval([0.005,1], np.arange(length))
y = np.exp(-(x-0.075)**2 / (2*0.005**2)) + baseline
e = np.repeat(0.1, length)
sp = pyspeckit.Spectrum(xarr=x, data=y, error=e, xarrkwargs={'unit':'um'}, header={})

sp.plotter(figure=pl.figure(1), clear=True)
sp.specfit(fittype='gaussian', guesses='moments')
# make sure the fit is way too wide
assert sp.specfit.parinfo.WIDTH0.value > 0.05
# and too high by a little
assert sp.specfit.parinfo.AMPLITUDE0.value > 1.05

sp.baseline(subtract=False, save=False, highlight_fitregion=True,
            exclude=[0.05,0.10], order=1)

np.testing.assert_almost_equal(sp.baseline.baselinepars[0], 0.005)
np.testing.assert_almost_equal(sp.baseline.baselinepars[1], 1)

sp.specfit(fittype='gaussian', guesses='moments')

np.testing.assert_almost_equal(sp.specfit.parinfo.WIDTH0.value, 0.005, decimal=4)
np.testing.assert_almost_equal(sp.specfit.parinfo.AMPLITUDE0.value, 1.0, decimal=3)
np.testing.assert_almost_equal(sp.specfit.parinfo.SHIFT0.value, 0.075, decimal=3)

sp.baseline(subtract=False, save=False, highlight_fitregion=True, exclude=[0.06,0.09], order=2)

np.testing.assert_almost_equal(sp.baseline.baselinepars[0], 0.000, decimal=3)
np.testing.assert_almost_equal(sp.baseline.baselinepars[1], 0.005, decimal=3)
np.testing.assert_almost_equal(sp.baseline.baselinepars[2], 1, decimal=3)


# Making a copy of the spectrum file to be iterated through with MC loop later
sp2 = sp.copy()
sp2.xarr.xtype = 'wavelength'

for i in range(1):
    sp2.data = sp.data + np.random.randn(sp.data.size)*sp.error
    sp2.plotter(xmin=0, xmax=0.15, ymin=0.9, ymax=2.1, errstyle='bars')
    sp2.plotter.axis.set_ylabel(r'Flux F$_{\lambda}$')
    sp2.plotter.axis.set_xlabel(r'Wavelength ($\mu$m) - $W_0$')
    sp2.baseline(subtract=False, save=False, highlight_fitregion=True, exclude=[0.06,0.09], order=1)
    coeffs = sp2.baseline.baselinepars
    print(coeffs[0])
