from __future__ import print_function
import pyspeckit
import matplotlib
import numpy as np
from astropy import units as u
from distutils.version import StrictVersion

if not 'savedir' in globals():
    savedir = ''

# load a FITS-compliant spectrum
spec = pyspeckit.Spectrum('10074-190_HCOp.fits')
# The units are originally frequency (check this by printing spec.xarr.units).
# I want to know the velocity.  Convert!
# Note that this only works because the reference frequency is set in the header
# this is no longer necessary!  #spec.xarr.frequency_to_velocity()
# Default conversion is to m/s, but we traditionally work in km/s
spec.xarr = spec.xarr.as_unit('km/s', equivalencies=u.doppler_radio(spec.xarr.center_frequency))
# plot it up!
spec.plotter()
# Subtract a baseline (the data is only 'mostly' reduced)
spec.baseline(interactive=True)

# specify x points in data units.  We need to transform them to axis units
# because the axis are not consistently generated by mpl
xpoints = [-270,0,50,218,218]
ypoints = [0]*5
buttons = [1,1,1,1,2]
transform = spec.plotter.axis.transData.transform_point
# this absolutely ridiculous line is to deal with scope changes from py2->py3
# http://stackoverflow.com/questions/13905741/accessing-class-variables-from-a-list-comprehension-in-the-class-definition#comment19179733_13913933
def xy_(transform, xpoints, ypoints):
    return [transform((xp,yp)) for xp,yp in zip(xpoints,ypoints)]
xy = xy_(transform, xpoints, ypoints)

mouseevent = matplotlib.backend_bases.MouseEvent
def events_(MouseEvent=matplotlib.backend_bases.MouseEvent,
            canvas=spec.plotter.axis.figure.canvas,
            xy=xy,
            buttons=buttons):
    return [MouseEvent('button_press_event', canvas,
                       xp, yp, button=bt) for (xp,yp),bt in zip(xy,buttons)]
events = events_()

for ev in events:
    print("Events x={0},y={1},button={2}".format(ev.xdata,ev.ydata,ev.button))
    spec.baseline.event_manager(ev)

spec.baseline.highlight_fitregion()

spec.specfit(interactive=True)

xpoints = [0,50,26,28,28]
ypoints = [0, 0, 0.14, 0.07, 0]
buttons = [1,1,2,2,3]
xy = xy_(transform, xpoints, ypoints)

def events_(KeyEvent=matplotlib.backend_bases.KeyEvent,
            canvas=spec.plotter.axis.figure.canvas,
            xy=xy,
            buttons=buttons):
    return [KeyEvent('button_press_event', canvas,
                     x=xp, y=yp, key=bt) for (xp,yp),bt in zip(xy,buttons)]
events = events_(matplotlib.backend_bases.KeyEvent,
                 spec.plotter.axis.figure.canvas, xy, buttons)

for ev in events:
    print("Events x={0},y={1}".format(ev.xdata,ev.ydata))
    spec.specfit.event_manager(ev)

print("Includemask before excludefit: ",spec.xarr[spec.baseline.includemask]," length = ",spec.baseline.includemask.sum())
assert spec.baseline.includemask.sum() > 0
spec.baseline(excludefit=True)
spec.baseline.highlight_fitregion()
print("Includemask after excludefit: ",spec.xarr[spec.baseline.includemask]," length = ",spec.baseline.includemask.sum())
assert spec.baseline.includemask.sum() > 0
spec.specfit(guesses=spec.specfit.modelpars)

np.testing.assert_array_almost_equal(spec.specfit.parinfo.values,
                                     np.array([0.149995,  27.160603,   0.930399]))


spec.plotter.figure.savefig(savedir+"simple_fit_interactive_HCOp.png")

print("Doing the interactive thing now")
event1 = matplotlib.backend_bases.KeyEvent('key_press_event', spec.plotter.axis.figure.canvas,key='o')
# event 1 is clicking the zoom button
x,y = transform((-20,-0.07))
event2 = matplotlib.backend_bases.MouseEvent('button_press_event', spec.plotter.axis.figure.canvas,button=1,x=x,y=y)
event2.inaxes = spec.plotter.axis

event3 = matplotlib.backend_bases.MouseEvent('motion_notify_event', spec.plotter.axis.figure.canvas,button=1,x=x,y=y)
event3.inaxes = spec.plotter.axis

x,y = transform((75,0.16))
event4 = matplotlib.backend_bases.MouseEvent('button_release_event', spec.plotter.axis.figure.canvas,button=1,x=x,y=y)
event4.inaxes = spec.plotter.axis

