import pyspeckit
sp = pyspeckit.Spectrum('julian_infrared.txt')

# set up units properly
sp.xarr.set_unit='angstrom'
sp.xarr.xtype = 'wavelength'
sp.units = r'erg s$^{-1}$ cm$^{-2}$ $\AA^{-1}$'

# plot!
sp.plotter()
