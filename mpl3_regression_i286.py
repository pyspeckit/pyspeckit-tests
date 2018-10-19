"""
Regression test for Issue 286: a method in matplotlib went from
public->private->absent, so I had to build in a workaround for that.

The test just makes sure that the disconnect/reconnect stuff operates
properly; it needs to check whether the function used as a callback
is one created by pyspeckit (i.e., one called 'event_manager')
"""
import numpy as np
import pyspeckit

def test_regression_i286():
    sp = pyspeckit.Spectrum(xarr=np.linspace(-5,5), data=np.random.randn(50))
    sp.plotter()
    sp.specfit.clear_all_connections()
