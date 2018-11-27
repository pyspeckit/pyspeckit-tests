from astropy.table import Table
from astropy import log
from pyspeckit.spectrum import Spectrum

tbl = Table.read('problemspec.txt', format='ascii')

sp = Spectrum(xarr=tbl['x'], data=tbl['y'].data, header={})

#sp.specfit(guesses=[0.042577108420564426, 47.709708298124426, 0.6840788813117882], use_lmfit=True, quiet=False, debug=True)
#print(sp.specfit.modelpars, sp.specfit.modelerrs)

sp.plotter()

try:
    import lmfit
    #log.setLevel('DEBUG')
    sp.specfit(guesses=[0.042577108420564426, 47.709708298124426, 0.6840788813117882], use_lmfit=True, quiet=True, debug=False)
    print("lmfit modelpars, modelerrs: ", sp.specfit.modelpars, sp.specfit.modelerrs, sp.specfit.fitter.mp.ier)

    for par in sp.specfit.parinfo:
        assert par.error is None

except ImportError:
    # skip the test if lmfit is unavailable
    pass

sp.specfit(guesses=[0.042577108420564426, 47.709708298124426, 0.6840788813117882], use_lmfit=False, quiet=True, debug=False)
print("mpfit modelpars, modelerrs: ", sp.specfit.modelpars, sp.specfit.modelerrs, sp.specfit.fitter.mp.status)
print("NOTHING SHOULD BE PRINTED AFTER THIS")
#log.setLevel('INFO')

for par in sp.specfit.parinfo:
    assert par.error is None


# extra testing: figure out which parameters result in converged fits
#for ii in range(10):
#    randfac = 1+np.random.randn(1) * 0.001
#    sp.specfit(guesses=[0.042577108420564426*randfac, 47.709708298124426*randfac, 0.6840788813117882*randfac], use_lmfit=True, quiet=True, debug=False)
#    print("lmfit modelpars, modelerrs: ", sp.specfit.modelpars, sp.specfit.modelerrs, sp.specfit.fitter.mp.ier)
