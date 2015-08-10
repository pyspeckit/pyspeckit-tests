from __future__ import print_function
import numpy as np
from pyspeckit import SpectralCube
from pyspeckit.spectrum.units import SpectroscopicAxis
from pyspeckit.spectrum.models.inherited_gaussfitter import gaussian_fitter
from astropy import units as u
import matplotlib.pyplot as plt
import pytest
from astropy import log

xarr = SpectroscopicAxis(np.linspace(-100, 100, 50), unit=u.dimensionless_unscaled)
gf = gaussian_fitter()
params = [1.0, 2.0, 5.0]
parameter_error_amplitude = [50., 5., 5.]
assertion_list = []
passes = {'passes': [0,0,0], 'avg_difference': [0,0,0]}
fails = {'fails': [0,0,0], 'avg_difference': [0, 0, 0]}


@pytest.mark.parametrize(("rawdata", "noise"), [
                         (gf.n_modelfunc(pars=params)(xarr.value), 
                          np.random.randn(xarr.value.size)/100.)])
def test_fiteach(rawdata, noise):
    for i in range(1):
        passed = True
        parameter_noise = [params[0] + abs(np.random.randn()) * parameter_error_amplitude[0], 
                           params[1] + abs(np.random.randn()) * parameter_error_amplitude[1],
                           params[2] + abs(np.random.randn()) * parameter_error_amplitude[2]]
        guesses = np.array(params)+parameter_noise
        errspec = np.ones(xarr.size)
        data = rawdata + noise
        cube = [[[x for x in data] for y in range(2)] for z in range(2)]
        cube = np.array(cube)
        cube = np.rollaxis(cube, 2, 0)
        sp = SpectralCube.Cube(xarr=xarr, cube=cube, unit='Hz')
        sp.fiteach(guesses=guesses, errspec=errspec, signal_cut=0,
                   fitkwargs={'guesses':guesses}, prevalidate_guesses=True)
        # sp.plotter(axis=plt.gca())
        # plt.show()
        result_cube = sp.parcube
        log.info('sp.parcube: {0}'.format(sp.parcube))
        for i in range(2):
            for j in range(2):
                assertion = ((np.array(result_cube[:,i,j])-np.array(params))/parameter_noise)**2
                for k,result in enumerate(assertion):
                    if result >= 2: 
                        passed = False
                        continue
                if passed:
                    for k in range(3):
                        passes['passes'][k]+=1
                        passes['avg_difference'][k] += abs(result_cube[:,i,j][k] - params[k]).tolist()
                else:
                    for k in range(3):
                        fails['fails'][k]+=1
                        fails['avg_difference'][k] += abs(result_cube[:,i,j][k] - params[k]).tolist()
                assertion_list.append(assertion)

    log.info('assertion_list: {0}'.format(np.array(assertion_list)))
    log.info('passes: {0}'.format(passes))
    log.info('fails: {0}'.format(fails))
