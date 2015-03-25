import pyspeckit

if not 'interactive' in globals():
    interactive=False
if not 'savedir' in globals():
    savedir = ''


# Dunham 2011 source ID 4091
sp_whole = pyspeckit.Spectrum('G031.947+00.076_nh3_11_Tastar.fits')#,wcstype='F')
sp = sp_whole.slice(60, 140, units='km/s', copy=False)

#sp.plotter(xmin=2.36875e10,xmax=2.36924e10) 
sp.plotter()
import pylab; pylab.ioff(); pylab.draw()
if interactive: raw_input("Plotter")
sp.smooth(2)
sp.plotter()
import pylab; pylab.ioff(); pylab.draw()
if interactive: raw_input("Plotter (smooth)")

amp,cen,wid = pyspeckit.moments.moments(sp.xarr, sp.data, vheight=False)
sp.specfit(negamp=False,debug=True,fittype='gaussian', guesses=[amp,cen,wid])
sp.plotter.figure.savefig(savedir+'nh3_gaussfit.png')
print "Guesses: ", sp.specfit.guesses
print "Best fit: ", sp.specfit.modelpars

sp.baseline(exclude=[74,120],order=0)
#print "Plotter min/max: ",sp.plotter.xmin,sp.plotter.xmax," Fitter min/max: ",sp.specfit.gx1,sp.specfit.gx2," Fitregion= ",sp.baseline.excludevelo,sp.baseline.excludepix
#if interactive: raw_input('Baseline')
#sp.specfit(fittype='ammonia',guesses=[20,20,1e16,1.0,-55.0,0.5],quiet=False,xunits='Hz')
sp.specfit(fittype='ammonia',
           guesses=[5.9,4.45,14.919,0.84,96.2,0.43],quiet=False)
sp.specfit.plotresiduals()
if interactive: raw_input('Press enter to print guesses and zoom in.')
sp.plotter.figure.savefig(savedir+'nh3_ammonia_fit.png')
print "Guesses: ", sp.specfit.guesses
print "Best fit: ", sp.specfit.modelpars
sp.plotter(xmin=70,xmax=125)
sp.specfit.plot_fit()
sp.plotter.figure.savefig(savedir+'nh3_ammonia_fit_zoom.png')
if interactive: raw_input('Press enter to fit')
sp.specfit(fittype='ammonia',
        guesses=[4,3.5,14.69,0.68,97.3,0.5]+[15,4.2,14.85,0.52,95.8,0.35],
        quiet=False)
sp.specfit.plotresiduals()
sp.plotter.figure.savefig(savedir+'nh3_ammonia_multifit_zoom.png')

sp.specfit(fittype='ammonia',
           guesses=[5.9,4.45,14.919,0.84,96.2,0.5],fixed=[False,False,False,False,False,True],quiet=False)
if len(sp.specfit.parinfo) != 6:
    raise ValueError("parinfo has wrong number of parameters")
sp.plotter.figure.savefig(savedir+'nh3_ammonia_fit_fixedfortho.png')

try:
    sp.specfit(fittype='ammonia',
               guesses=[4,3.5,14.69,0.68,97.3,0.5]+[15,4.2,14.85,0.52,95.8,0.5]
            ,fixed=[False,False,False,False,False,True]*2,quiet=False,use_lmfit=True,debug=True)
except ImportError as ex:
    log.warn("Could not import lmfit: {0}".format(ex))
    sp.specfit(fittype='ammonia',
               guesses=[4,3.5,14.69,0.68,97.3,0.5]+[15,4.2,14.85,0.52,95.8,0.5]
            ,fixed=[False,False,False,False,False,True]*2,quiet=False,use_lmfit=False,debug=True)
print sp.specfit.parinfo
sp.plotter.figure.savefig(savedir+'nh3_ammonia_multifit_fixedfortho_lmfit.png')

sp.specfit(fittype='ammonia',
           guesses=[4,3.5,14.69,0.68,97.3,0.5]+[15,4.2,14.85,0.52,95.8,0.5]
        ,fixed=[False,False,False,False,False,True]*2,quiet=False)
sp.plotter.figure.savefig(savedir+'nh3_ammonia_multifit_fixedfortho.png')

anothertry=True
if anothertry:
    try: 
        sp.specfit(fittype='ammonia',
                   guesses=[4,3.5,14.69,0.68,97.3,0.0]+[15,4.2,14.85,0.52,95.8,0.0]
                ,fixed=[False,False,False,False,False,True]*2,quiet=False,use_lmfit=True)
    except ImportError as ex:
        log.warn("Could not import lmfit: {0}".format(ex))
        sp.specfit(fittype='ammonia',
                   guesses=[4,3.5,14.69,0.68,97.3,0.0]+[15,4.2,14.85,0.52,95.8,0.0]
                ,fixed=[False,False,False,False,False,True]*2,quiet=False,use_lmfit=False)
    print sp.specfit.parinfo
    sp.plotter.figure.savefig(savedir+'nh3_ammonia_multifit_fixedfortho0_lmfit.png')

    sp.specfit(fittype='ammonia',
               guesses=[4,3.5,14.69,0.68,97.3,0.0]+[15,4.2,14.85,0.52,95.8,0.0]
            ,fixed=[False,False,False,False,False,True]*2,quiet=False)
    sp.plotter.figure.savefig(savedir+'nh3_ammonia_multifit_fixedfortho0.png')

from pyspeckit.spectrum.models import ammonia

taudict1 = ammonia.ammonia(sp.xarr, tkin=sp.specfit.parinfo.tkin0.value,
                           tex=sp.specfit.parinfo.tex0.value,
                           ntot=sp.specfit.parinfo.ntot0.value,
                           width=sp.specfit.parinfo.width0.value,
                           return_tau=True)
taudict2 = ammonia.ammonia(sp.xarr, tkin=sp.specfit.parinfo.tkin1.value,
                           tex=sp.specfit.parinfo.tex1.value,
                           ntot=sp.specfit.parinfo.ntot1.value,
                           width=sp.specfit.parinfo.width1.value,
                           return_tau=True)

# From Dunham 2011: should be either 4.03 or 4.54 or both
# But I get 3.41 and 5.69 and the fit looks good
assert 4.5 < taudict1['oneone'] < 4.6
assert 6.8 < taudict2['oneone'] < 6.9

# This works, but it probably yields unphysical temperatures
#sp.specfit(fittype='ammonia', multifit=True,
#           guesses=[15,1e10,14.19,0.68,97.3,0.5]+[15,1e10,14.15,0.52,95.8,0.35],
#           fixed=[False,True,False,False,False,False]*2,
#           quiet=False)
#
#taudict2 = ammonia.ammonia(sp.xarr, tkin=sp.specfit.parinfo.tkin0.value,
#                          tex=sp.specfit.parinfo.tex0.value,
#                          ntot=sp.specfit.parinfo.ntot0.value,
#                          width=sp.specfit.parinfo.width0.value,
#                          return_tau=True)

if interactive: raw_input('Press enter to end code')
