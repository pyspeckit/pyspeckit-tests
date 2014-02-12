import pyspeckit
import matplotlib
import numpy as np

if not 'savedir' in globals():
    savedir = ''

# load a FITS-compliant spectrum
spec = pyspeckit.Spectrum('10074-190_HCOp.fits')
# The units are originally frequency (check this by printing spec.xarr.units).
# I want to know the velocity.  Convert!
# Note that this only works because the reference frequency is set in the header
# this is no longer necessary!  #spec.xarr.frequency_to_velocity()
# Default conversion is to m/s, but we traditionally work in km/s
spec.xarr.convert_to_unit('km/s')
# plot it up!
spec.plotter()
# Subtract a baseline (the data is only 'mostly' reduced)
spec.baseline(interactive=True)
event1 = matplotlib.backend_bases.MouseEvent('button_press_event', spec.plotter.axis.figure.canvas,143,223,button=1)
event2 = matplotlib.backend_bases.MouseEvent('button_press_event', spec.plotter.axis.figure.canvas,300,223,button=1)
event3 = matplotlib.backend_bases.MouseEvent('button_press_event', spec.plotter.axis.figure.canvas,572,223,button=1)
event4 = matplotlib.backend_bases.MouseEvent('button_press_event', spec.plotter.axis.figure.canvas,787,223,button=1)
event5 = matplotlib.backend_bases.MouseEvent('button_press_event', spec.plotter.axis.figure.canvas,787,223,button=2)
spec.baseline.event_manager(event1)
spec.baseline.event_manager(event2)
spec.baseline.event_manager(event3)
spec.baseline.event_manager(event4)
spec.baseline.event_manager(event5)
spec.baseline.highlight_fitregion()

spec.specfit(interactive=True)
event1 = matplotlib.backend_bases.KeyEvent('button_press_event', spec.plotter.axis.figure.canvas,x=463,y=570,key=2)
event2 = matplotlib.backend_bases.KeyEvent('button_press_event', spec.plotter.axis.figure.canvas,x=461,y=351,key=2)
event3 = matplotlib.backend_bases.KeyEvent('button_press_event', spec.plotter.axis.figure.canvas,x=403,y=256,key=1)
event4 = matplotlib.backend_bases.KeyEvent('button_press_event', spec.plotter.axis.figure.canvas,x=516,y=243,key=1)
event5 = matplotlib.backend_bases.KeyEvent('button_press_event', spec.plotter.axis.figure.canvas,x=597,y=257,key=3)
spec.specfit.event_manager(event1)
spec.specfit.event_manager(event2)
spec.specfit.event_manager(event3)
spec.specfit.event_manager(event4)
spec.specfit.event_manager(event5)

print "Includemask before excludefit: ",spec.xarr[spec.baseline.includemask]," length = ",spec.baseline.includemask.sum()
spec.baseline(excludefit=True)
print "Includemask after excludefit: ",spec.xarr[spec.baseline.includemask]," length = ",spec.baseline.includemask.sum()
spec.specfit(guesses=spec.specfit.modelpars)

spec.plotter.figure.savefig(savedir+"simple_fit_interactive_HCOp.png")

print "Doing the interactive thing now"
event1 = matplotlib.backend_bases.KeyEvent('key_press_event', spec.plotter.axis.figure.canvas,key='o')
event2 = matplotlib.backend_bases.MouseEvent('button_press_event', spec.plotter.axis.figure.canvas,button=1,x=-100,y=-0.07)
event2.xdata, event2.ydata = -100,-0.07
event2.x, event2.y= spec.plotter.axis.transData.transform_point((-100,-0.07))
event2.inaxes = spec.plotter.axis
event3 = matplotlib.backend_bases.MouseEvent('motion_notify_event', spec.plotter.axis.figure.canvas,button=1,x=20,y=0.16)
event3.inaxes = spec.plotter.axis
event4 = matplotlib.backend_bases.MouseEvent('button_release_event', spec.plotter.axis.figure.canvas,button=1,x=20,y=0.16)
event4.inaxes = spec.plotter.axis
event4.xdata, event4.ydata = 20,0.16
event4.x, event4.y= spec.plotter.axis.transData.transform_point((20,0.16))
spec.plotter.figure.canvas.toolbar.press_zoom(event2)
spec.plotter.figure.canvas.toolbar._xypress=[(event2.x,event2.y,spec.plotter.axis,0,spec.plotter.axis.viewLim.frozen(),spec.plotter.axis.transData.frozen())]
spec.plotter.figure.canvas.toolbar.drag_zoom(event3)
spec.plotter.figure.canvas.toolbar.release_zoom(event4)

#spec.plotter.debug=True
print "Includemask before excludefit with window limits: ",spec.xarr[spec.baseline.includemask]," length = ",spec.baseline.includemask.sum()
spec.baseline(excludefit=True,use_window_limits=True,highlight=True)
print "Includemask after excludefit with window limits: ",spec.xarr[spec.baseline.includemask]," length = ",spec.baseline.includemask.sum()
spec.specfit(use_window_limits=True)
spec.baseline.highlight_fitregion()

# Regression test: make sure baseline selection works
# this should *NOT* be 107!  107 is ALL data between -100 and +20
# this should be 102, which tells you that the fit has been excluded!
# (note added 2/12/2014)
print spec.baseline.includemask.sum()
assert spec.baseline.includemask.sum() == 102

event1 = matplotlib.backend_bases.KeyEvent('key_press_event', spec.plotter.axis.figure.canvas,key='B')
spec.plotter.parse_keys(event1)
print "spec.baseline.includemask.sum()",spec.baseline.includemask.sum()
assert spec.baseline.includemask.sum() == 0
event2 = matplotlib.backend_bases.MouseEvent('button_press_event', spec.plotter.axis.figure.canvas,button=1,x=-153.3,y=-0.007)
event2.inaxes,event2.button,event2.xdata,event2.ydata = spec.plotter.axis,1,-153.3,-0.007
spec.baseline.event_manager(event2,debug=True)
event2.inaxes,event2.button,event2.xdata,event2.ydata = spec.plotter.axis,1,-41.5,-0.01
spec.baseline.event_manager(event2,debug=True)
assert spec.baseline.includemask.sum() == 99

event2.inaxes,event2.button,event2.xdata,event2.ydata = spec.plotter.axis,1,59,-0.1
spec.baseline.event_manager(event2,debug=True)
event2.inaxes,event2.button,event2.xdata,event2.ydata = spec.plotter.axis,1,244,0.1
spec.baseline.event_manager(event2,debug=True)
assert spec.baseline.includemask.sum() == 264

event2.inaxes,event2.button,event2.xdata,event2.ydata = spec.plotter.axis,3,244,0.1
spec.baseline.event_manager(event2,debug=True)
np.testing.assert_array_almost_equal(spec.baseline.baselinepars, np.array([-0.00016474, -0.01488391]))


spec.baseline.selectregion(reset=True)
assert np.all(spec.baseline.includemask)
spec.baseline(interactive=True)
assert np.all(spec.baseline.includemask)
# reset_selection intentionally has a different behavior than reset
# for interactive, you want POSITIVE selection, not negative
spec.baseline(interactive=True, reset_selection=True)
assert np.all(True-spec.baseline.includemask)
