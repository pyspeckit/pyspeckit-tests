interactive=False
import subprocess
import os
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.pyplot import ion,ioff
if interactive:
    ion()
else:
    ioff()

#def test_units():
#    from pyspeckit.spectrum.tests import test_units as tu
#    for p in tu.params:
#        tu.test_convert_units(*p)
#        tu.test_convert_back(*p)

dir_prefix = os.path.split(os.path.abspath(__file__))[0]
if os.path.exists(dir_prefix):
    os.chdir(dir_prefix)

savedir = ''

if False:
    versnum = subprocess.Popen(["hg","id","--num"],stdout=subprocess.PIPE).communicate()[0].strip().strip("+")
    if versnum != "":
        savedir = "tests_%s/" % versnum
        if not os.path.exists(savedir):
            os.mkdir(savedir)
    else:
        savedir = ""

def test_everything():

    #test_units()
    from pyspeckit.spectrum.tests import test_units as tu
    for p in tu.params:
        tu.test_convert_units(*p)
        tu.test_convert_back(*p)

    print "*****test_fits.py*****"
    execfile('test_fits.py',{'interactive':interactive,'savedir':savedir})
    print "*****test_hr2421.py*****"
    execfile('test_hr2421.py',{'interactive':interactive,'savedir':savedir})
    #print "*****test_nh3.py*****"
    #execfile('test_nh3.py',{'interactive':interactive,'savedir':savedir})
    print "*****test_sdss.py*****"
    execfile('test_sdss.py',{'interactive':interactive,'savedir':savedir})
    print "*****test_txt.py*****"
    execfile('test_txt.py',{'interactive':interactive,'savedir':savedir})
    print "*****simple_fit_example.py*****"
    execfile('simple_fit_example.py',{'interactive':interactive,'savedir':savedir})
    print "*****simple_fit_interactive.py*****"
    execfile('simple_fit_interactive.py',{'interactive':interactive,'savedir':savedir})
    print "*****alberto_example.py*****"
    execfile('alberto_example.py',{'interactive':interactive,'savedir':savedir})

    print "*****test_formaldehyde_radex.py*****"
    execfile('test_formaldehyde_radex.py',{'interactive':interactive,'savedir':savedir})
    print "*****test_formaldehyde.py*****"
    execfile('test_formaldehyde.py',{'interactive':interactive,'savedir':savedir})

    print "*****vega_echelle.py*****"
    execfile('vega_echelle_example.py',{'interactive':interactive,'savedir':savedir})

    print "*****test_voigt.py*****"
    execfile('test_voigt.py')

    print "*****test_juliantxt.py*****"
    execfile('test_juliantxt.py')

    print "Success!  Or at least, no exceptions..."

    #try:
    #    print "Running comparison"
    #    execfile('compare_images.py')
    #except ImportError:
    #    print "Not comparing images because PIL was not installed."

