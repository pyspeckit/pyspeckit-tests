import numpy as np
from astropy import wcs
import pyspeckit

def make_fake_cube():
    from spectral_cube import SpectralCube

    simpleFakeCube = np.empty([25,2,2])
    xarr = np.linspace(-20,20,25)
    simpleFakeCube[:,0,0] = np.exp(-(xarr-1)**2/(2*3.**2))
    simpleFakeCube[:,1,0] = np.exp(-(xarr+1)**2/(2*3.**2))
    simpleFakeCube[:,0,1] = np.exp(-(xarr+1)**2/(2*4.**2))
    simpleFakeCube[:,1,1] = np.exp(-(xarr-1)**2/(2*4.**2))

    w = wcs.WCS(naxis=3, header={'CUNIT3': 'km s-1', 'CDELT3':1.0, 'CRVAL3': 0,
                                 'CRPIX3': 12.5, 'CTYPE2':'DEC--TAN', 'CTYPE1':
                                 'RA---TAN', 'CDELT2':1./3600, 'CDELT1':
                                 1/3600., 'CRVAL2': 25.0, 'CRVAL1': 12.0,
                                 'CRPIX2': 1, 'CRPIX1': 1})
    sc = SpectralCube(data=simpleFakeCube, wcs=w, meta={'BUNIT': 'K'})

    return sc

def test_load_cube_from_spectralcube():
    sc = make_fake_cube()
    pcube = pyspeckit.Cube(cube=sc)

    assert pcube.unit == 'K'
    assert pcube.xarr.unit == 'km/s'

    return pcube

if __name__ == "__main__":
    test_load_cube_from_spectralcube()
