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
    example_prefix = '/../../examples/'

    run_only_examples = False
    if not run_only_examples:

        print "*****test_nh3_loading_regression.py*****"
        execfile(os.path.join(dir_prefix,'test_nh3_loading_regression.py'))

        print "*****test_fits.py*****"
        execfile(os.path.join(dir_prefix,'test_fits.py'),{'interactive':interactive,'savedir':savedir})
        print "*****test_hr2421.py*****"
        execfile(os.path.join(dir_prefix,'test_hr2421.py'),{'interactive':interactive,'savedir':savedir})
        #print "*****test_nh3.py*****"
        #execfile(os.path.join(dir_prefix,'test_nh3.py'),{'interactive':interactive,'savedir':savedir})
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

        print "*****test_spectral_cube.py*****"
        execfile(os.path.join(dir_prefix,'test_spectral_cube.py'))

        print "*****test_moments.py*****"
        execfile(os.path.join(dir_prefix,'test_moments.py'))

        print "*****test_masking.py*****"
        execfile(os.path.join(dir_prefix,'test_masking.py'))

    print "#####Testing Examples#####"
    dir_prefix += example_prefix
        
    #NOT WORKING EXAMPLES
    #missing file
    # print "*****fit_nh3_cube.py*****"
    # execfile(os.path.join(dir_prefix,'fit_nh3_cube.py'))

    #ValueError: Set parameter value -0.42303302433020978 < limit value 0
    # print "*****multivoigt.py*****"
    # execfile(os.path.join(dir_prefix,'multivoigt.py'))
    
    # print "*****interactive_example_hr2421.py*****"
    # execfile(os.path.join(dir_prefix,'interactive_example_hr2421.py'))
    
    #WORKING EXAMPLES
    #runs 630 fits; left it out
    # print "*****n2hp_cube_example.py*****"
    # execfile(os.path.join(dir_prefix,'n2hp_cube_example.py'))
    # print "*****hcn_cube_test.py*****"
    # execfile(os.path.join(dir_prefix,'hcn_cube_test.py'))
    print "*****voigt.py*****"
    execfile(os.path.join(dir_prefix,'voigt.py'))
    print "*****sn_example.py*****"
    execfile(os.path.join(dir_prefix,'sn_example.py'))
    print "*****sn_deredden_example.py*****"
    execfile(os.path.join(dir_prefix,'sn_deredden_example.py'))
    print "*****n2hp_example.py*****"
    execfile(os.path.join(dir_prefix,'n2hp_example.py'))
    print "*****hcn_example.py*****"
    execfile(os.path.join(dir_prefix,'hcn_example.py'))
    print "*****doublet_example.py*****"
    execfile(os.path.join(dir_prefix,'doublet_example.py'))
    # print "*****agn_example.py*****"
    # execfile(os.path.join(dir_prefix,'agn_example.py'))
    print "*****ammonia_vtau_fit_example.py*****"
    execfile(os.path.join(dir_prefix,'ammonia_vtau_fit_example.py'))
    print "*****ammonia_fit_example.py*****"
    execfile(os.path.join(dir_prefix,'ammonia_fit_example.py'))    
    print "*****ammonia_vtau_multitem_example.py*****"
    execfile(os.path.join(dir_prefix,'ammonia_vtau_multitem_example.py'))

    print "Success!  Or at least, no exceptions..."
    os.chdir(curpath)

    #try:
    #    print "Running comparison"
    #    execfile(os.path.join(dir_prefix,'compare_images.py'))
    #except ImportError:
    #    print "Not comparing images because PIL was not installed."

