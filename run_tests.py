interactive=False
import subprocess
import os
import matplotlib

def test_everything(savedir=''):

    matplotlib.use('TkAgg')
    from matplotlib.pyplot import ion,ioff
    if interactive:
        ion()
    else:
        ioff()

    #test_units()
    from pyspeckit.spectrum.tests import test_units as tu
    for p in tu.params:
        tu.test_convert_units(*p)
        tu.test_convert_back(*p)

    curpath = os.getcwd()
    dir_prefix = os.path.split(os.path.abspath(__file__))[0]
    os.chdir(dir_prefix)

    print "*****test_fits.py*****"
    execfile(os.path.join(dir_prefix,'test_fits.py'),{'interactive':interactive,'savedir':savedir})
    print "*****test_hr2421.py*****"
    execfile(os.path.join(dir_prefix,'test_hr2421.py'),{'interactive':interactive,'savedir':savedir})
    print "*****test_sdss.py*****"
    execfile(os.path.join(dir_prefix,'test_sdss.py'),{'interactive':interactive,'savedir':savedir})
    print "*****test_txt.py*****"
    execfile(os.path.join(dir_prefix,'test_txt.py'),{'interactive':interactive,'savedir':savedir})
    print "*****simple_fit_example.py*****"
    execfile(os.path.join(dir_prefix,'simple_fit_example.py'),{'interactive':interactive,'savedir':savedir})
    print "*****simple_fit_interactive.py*****"
    execfile(os.path.join(dir_prefix,'simple_fit_interactive.py'),{'interactive':interactive,'savedir':savedir})
    print "*****alberto_example.py*****"
    execfile(os.path.join(dir_prefix,'alberto_example.py'),{'interactive':interactive,'savedir':savedir})

    print "*****test_formaldehyde_radex.py*****"
    execfile(os.path.join(dir_prefix,'test_formaldehyde_radex.py'),{'interactive':interactive,'savedir':savedir})
    print "*****test_formaldehyde.py*****"
    execfile(os.path.join(dir_prefix,'test_formaldehyde.py'),{'interactive':interactive,'savedir':savedir})

    print "*****vega_echelle.py*****"
    execfile(os.path.join(dir_prefix,'vega_echelle_example.py'),{'interactive':interactive,'savedir':savedir})

    print "*****test_voigt.py*****"
    execfile(os.path.join(dir_prefix,'test_voigt.py'))

    print "*****test_juliantxt.py*****"
    execfile(os.path.join(dir_prefix,'test_juliantxt.py'))

    print "*****test_nh3.py (run last because it is long)*****"
    execfile(os.path.join(dir_prefix,'test_nh3.py'),{'interactive':interactive,'savedir':savedir})

    print "Success!  Or at least, no exceptions..."
    os.chdir(curpath)

    #try:
    #    print "Running comparison"
    #    execfile(os.path.join(dir_prefix,'compare_images.py'))
    #except ImportError:
    #    print "Not comparing images because PIL was not installed."

