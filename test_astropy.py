import pyspeckit

if not 'interactive' in globals():
    interactive=False
if not 'savedir' in globals():
    savedir = ''

# load a FITS-compliant spectrum
spec = pyspeckit.Spectrum('10074-190_HCOp.fits')
# The units are originally frequency (check this by printing spec.xarr.units).
# I want to know the velocity.  Convert!
# Note that this only works because the reference frequency is set in the header
# this is no longer necessary!  #spec.xarr.frequency_to_velocity()
# Default conversion is to m/s, but we traditionally work in km/s
spec.xarr.convert_to_unit('km/s')
# plot it up!
spec.plotter()

# compute statistics
stats = spec.stats()

# set the errors
spec.error[:] = stats['std']

# Subtract a baseline (the data is only 'mostly' reduced)
spec.baseline()
# Fit a gaussian.  We know it will be an emission line, so we force a positive guess
# nsigcut_moments tells the moment analysis tool to only use high-significance
# data points to estimate the width of the line (it's tricky)
spec.specfit(negamp=False, nsigcut_moments=2)
# Note that the errors on the fits are larger than the fitted parameters.
# That's because this spectrum did not have an error assigned to it.  
# Let's use the residuals:
# spec.specfit.plotresiduals()
# Now, refit with error determined from the residuals:
# (we pass in guesses to save time / make sure nothing changes)
spec.specfit(guesses=spec.specfit.modelpars)

spec.crop(-45,-5)

import astropy.models as models
gaussian = models.builtin_models.Gaussian1DModel(1,1,1)

import pyspeckit.spectrum.models.model
g = pyspeckit.spectrum.models.model.AstropyModel(gaussian)

spec.specfit.register_fitter('gaussian2',g,3,multisingle='multi')
spec.specfit(fittype='gaussian2',guesses=[0.5,-27,1])

# spec += 1.3
# 
# vheight = models.builtin_models.ShiftModel(0.5)
# vheightGaussian = models.SCompositeModel([vheight, gaussian])
# vg = pyspeckit.spectrum.models.model.AstropyModel(vheightGaussian)
# 
# spec.specfit.register_fitter('vgaussian',vg,4)
# spec.specfit(fittype='vgaussian', guesses=[0.5,-26,1])