if hasattr(spec.plotter.figure.canvas,'toolbar'):
    spec.plotter.figure.canvas.toolbar.press_zoom(event2)
    # mpl 1.5:
    # lastx, lasty, a, ind, view = self._xypress[0]
    if StrictVersion(matplotlib.__version__) >= StrictVersion('1.5.0'):
        spec.plotter.figure.canvas.toolbar._xypress=[(event2.x,event2.y,spec.plotter.axis,0,spec.plotter.axis.viewLim.frozen())]
    else:
        spec.plotter.figure.canvas.toolbar._xypress=[(event2.x,event2.y,spec.plotter.axis,0,spec.plotter.axis.viewLim.frozen(),spec.plotter.axis.transData.frozen())]
    spec.plotter.figure.canvas.toolbar.drag_zoom(event3)
    spec.plotter.figure.canvas.toolbar.release_zoom(event4)

    # make sure zoom worked
    try:
        np.testing.assert_array_almost_equal(spec.plotter.axis.get_xlim(), [-20, 75])
    except AssertionError:
        # in a few versions of matplotlib, for reasons I can't understand (10/20/2018), the zoom limits are
        # array([-20.778546,  73.879274]), which is definitely wrong, but I don't know how to test this or
        # reproduce it.  It happens on mpl1.5 and mpl3 on python3.6, but not mpl2.  Maybe one of travis's setups
        # is different?
        if (np.abs(spec.plotter.axis.get_xlim()[0] + 20) > 1) or (np.abs(spec.plotter.axis.get_xlim()[1] - 75) > 2):
            raise ValueError("Zooming failed by more than one pixel")
    np.testing.assert_array_almost_equal(spec.plotter.axis.get_ylim(), [-0.07, 0.16])
else:
    spec.plotter.axis.set_xlim(-20, 75)
    spec.plotter.axis.set_ylim(-0.07, 0.16)

#spec.plotter.debug=True
print("Includemask before excludefit with window limits: ",spec.xarr[spec.baseline.includemask]," length = ",spec.baseline.includemask.sum())
assert spec.baseline.includemask.sum() == 507
assert spec.plotter.xmin < -286*u.km/u.s
assert spec.plotter.xmax > -286*u.km/u.s
np.testing.assert_array_almost_equal(spec.plotter.axis.get_xlim(), (-20.0, 75.0))
spec.baseline(excludefit=True, use_window_limits=True, highlight=True)
np.testing.assert_array_almost_equal(spec.plotter.axis.get_xlim(), (-20.0, 75.0))
assert spec.plotter.xmin < -10*u.km/u.s
assert spec.plotter.xmax > 60*u.km/u.s
spec.baseline.highlight_fitregion()
print("Includemask after excludefit with window limits: ",spec.xarr[spec.baseline.includemask]," length = ",spec.baseline.includemask.sum())
# total 512 pixels, 5 (or 7?) should be excluded inside, 80 should be available
assert spec.baseline.includemask.sum() == 80
spec.specfit(guesses='moments', use_window_limits=True)
np.testing.assert_array_almost_equal(spec.specfit.parinfo.values,
                                     np.array([0.151523,  27.162823,   0.942997]))

# Regression test: make sure baseline selection works
# this should *NOT* be 107!  107 is ALL data between -100 and +20
# this should be 103, which tells you that the fit has been excluded!
# (note added 2/12/2014) - now changed because the
print(spec.baseline.includemask.sum())
assert spec.baseline.includemask.sum() == 80
assert ~spec.baseline.includemask[spec.xarr.x_to_pix(27.6)]

event1 = matplotlib.backend_bases.KeyEvent('key_press_event', spec.plotter.axis.figure.canvas,key='B')
spec.plotter.parse_keys(event1)
print("spec.baseline.includemask.sum()",spec.baseline.includemask.sum())
assert spec.baseline.includemask.sum() == 0
x,y = transform((-83.3,-0.007))
event2 = matplotlib.backend_bases.MouseEvent('button_press_event', spec.plotter.axis.figure.canvas,button=1,x=x,y=y)
event2.inaxes,event2.button,event2.xdata,event2.ydata = spec.plotter.axis,1,-83.3,-0.007
spec.baseline.event_manager(event2,debug=True)
event2.inaxes,event2.button,event2.xdata,event2.ydata = spec.plotter.axis,1,23,-0.01
spec.baseline.event_manager(event2,debug=True)
assert spec.baseline.includemask.sum() == 95

event2.inaxes,event2.button,event2.xdata,event2.ydata = spec.plotter.axis,1,35,-0.1
spec.baseline.event_manager(event2,debug=True)
event2.inaxes,event2.button,event2.xdata,event2.ydata = spec.plotter.axis,1,141,0.1
spec.baseline.event_manager(event2,debug=True)
assert spec.baseline.includemask.sum() == 189

event2.inaxes,event2.button,event2.xdata,event2.ydata = spec.plotter.axis,3,204,0.1
spec.baseline.event_manager(event2,debug=True)
spec.plotter.axis.set_xlim(-100, 150)
spec.baseline.highlight_fitregion()
np.testing.assert_array_almost_equal(spec.baseline.baselinepars,
                                     np.array([-0.00024 ,  0.043014]))


spec.baseline.selectregion(reset=True)
assert np.all(spec.baseline.includemask)
spec.baseline(interactive=True)
assert np.all(spec.baseline.includemask)
# reset_selection intentionally has a different behavior than reset
# for interactive, you want POSITIVE selection, not negative
spec.baseline(interactive=True, reset_selection=True)
assert np.all(~spec.baseline.includemask)
