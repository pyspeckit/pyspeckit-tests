from __future__ import print_function
import numpy as np
from pyspeckit.spectrum.models.inherited_gaussfitter import gaussian_fitter
from pyspeckit import Spectrum
import matplotlib.pyplot as plt
import pytest

strict_assertion = True
xarr = np.linspace(-100,100,200)
gf = gaussian_fitter()
# params = [1.0, 2.0, 20.]
parameter_error_amplitude = [5., 5., 5.]
passes = {'passes': [0,0,0], 'avg_difference': [0,0,0]}
fails = {'fails': [0,0,0], 'avg_difference': [0, 0, 0]}

@pytest.mark.parametrize(('rawdata', 'noise', 'error', 'params'), 
                                                [(gf.n_modelfunc(pars=params)(xarr), 
                                                  np.random.randn(xarr.size)/100., 
                                                  np.ones(xarr.size)/100.,
                                                  [np.random.rand()+1, np.random.rand()+2, np.random.rand()+20])])
def test_specfit(rawdata, noise, error, params):
        for i in range(100):
                passed = True
                parameter_noise = [params[0] + abs(np.random.randn()) * parameter_error_amplitude[0], 
                               params[1] + abs(np.random.randn()) * parameter_error_amplitude[1],
                               params[2] + abs(np.random.randn()) * parameter_error_amplitude[2]]
                guesses = np.array(params)+parameter_noise
                sp = Spectrum(xarr=xarr, data=rawdata+noise, error=error,
                              header={})
                # sp.plotter(axis=plt.gca(), errstyle='fill')
                sp.specfit(guesses=guesses)
                assertion = ((np.array(sp.specfit.fitter.mpp)-np.array(params))/parameter_noise)**2
                print('(mpp - params / param_noise )^2 = ', assertion)
                for j,result in enumerate(assertion):
                        if strict_assertion:
                                assert result < 2
                        if result >= 2: 
                                passed = False
                                continue
                if passed:
                        for j in range(3):
                                passes['passes'][j]+=1
                                passes['avg_difference'][j] += abs(sp.specfit.fitter.mpp[j] - params[j])
                else:
                        for j in range(3):
                                fails['fails'][j]+=1
                                fails['avg_difference'][j] += abs(sp.specfit.fitter.mpp[j] - params[j])
                # plt.show()

        for i,j in enumerate(passes['avg_difference']):
                if passes['passes'][i]:
                        passes['avg_difference'][i] = j/passes['passes'][i]
        for i,j in enumerate(fails['avg_difference']):
                if fails['fails'][i]:
                        fails['avg_difference'][i] = j/fails['fails'][i]

        print('passes:', passes)
        print('fails:', fails)
