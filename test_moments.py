from pyspeckit.spectrum.units import SpectroscopicAxis
from pyspeckit import Spectrum
import numpy as np
import pytest

xarr = np.linspace(-100,100,200)

sp = Spectrum('test.fits')
for model_name in sp.specfit.Registry.multifitters.iterkeys():
    try:
        print 'testing:', model_name
        model = sp.specfit.Registry.multifitters[model_name]
        moments = getattr(model, 'moments')
        rawdata = np.random.randn(xarr.size)
        params = model.moments(xarr, rawdata)
        print 'params from moments:',params
        xarr = SpectroscopicAxis(xarr)
        model.n_modelfunc(pars=params)(xarr)
    except Exception as e:
        pytest.fail(e)
