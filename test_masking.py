import numpy as np
from astropy import units as u
import pyspeckit

x = np.linspace(-50,50)
y = np.exp(-x**2/(5.**2*2))
error = np.ones_like(x,dtype='float')/10.
e = np.random.randn(x.size) * error

def test_chi2_consistency_when_masking():

    sp = pyspeckit.Spectrum(xarr=x*u.km/u.s, data=y+e,
                            error=error, header={})
    sp.specfit(fittype='gaussian', guesses=[1,0,1])
    assert sp.specfit.dof == x.size - sp.specfit.fitter.npars

    chi2_a = sp.specfit.chi2
    chi2_a = sp.specfit.chi2
    chi2_a_correct = ((sp.data-sp.specfit.model)**2/error**2).sum()
    np.testing.assert_almost_equal(chi2_a, chi2_a_correct)

    mask_out = np.abs(x)>40
    y2 = np.ma.masked_where(mask_out, y)
    sp2 = pyspeckit.Spectrum(xarr=x*u.km/u.s, data=y2+e,
                             error=error, header={})
    sp2.specfit(fittype='gaussian', guesses=[1,0,1])
    assert sp2.specfit.dof == x.size - mask_out.sum() - sp2.specfit.fitter.npars

    chi2_b = sp2.specfit.chi2
    chi2_b_correct = ((sp2.data-sp2.specfit.get_full_model())**2/error**2).sum()
    np.testing.assert_almost_equal(chi2_b, chi2_b_correct)
    chi2_b_correct2 = ((sp2.data[~mask_out] - sp2.specfit.get_full_model()[~mask_out])**2
                       / error[~mask_out]**2).sum()
    np.testing.assert_almost_equal(chi2_b_correct, chi2_b_correct2)

def test_setfitspec():
    mask_out = np.abs(x)>40
    y2 = np.ma.masked_where(mask_out, y)
    sp2 = pyspeckit.Spectrum(xarr=x*u.km/u.s, data=y2+e,
                             error=error, header={})
    assert np.all(sp2.data.mask == sp2.specfit.spectofit.mask)

    sp2.specfit(fittype='gaussian', guesses=[1,0,1])


if __name__ == "__main__":
    test_chi2_consistency_when_masking()
    test_setfitspec()
