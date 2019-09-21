import numpy as np
import os
import sys
import matplotlib
import warnings
from six.moves.urllib.error import URLError
from astropy.utils.console import ProgressBar
from astropy import wcs
from .utils import run_tests
interactive=False

# for python 3
def execute_file(fn, lglobals=None, llocals=None):
    with open(fn, 'rb') as f:
        code = compile(f.read(), fn, 'exec')

    if lglobals is None:
        lglobals = {}
    if llocals is None:
        llocals = {}
    lglobals.update({'__name__':fn})
    exec(code, lglobals, llocals)

def import_file(fn):
    __import__(os.path.splitext(os.path.basename(fn))[0])

def test_everything(savedir=''):

    warnings.simplefilter("error")
    warnings.filterwarnings("default", category=UserWarning)
    warnings.filterwarnings("ignore", category=ImportWarning) # for a cython bug: https://github.com/astropy/astropy/issues/6025
    warnings.filterwarnings("ignore", category=FutureWarning, module='h5py') # see commit message
    warnings.filterwarnings("ignore", category=PendingDeprecationWarning, module='astropy') # see commit message
    warnings.filterwarnings("ignore", category=PendingDeprecationWarning, module='astropy.wcs') # see commit message
    warnings.filterwarnings("ignore", category=PendingDeprecationWarning, module='numpy.matrixlib') # see commit message
    warnings.filterwarnings("ignore", category=FutureWarning, module='spectral_cube') # tuple(list(inds)); may need to be numpy
    try:
        warnings.filterwarnings("error", category=ResourceWarning)
    except NameError:
        # python2.7 didn't have ResourceWarnings
        pass
    warnings.filterwarnings("ignore",
                            message="elementwise == comparison failed; this will raise an error in the future.",
                            category=DeprecationWarning,
                            module='matplotlib')
    warnings.filterwarnings("ignore",
                            message="Using or importing the ABCs from 'collections' instead of from 'collections.abc' is deprecated, and in 3.8 it will stop working",
                            category=DeprecationWarning,
                            module='matplotlib') # may need to do this in collections?
    warnings.filterwarnings("ignore",
                            message="Using or importing the ABCs from 'collections' instead of from 'collections.abc' is deprecated, and in 3.8 it will stop working",
                            category=DeprecationWarning,
                            module='collections') # see above
    warnings.filterwarnings("ignore",
                            message="inspect.getargspec() is deprecated, use inspect.signature() instead",
                            category=DeprecationWarning,
                            module='sympy') # actually in yt; I don't import sympy
    warnings.filterwarnings("ignore",
                            message="inspect.getargspec",
                           )
    warnings.filterwarnings("ignore",
                            message="astropy.utils.compat.odict.OrderedDict is now deprecated - import OrderedDict from the collections module instead")
    warnings.filterwarnings("ignore",
                            message="The 'warn' method is deprecated, use 'warning' instead",
                            category=DeprecationWarning,
                            module='spectral_cube',
                           )
    warnings.filterwarnings("ignore",
                            message="More than 20 figures have been opened.")
    # I get some un-reproducible errors on travis, e.g.:
    # https://travis-ci.org/keflavich/pyspeckit/jobs/113880743
    warnings.filterwarnings("default",
                            category=RuntimeWarning)
    warnings.filterwarnings("ignore",
                            message="Parent module",
                            category=RuntimeWarning)

    warnings.filterwarnings("ignore",
                            module='IPython',
                            category=DeprecationWarning)
    warnings.filterwarnings("ignore",
                            module='ipython',
                            category=DeprecationWarning)
    warnings.filterwarnings("ignore",
                            message="IOStream",
                            category=DeprecationWarning)
    warnings.filterwarnings("ignore", category=DeprecationWarning,
                            message='np.asscalar(a) is deprecated since NumPy v1.16, use a.item() instead')


    with warnings.catch_warnings():
        # ignore matplotlib's "use has no effect" warning
        # on travis, at least, it should work
        warnings.simplefilter('ignore')
        matplotlib.use('TkAgg')
    from matplotlib.pyplot import ion,ioff
    if interactive:
        ion()
    else:
        ioff()

    with warnings.catch_warnings():
        # matplotlib raises errors related to color that we can't control
        warnings.filterwarnings('ignore', 'elementwise == comparison failed')
        from pyspeckit.spectrum.tests import test_eqw
        test_eqw.test_eqw()
        test_eqw.test_eqw_plot()

    from pyspeckit.spectrum.tests import test_fitter
    tf = test_fitter.TestFitter()
    tf.setup_method()
    run_tests(tf)
    #tf.test_init()
    #tf.test_copy()
    #tf.test_fitter()
    #tf.test_set_pars()
    #tf.test_set_tied()
    #tf.test_invalid_guess()
    #tf.test_almost_invalid_guess()
    #tf.test_multipeak()
    #tf.test_multipeak_tiny()

    #specutils is legacy & broken now
    # from pyspeckit.spectrum.readers.tests import test_specutils_reading
    # if test_specutils_reading.SPECUTILS_OK:
    #     with warnings.catch_warnings():
    #         warnings.filterwarnings("ignore")
    #         # this is a really weird one:
    #         # I get this error:
    #         # DeprecationWarning: numpy boolean subtract, the `-` operator, is deprecated, use the bitwise_xor, the `^` operator, or the logical_xor function instead.
    #         # but I can't reproduce it interactively
    #         # (sp[0] and sp[1] are *NOT* booleans; I checked!!!)
    #         # Ah, ok, actually, this is probably happening in operation_wrapper comparison region somehow
    #         test_specutils_reading.test_specutils_aao_reader_dontallowmismatchdiffs()
    #     test_specutils_reading.test_specutils_aao_reader_multiple()
    #     test_specutils_reading.test_specutils_aao_reader_single()


    from pyspeckit.cubes.SpectralCube import test_get_neighbors
    test_get_neighbors()

    with warnings.catch_warnings():
        # ignore FITS-related warnings
        warnings.filterwarnings('ignore', category=wcs.FITSFixedWarning)
        try:
            import spectral_cube
            from pyspeckit.cubes.tests import test_cubetools
            run_tests(test_cubetools)
            #test_cubetools.test_subimage_integ_header()
            #test_cubetools.test_fiteach()
            #test_cubetools.test_get_modelcube()
            #test_cubetools.test_get_modelcube_badpar()
            #test_cubetools.test_registry_inheritance()
            #test_cubetools.test_noerror_cube()
            #test_cubetools.test_slice_header()
            #test_cubetools.test_nonuniform_chan_weights()

            from pyspeckit.cubes.tests import test_spectralcube
            run_tests(test_spectralcube)
        except ImportError:
            pass

    #from pyspeckit.spectrum.models.tests import test_moments
    #for name in test_moments.names:
    #    print("testing moments for {0}".format(name))
    #    test_moments.test_moments(name)
    from pyspeckit.spectrum.models.tests import test_astropy_models
    test_astropy_models.test_powerlaw()
    from pyspeckit.spectrum.models.tests import test_template
    test_template.test_template()
    test_template.test_template_withcont()
    from pyspeckit.spectrum.models.tests import test_hyperfine
    test_hyperfine.test_hyperfine()
    from pyspeckit.spectrum.models.tests import test_hill5
    run_tests(test_hill5)
    from pyspeckit.spectrum.models.tests import test_ammonia
    run_tests(test_ammonia)
    #test_ammonia.test_ammonia_parlimits()
    #test_ammonia.test_ammonia_parlimits_fails()
    #test_ammonia.test_cold_ammonia()
    #test_ammonia.test_self_fit()

    #test_units()
    from pyspeckit.spectrum.tests import test_units
    tu = test_units.TestUnits.setup_class()()
    for p in ProgressBar(test_units.params):
        #print("Testing unit conversion with {0}".format(p))
        tu.test_convert_units(*p)
        tu.test_convert_back(*p)
    tu.test_equivalencies_1()
    for convention in ProgressBar(test_units.convention):
        tu.test_equivalencies_2(convention)
        tu.test_equivalencies_3(convention)
    tu.test_initialize_units()
    tu.test_convert_units2()
    tu.test_in_range()
    tu.test_x_to_pix()
    tu.test_comparison()
    tu.test_cdelt()



    #### SCRIPT TESTS BELOW ####


    curpath = os.getcwd()

    dir_prefix = os.path.split(os.path.abspath(__file__))[0]

    os.chdir(dir_prefix)
    example_prefix = '/../../examples/'

    run_only_examples = False
    if not run_only_examples:


        print("Running test directory scripts")
        print("dir_prefix={0}".format(dir_prefix))

        print("*****vega_echelle.py*****")
        # because python3 can't execfile, we have to import wav2rgb here and pass it in
        import wav2rgb
        execute_file(os.path.join(dir_prefix,'vega_echelle_example.py'),
                     {'interactive':interactive,'savedir':savedir, 'wav2rgb':wav2rgb})
        print("*****simple_fit_example.py*****")
        execute_file(os.path.join(dir_prefix,'simple_fit_example.py'),{'interactive':interactive,'savedir':savedir})
        print("*****simple_fit_interactive.py*****")
        execute_file(os.path.join(dir_prefix,'simple_fit_interactive.py'),{'interactive':interactive,'savedir':savedir})

        print("*****test_moments.py*****")
        execute_file(os.path.join(dir_prefix,'test_moments.py'))

        # regression test for issue w/error=None vs error=0, which changed
        # behavior from v0.9.7 to v0.9.11 of lmfit
        print("*****jdh_none_parinfo_test.py*****")
        execute_file(os.path.join(dir_prefix,'jdh_none_parinfo_test.py'))

        print("*****baseline_test_synth.py*****")
        execute_file(os.path.join(dir_prefix,'baseline_test_synth.py'))
        print("*****test_cube_init.py*****")
        execute_file(os.path.join(dir_prefix,'test_cube_init.py'))
        print("*****test_Cube_fiteach.py*****")
        import test_Cube_fiteach as tCf
        tCf.test_fiteach(
            tCf.gf.n_modelfunc(pars=tCf.params)(tCf.xarr.value),
            np.random.randn(tCf.xarr.value.size)/100.)

        print("*****test_nh3_loading_regression.py*****")
        execute_file(os.path.join(dir_prefix,'test_nh3_loading_regression.py'))

        print("*****test_fits.py*****")
        execute_file(os.path.join(dir_prefix,'test_fits.py'),{'interactive':interactive,'savedir':savedir})
        print("*****test_hr2421.py*****")
        execute_file(os.path.join(dir_prefix,'test_hr2421.py'),{'interactive':interactive,'savedir':savedir})
        #print("*****test_nh3.py*****")
        #execute_file(os.path.join(dir_prefix,'test_nh3.py'),{'interactive':interactive,'savedir':savedir})
        print("*****test_sdss.py*****")
        execute_file(os.path.join(dir_prefix,'test_sdss.py'),{'interactive':interactive,'savedir':savedir})
        print("*****test_txt.py*****")
        execute_file(os.path.join(dir_prefix,'test_txt.py'),{'interactive':interactive,'savedir':savedir})
        print("*****alberto_example.py*****")
        execute_file(os.path.join(dir_prefix,'alberto_example.py'),{'interactive':interactive,'savedir':savedir})

        print("*****test_formaldehyde_radex.py*****")
        execute_file(os.path.join(dir_prefix,'test_formaldehyde_radex.py'),{'interactive':interactive,'savedir':savedir})
        print("*****test_formaldehyde.py*****")
        execute_file(os.path.join(dir_prefix,'test_formaldehyde.py'),{'interactive':interactive,'savedir':savedir})
        print("*****mpl3_regression_i286.py*****")
        execute_file(os.path.join(dir_prefix,'mpl3_regression_i286.py'),{'interactive':interactive,'savedir':savedir})


        print("*****test_voigt.py*****")
        execute_file(os.path.join(dir_prefix,'test_voigt.py'))

        print("*****test_juliantxt.py*****")
        execute_file(os.path.join(dir_prefix,'test_juliantxt.py'))

        print("*****test_spectral_cube.py*****")
        execute_file(os.path.join(dir_prefix,'test_spectral_cube.py'))

        print("*****test_masking.py*****")
        execute_file(os.path.join(dir_prefix,'test_masking.py'))

        print("*****TEST_wrapper_nh3.py*****")
        execute_file(os.path.join(dir_prefix,'TEST_wrapper_nh3.py'))

        print("*****convert_to_unit regression test PR#12*****")
        sys.path.append(dir_prefix)
        from test_convert_to_unit import test_convert_to_unit
        test_convert_to_unit(run_with_assert=True)

    print("#####Testing Examples#####")
    dir_prefix += example_prefix

    #NOT WORKING EXAMPLES
    #missing file
    # print("*****fit_nh3_cube.py*****")
    # execute_file(os.path.join(dir_prefix,'fit_nh3_cube.py'))

    #ValueError: Set parameter value -0.42303302433020978 < limit value 0
    # print("*****multivoigt.py*****")
    # execute_file(os.path.join(dir_prefix,'multivoigt.py'))

    # print("*****interactive_example_hr2421.py*****")
    # execute_file(os.path.join(dir_prefix,'interactive_example_hr2421.py'))

    #WORKING EXAMPLES
    #runs 630 fits; left it out
    with warnings.catch_warnings():
        # nuclear option: need to get matplotlib/numpy interaction to NOT raise
        # deprecation warnings (we don't do anything deprecated in pyspeckit
        # as of this commit, but mpl does)
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        print("*****n2hp_cube_example.py*****")
        execute_file(os.path.join(dir_prefix,'n2hp_cube_example.py'))
    # missing files
    #print("*****hcn_cube_test.py*****")
    #execute_file(os.path.join(dir_prefix,'hcn_cube_test.py'))
    print("*****voigt.py*****")
    execute_file(os.path.join(dir_prefix,'voigt.py'))
    print("*****sn_example.py*****")
    execute_file(os.path.join(dir_prefix,'sn_example.py'))
    print("*****sn_deredden_example.py*****")
    execute_file(os.path.join(dir_prefix,'sn_deredden_example.py'))
    print("*****n2hp_example.py*****")
    execute_file(os.path.join(dir_prefix,'n2hp_example.py'))
    print("*****hcn_example.py*****")
    execute_file(os.path.join(dir_prefix,'hcn_example.py'))
    print("*****doublet_example.py*****")
    execute_file(os.path.join(dir_prefix,'doublet_example.py'))
    # print("*****agn_example.py*****")
    # execute_file(os.path.join(dir_prefix,'agn_example.py'))
    print("*****ammonia_vtau_fit_example.py*****")
    execute_file(os.path.join(dir_prefix,'ammonia_vtau_fit_example.py'))
    print("*****ammonia_fit_example.py*****")
    execute_file(os.path.join(dir_prefix,'ammonia_fit_example.py'))
    print("*****ammonia_fit_example_wrapper.py*****")
    execute_file(os.path.join(dir_prefix,'ammonia_fit_example_wrapper.py'))
    print("*****ammonia_vtau_multitem_example.py*****")
    execute_file(os.path.join(dir_prefix,'ammonia_vtau_multitem_example.py'))

    print("Success!  Or at least, no exceptions...")
    os.chdir(curpath)

    #try:
    #    print("Running comparison")
    #    execute_file(os.path.join(dir_prefix,'compare_images.py'))
    #except ImportError:
    #    print("Not comparing images because PIL was not installed.")

