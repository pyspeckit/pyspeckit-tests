import numpy as np
from pyspeckit import SpectralCube

xarr = np.linspace(-100, 100, 200)
cube = [[[x for x in xarr] for y in range(2)] for z in range(2)]
cube = np.array(cube)
cube = np.rollaxis(cube, 2, 0)

guesses = (1.0, 50.0, 20.0)
sp = SpectralCube.Cube(xarr=xarr, cube=cube)
sp.fiteach(guesses=guesses)