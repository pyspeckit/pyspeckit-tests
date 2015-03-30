import numpy as np
from pyspeckit.spectrum.models.gaussfitter import gaussian_fitter
from pyspeckit import Spectrum

xarr = np.linspace(-100,100,200)
gf = gaussian_fitter()
params = [1.0, 2.0, 0.5]
passes = {'passes': [0,0,0], 'avg_difference': [0,0,0]}
fails = {'fails': [0,0,0], 'avg_difference': [0, 0, 0]}

for i in range(100):
	parameter_noise = [abs(params[0]+np.random.randn()) / 5., abs(params[1] + np.random.randn())*5, abs(params[2] + np.random.randn())]
	guesses = np.array(params)+parameter_noise

	sp = Spectrum(xarr=xarr, data=gf.n_modelfunc(pars=params)(xarr))
	sp.specfit(guesses=guesses, verbose=False)
	print 'params:',params
	print 'guesses:',guesses
	assertion = ((np.array(sp.specfit.fitter.mpp)-np.array(params))/parameter_noise)**2
	print '(mpp - params / param_noise )^2 = ', assertion
	for j,result in enumerate(assertion):
		if result >= 2: 
			fails['fails'][j]+=1
			fails['avg_difference'][j] += abs(result - params[j])
			continue
		passes['passes'][j]+=1
		passes['avg_difference'][j] += abs(result - params[j])

for i,j in enumerate(passes['avg_difference']):
	passes['avg_difference'][i] = j/passes['passes'][i]
for i,j in enumerate(fails['avg_difference']):
	fails['avg_difference'][i] = j/fails['fails'][i]

print 'passes:', passes
print 'fails:', fails