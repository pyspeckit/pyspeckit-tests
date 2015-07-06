import numpy as np
from astropy.io import fits
import pyspeckit
import matplotlib.pyplot as plt

mycube= np.random.randn(250,50,50)
myaxis= np.linspace(-100,100,250)
pcube=pyspeckit.Cube(cube=mycube, xarr=myaxis, xunit='km/s')

sp = pcube.get_spectrum(5,5)

print pcube
print pcube.__repr__()
