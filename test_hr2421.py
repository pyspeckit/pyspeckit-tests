from __future__ import print_function
import numpy; print(numpy.geterr())
import pyspeckit
import matplotlib
import warnings
from astropy.io import fits
from astropy import units as u

if not 'interactive' in globals():
    interactive=False
if not 'savedir' in globals():
    savedir = ''

try:
    input = raw_input
except NameError:
    raw_input = input


with warnings.catch_warnings():
    # do not allow warnings to raise exceptions here as they will be caught incorrectly
    warnings.simplefilter('ignore')
    try:
        sp = pyspeckit.Spectrum('hr2421.fit')
    except Exception as ex:
        assert ex.message == "'ergs s-1 cm-2 A-1' did not parse as unit: At col 0, ergs is not a valid unit. Did you mean erg?"

f = fits.open('hr2421.fit')
f[0].header['BUNIT'] = 'erg s-1 cm-2 AA-1'
sp = pyspeckit.Spectrum.from_hdu(f[0])


print("Does it have an axis? ",sp.plotter.axis)
sp.plotter()
print("How about now? ",sp.plotter.axis)

sp.plotter(xmin=4700,xmax=5000)
print("Plotter min/max: ",sp.plotter.xmin,sp.plotter.xmax," Fitter min/max: ",sp.specfit.xmin,sp.specfit.xmax," Fitregion= ",sp.baseline.button1plot," bfit target sum: ",sp.baseline.includemask.sum())

if interactive: raw_input("Wait here a moment")
import numpy as np;
print(np.geterr())
sp.baseline(subtract=False, exclude=[4830, 4890], order=2, highlight=True)
assert sp.baseline.basespec[sp.xarr.x_to_pix(4860)] > 0
print("Plotter min/max: ",sp.plotter.xmin,sp.plotter.xmax," Fitter min/max: ",sp.specfit.xmin,sp.specfit.xmax," Fitregion= ",sp.baseline.button1plot," bfit target sum: ",sp.baseline.includemask.sum())
# obsolete 1/16/2012 print("Baseline exclude: ",sp.baseline.excludevelo,sp.baseline.excludepix)
if interactive:
    raw_input("Wait here a moment")

# set the baseline to zero to prevent variable-height fitting
# (if you don't do this, the best fit to the spectrum is dominated by the
# background level)
#sp.baseline.order = 0
print("FITTING GAUSSIAN")
sp.specfit.peakbgfit() #(debug=True,verbose=True)
sp.specfit.peakbgfit() # Do this twice to get a better estimate of the noise  (debug=True,verbose=True)
print("Plotter min/max: ",sp.plotter.xmin,sp.plotter.xmax," Fitter min/max: ",sp.specfit.xmin,sp.specfit.xmax," Fitregion= ",sp.baseline.button1plot," bfit target sum: ",sp.baseline.includemask.sum())
if savedir != "":
    sp.plotter.figure.savefig(savedir+'hr2421_gaussfit.png')
print("Guesses: ", sp.specfit.guesses)
print("Best fit: ", sp.specfit.modelpars)
print("EQW: ",sp.specfit.EQW())
print("Chi2: ",sp.specfit.chi2)
print("Optimal Chi2/n:",sp.specfit.optimal_chi2())
gauss_model = sp.specfit.model+sp.baseline.basespec[sp.specfit.xmin:sp.specfit.xmax]
print("A Gaussian has been fit.  There should be a red line overlaid on the spectrum with green highlighting the baseline fit region and yellow showing the baseline fit")
if interactive: raw_input("Wait here a moment")

try:
    print("FITTING VOIGT")
    sp.specfit.peakbgfit(fittype='voigt')
    print("Guesses: ", sp.specfit.guesses)
    print("Best fit: ", sp.specfit.modelpars)
    print("EQW: ",sp.specfit.EQW())
    print("Chi2: ",sp.specfit.chi2)
    sp.plotter.axis.plot(sp.xarr[sp.specfit.xmin:sp.specfit.xmax],gauss_model,color='b',linewidth=0.5)
    sp.plotter(clear=False,reset=False)
    if savedir != "":
        sp.plotter.figure.savefig(savedir+'hr2421_voigtfit.png')
    voigt_model = sp.specfit.model+sp.baseline.basespec[sp.specfit.xmin:sp.specfit.xmax]
    print("Voigt baseline: {0}".format(sp.baseline.baselinepars))
    print("A voigt model has been fit.  The red line from before should have a blue line overlaid.  They should be only moderately different.")
    if interactive:
        raw_input("Wait here a moment")
except ImportError:
    print("Could not fit voigt profiles because scipy wasn't installed.")

print()

# refit the baseline
sp.baseline(subtract=False, exclude=[4830, 4890], order=2, highlight=True)

