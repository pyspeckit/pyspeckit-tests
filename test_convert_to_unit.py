#####################################################################################
# Regression test for convert_to_unit in pyspeckit.spectrum.units.SpectroscopicAxis #
# Uses doppler_radio, _optical and _relativistic equivalencies                      #
#####################################################################################

from pyspeckit.spectrum.units import SpectroscopicAxis
import astropy.units as u
import random
import numpy as np
import inspect
import pytest

def test_convert_to_unit(run_with_assert=False):
    for from_unit, to_unit, _, __ in u.doppler_optical(1*u.Hz):
        sp = SpectroscopicAxis(np.linspace(-100,100,100),
                               unit=from_unit, refX=23.2*u.Hz,
                               velocity_convention='optical')
        sp.convert_to_unit(to_unit)
        if(run_with_assert):
            assert sp.unit == to_unit
    for from_unit, to_unit, _, __ in u.doppler_radio(1*u.eV):
        sp = SpectroscopicAxis(np.linspace(-100,100,100), 
                               unit=from_unit, refX=23.2*u.Hz,
                               velocity_convention='optical')
        sp.convert_to_unit(to_unit)
        if(run_with_assert):
            assert sp.unit == to_unit
    for from_unit, to_unit, _, __ in u.doppler_relativistic(1*u.Angstrom):
        sp = SpectroscopicAxis(np.linspace(-100,100,100), 
                               unit=from_unit, refX=23.2*u.Hz,
                               velocity_convention='relativistic')
        sp.convert_to_unit(to_unit)
        if(run_with_assert):
            assert sp.unit == to_unit
