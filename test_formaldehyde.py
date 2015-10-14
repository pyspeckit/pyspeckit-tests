from __future__ import print_function
import pyspeckit
from astropy import units as u
sp = pyspeckit.Spectrum('G203.04+1.76_h2co.fits',wcstype='D')
sp.xarr.center_frequency._unit = u.Hz
sp.xarr = sp.xarr.as_unit('km/s', equivalencies=u.doppler_radio(sp.xarr.center_frequency))
sp.specfit(fittype='formaldehyde',multifit=True,usemoments=True,guesses=[-0.6,4,0.2],equivalencies=u.doppler_optical(sp.xarr.center_frequency))
sp.plotter(figure=2)
sp.crop(-5*u.km/u.s,15*u.km/u.s)
sp.specfit(fittype='formaldehyde',multifit=True,usemoments=True,guesses=[-0.6,4,0.2])
sp.specfit(fittype='formaldehyde',multifit=True,usemoments=True,guesses=[-0.6,4,0.2])
sp.specfit.plot_fit(show_components=True)
sp.plotter.savefig("h2co_11_h2cofit.png")
print("Line integral (Formaldehyde,11): ",sp.specfit.integral())
print("Direct Line integral (Formaldehyde,11): ",sp.specfit.integral(direct=True,return_error=True))

sp2 = pyspeckit.Spectrum('G203.04+1.76_h2co.fits',wcstype='V')
sp2.xarr.convert_to_unit('km/s')
sp2.crop(-5*u.km/u.s,15*u.km/u.s)
sp2.plotter(figure=3)
sp2.specfit.peakbgfit(negamp=True, vheight=False)
sp2.specfit.peakbgfit(negamp=True, vheight=False)
sp2.plotter.savefig("h2co_11_gaussfit.png")
print("Line integral (Gaussian,11): ",sp2.specfit.integral())
print("Direct Line integral (Gaussian,11): ",sp2.specfit.integral(direct=True,return_error=True))


sp22g = pyspeckit.Spectrum('G203.04+1.76_h2co_Tastar.fits',wcstype='V')
sp22g.specfit.peakbgfit(negamp=True)
sp22g.xarr = sp22g.xarr.as_unit('km/s')
sp22g.plotter(figure=5)
sp22g.crop(-5*u.km/u.s,15*u.km/u.s)
sp22g.specfit.peakbgfit(negamp=True, vheight=False)
sp22g.specfit.peakbgfit(negamp=True, vheight=False)
sp22g.specfit.plot_fit()
sp22g.plotter.savefig("h2co_22_gaussfit.png")


sp22 = pyspeckit.Spectrum('G203.04+1.76_h2co_Tastar.fits',wcstype='V')
sp22.xarr.center_frequency._unit = u.Hz
sp22.specfit(fittype='formaldehyde',multifit=True,usemoments=True,guesses=[-0.3,4,0.2],equivalencies=u.doppler_radio(sp22.xarr.center_frequency))
sp22.xarr.convert_to_unit('km/s')
sp22.plotter(figure=4)
sp22.crop(-5*u.km/u.s,15*u.km/u.s)
sp22.specfit(fittype='formaldehyde',multifit=True,usemoments=True,guesses=[-0.6,4,0.2])
sp22.specfit(fittype='formaldehyde',multifit=True,usemoments=True,guesses=[-0.6,4,0.2])
sp22.specfit.plot_fit(show_components=True)
sp22.plotter.savefig("h2co_22_h2cofit.png")

print("Line integral (Formaldehyde,11): ",sp.specfit.integral())
print("Direct Line integral (Formaldehyde,11): ",sp.specfit.integral(direct=True,return_error=True))
print("Line integral (Gaussian,11): ",sp2.specfit.integral())
print("Direct Line integral (Gaussian,11): ",sp2.specfit.integral(direct=True,return_error=True))
print("Line integral (Formaldehyde,22): ",sp22.specfit.integral(linename='twotwo'))
print("Direct Line integral (Formaldehyde,22): ",sp22.specfit.integral(direct=True,return_error=True))
print("Line integral (Gaussian,22): ",sp22g.specfit.integral())
print("Direct Line integral (Gaussian,22): ",sp22g.specfit.integral(direct=True,return_error=True))