# convert from data locations to plotter locations
x1d = 4800
x2d = 4900
x3d = 4860
y3d = sp.slice(4800*u.AA, 4900*u.AA).data.min()
x4d = 4850
y4d = sp.data[np.int(sp.xarr.x_to_pix(4879))]
x5d = 4880
y1d = sp.slice(4800*u.AA, 4900*u.AA).data.mean()
x1,y1 = sp.plotter.axis.transData.transform([x1d,y1d])
x2,y1 = sp.plotter.axis.transData.transform([x2d,y1d])
x3,y3 = sp.plotter.axis.transData.transform([x3d,y3d])
x4,y4 = sp.plotter.axis.transData.transform([x4d,y4d])
x5,y1 = sp.plotter.axis.transData.transform([x5d,y1d])

sp.specfit(interactive=True)
print("INTERACTIVE #1: fittype=",sp.specfit.fittype," npars: ",sp.specfit.fitter.npars)
if interactive:
    raw_input('Press enter to printguesses and best fit and end code')
else:
    event1 = matplotlib.backend_bases.MouseEvent('button_press_event', sp.plotter.axis.figure.canvas,x1,y1,button=1)
    event2 = matplotlib.backend_bases.MouseEvent('button_press_event', sp.plotter.axis.figure.canvas,x2,y1,button=1)
    event3 = matplotlib.backend_bases.MouseEvent('button_press_event', sp.plotter.axis.figure.canvas,x3,y3,button=2)
    event4 = matplotlib.backend_bases.MouseEvent('button_press_event', sp.plotter.axis.figure.canvas,x4,y4,button=2)
    event5 = matplotlib.backend_bases.MouseEvent('button_press_event', sp.plotter.axis.figure.canvas,x5,y1,button=3)
    sp.specfit.event_manager(event1)
    sp.specfit.event_manager(event2)
    if savedir != "":
        sp.plotter.figure.savefig(savedir+'hr2421_interactive_selectregion.png')
    sp.specfit.event_manager(event3)
    sp.specfit.event_manager(event4)
    if savedir != "":
        sp.plotter.figure.savefig(savedir+'hr2421_interactive_guesses.png')
    sp.specfit.event_manager(event5)

if savedir != "":
    sp.plotter.figure.savefig(savedir+'hr2421_interactive_fit.png')
print("Guesses: ", sp.specfit.guesses)
print("Best fit: ", sp.specfit.modelpars)

print("EQW: ",sp.specfit.EQW(fitted=False))
print("EQW (fitted): ",sp.specfit.EQW(fitted=True))

# double check that the baseline is still OK
assert sp.baseline.basespec[sp.xarr.x_to_pix(4860)] > 0

sp.plotter(xmin=4700,xmax=5000)
eventF = matplotlib.backend_bases.KeyEvent('key_press_event', sp.plotter.axis.figure.canvas,key='f',x=257,y=316)
eventV = matplotlib.backend_bases.KeyEvent('key_press_event', sp.plotter.axis.figure.canvas,key='v',x=257,y=316)
sp.specfit.event_manager(eventF)
sp.specfit.event_manager(eventV)
print("INTERACTIVE #2: fittype=",sp.specfit.fittype," npars: ",sp.specfit.fitter.npars)

x1,y1 = sp.plotter.axis.transData.transform([x1d,y1d])
x2,y1 = sp.plotter.axis.transData.transform([x2d,y1d])
x3,y3 = sp.plotter.axis.transData.transform([x3d,y3d])
x4,y4 = sp.plotter.axis.transData.transform([x4d,y4d])
x5,y1 = sp.plotter.axis.transData.transform([x5d,y1d])

# double check that the baseline is still OK
assert sp.baseline.basespec[sp.xarr.x_to_pix(4860)] > 0

event1 = matplotlib.backend_bases.MouseEvent('button_press_event', sp.plotter.axis.figure.canvas,x1,y1,button=1)
event2 = matplotlib.backend_bases.MouseEvent('button_press_event', sp.plotter.axis.figure.canvas,x2,y1,button=1)
event3 = matplotlib.backend_bases.MouseEvent('button_press_event', sp.plotter.axis.figure.canvas,x3,y3,button=2)
event4 = matplotlib.backend_bases.MouseEvent('button_press_event', sp.plotter.axis.figure.canvas,x4,y4,button=2)
event5 = matplotlib.backend_bases.MouseEvent('button_press_event', sp.plotter.axis.figure.canvas,x5,y1,button=2)
event6 = matplotlib.backend_bases.MouseEvent('button_press_event', sp.plotter.axis.figure.canvas,x4,y1,button=3)
sp.specfit.event_manager(event1,debug=True)
sp.specfit.event_manager(event2,debug=True)
sp.specfit.event_manager(event3,debug=True)
sp.specfit.event_manager(event4,debug=True)
sp.specfit.event_manager(event5,debug=True)

# since this is an absorption line, the guess should be negative
# (guesses are only set after the 3rd (nwidths) click)
assert sp.specfit.guesses[0] < 0

if savedir != "":
    sp.plotter.figure.savefig(savedir+'hr2421_interactive_guesses_oneextra.png')
sp.specfit.event_manager(event6,debug=True)

print("Guesses: ", sp.specfit.guesses)
print("Best fit: ", sp.specfit.modelpars)

print("EQW: ",sp.specfit.EQW(fitted=False))
print("EQW (fitted): ",sp.specfit.EQW(fitted=True))


#from matplotlib import pyplot

