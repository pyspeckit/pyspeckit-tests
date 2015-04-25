import pyspeckit
sp = pyspeckit.Spectrum('janespec.txt', skiplines=2)
sp.units = 'W m$^{-2}$ Hz$^{-1}$'
sp.xarr.units = 'angstroms'
sp.xarr.xtype = 'wavelength'
sp.plotter()
