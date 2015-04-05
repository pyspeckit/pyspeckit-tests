import pyspeckit

def test_nh3_loading_regression():
    """
    Test that the spectofit and data are in the same order after loading
    """
    sp = pyspeckit.Spectrum('G032.020+00.065_nh3_22_Tastar.fits')

    # these should be the same data at this point, so we don't need to test
    # almost equal
    assert np.all(sp.specfit.spectofit == sp.data)

    # if this fails, it indicates a problem with _sort() in classes.py
    
if __name__ == "__main__":
    test_nh3_loading_regression()
