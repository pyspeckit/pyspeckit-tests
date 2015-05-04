#####################################################################
# Simple test file to test the __repr__ method in SpectroscopicAxis #
#####################################################################

from pyspeckit import Spectrum
from pyspeckit.spectrum.units import SpectroscopicAxis
import astropy.units as u
import numpy as np
import pytest

class TestRepr():

    def test_repr_from_test_fits(self):    	
    	sp = Spectrum('test.fits')
    	# This is too long but it raises an assertion error if I put newlines in it :/
        assert repr(sp.xarr) == """
	SpectroscopicAxis([array(-4953.029632560421),...,array(134895.565032969)], unit=Unit("m / s"), refX=110201370000.0, refX_unit='Hz', frame=None, redshift=None, xtype=None, velocity convention='radio')
        """.strip()

    def test_repr_withunit(self):
    	xarr = SpectroscopicAxis(np.linspace(-100,100,1024)*u.km/u.s)
    	# This is too long but it raises an assertion error if I put newlines in it :/
        assert repr(xarr) == """
	SpectroscopicAxis([array(-100.0),...,array(100.0)], unit=Unit("km / s"), refX=None, refX_unit='Hz', frame=None, redshift=None, xtype=None, velocity convention=None)
        """.strip()