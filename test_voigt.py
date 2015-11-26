try:
    import scipy
    scipyOK = True
except ImportError:
    scipyOK = False

if scipyOK:
    import numpy as np
    import pyspeckit.spectrum.models.inherited_voigtfitter as IV
    from pyspeckit.spectrum.units import SpectroscopicAxis

    xarr = SpectroscopicAxis(np.linspace(-100,100,1000))
    dx = np.diff(xarr).mean()

    V1 = IV.voigt(xarr,1,0,1,1,normalized=False)
    V2 = IV.voigt(xarr,1,0,1,1,normalized=True)

    assert np.sqrt(2*np.pi) - 0.05 < V1.sum()*dx.value < np.sqrt(2*np.pi) + 0.05 
    assert 0.99 < V2.sum()*dx.value < 1.01
else:
    print("Skipped Voigt test because scipy could not be imported")
