import numpy as np
from pyspeckit import SpectralCube
from pyspeckit.spectrum.units import SpectroscopicAxis
from pyspeckit.spectrum.models.inherited_gaussfitter import gaussian_fitter
from astropy import units as u

xarr = SpectroscopicAxis(np.linspace(-100, 100, 200), unit=u.Hz)
gf = gaussian_fitter()
params = [1., 2., 5.]
parameter_error_amplitude = [5., 5., 5.]
assertion = []
passes = {'passes': [0,0,0], 'avg_difference': [0,0,0]}
fails = {'fails': [0,0,0], 'avg_difference': [0, 0, 0]}

for i in range(20):
	parameter_noise = [params[0] + abs(np.random.randn()) * parameter_error_amplitude[0], 
	                   params[1] + abs(np.random.randn()) * parameter_error_amplitude[1],
	                   params[2] + abs(np.random.randn()) * parameter_error_amplitude[2]]
	guesses = np.array(params)+parameter_noise
	errspec = np.ones(xarr.size)
	data = gf.n_modelfunc(pars=params)(xarr)*100.+np.random.randn(xarr.size)

	cube = [[[x for x in data] for y in range(2)] for z in range(2)]
	cube = np.array(cube)
	cube = np.rollaxis(cube, 2, 0)
	sp = SpectralCube.Cube(xarr=xarr, cube=cube, unit='Hz')
	sp.fiteach(guesses=guesses, errspec=errspec, fitkwargs={'guesses':guesses})
	result_cube = sp.parcube
	for i in range(2):
		for j in range(2):
			print result_cube[:,i,j]
			passed = True
			for k,result in enumerate(result_cube[:,i,j]):
				if result >= 2: 
					passed = False
					continue
			if passed:
				for k in range(3):
					passes['passes'][k]+=1
					passes['avg_difference'][k] += abs(result_cube[:,i,j][k] - params[k])
			else:
				for k in range(3):
					fails['fails'][k]+=1
					fails['avg_difference'][k] += abs(result_cube[:,i,j][k] - params[k])
			assertion.append(((np.array(result_cube[:,i,j])-np.array(params))/parameter_noise)**2)

print 'result:', result
print 'assertion:', np.array(assertion)
print 'passes:', passes
print 'fails:', fails
