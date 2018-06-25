from __future__ import print_function
import pyspeckit
from pylab import *
from numpy import *
from pyspeckit.spectrum.models.inherited_lorentzian import lorentzian_fitter

x,Rexx,Imxx,Rexy,Imxy=loadtxt('KhiXD1281286HzFreq.txt',usecols=(0,1,2,3,4),unpack=True)

pos=Imxx+Rexy
neg=Imxx-Rexy

z=pos

y=[]
for i in range(97):
    y=append(y,(float(i+0.5)-49.)/49*ones(239))

Z=resize(z,(97,239))
imshow(Z)

## sp.specfit.annotate(loc='lower right')

def is_local_maximum(amp, channel):
    if (amp[channel] > amp[channel-1] and
        amp[channel] > amp[channel+1] and
        amp[channel+1] > amp[channel+3] and
        amp[channel-1] > amp[channel-3]):
        return True
    else:
        return False

def measure_peak(counts, channels, max_channel, width):
    mean = 0.0
    stdev = 0.0
    total_counts = 0.0
    for i in range(max_channel-width, max_channel+width):
        total_counts += counts[i]
        mean += counts[i]*channels[i]
    mean = mean/total_counts
    for i in range(max_channel-width, max_channel+width):
        stdev += counts[i]*(channels[i]-mean)**2
    stdev = math.sqrt(stdev/total_counts)
    return mean, stdev

def findpks(amp, channels, min_sigma):
    background=0.; background_rms=max(amp)*0.0+1.0; data=[]
    minimum_signal = background+background_rms
    for i in range(3, len(channels)-3):
        if amp[i] < minimum_signal:
            continue # Ignore noise
        if is_local_maximum(amp, i):
           mean, stdev = measure_peak(amp, channels, i, 4)
           if stdev > min_sigma :
               data+=[amp[i],channels[i],stdev]
    guesses=data
    tied = []
    for i in range(len(guesses)):
        if i%3 == 2:
            tied+=['p['+str(i-1)+'] * 0.013']
        else:
            tied+=['']
    return guesses, tied


def fixparams(value):
    fixed=[]
    for i in range(len(guesses)/3):
        fixed+=value
    return fixed

def limitparams(j,value):
    minp = []
    maxp = []
    lmin = []
    lmax = []
    for i, element in enumerate(guesses):
        minp.append(element - value * element)
        maxp.append(element + value * element)
        if i % 3 == j:
            lmin.append(True)
            lmax.append(True)
        else:
            lmin.append(False)
            lmax.append(False)
    return minp, maxp, lmin, lmax

def fitrow(n):
    global guesses,sp
    Y=z[239*n:239*(n+1)]; X=x[239*n:239*(n+1)]
    xarr = pyspeckit.spectrum.units.SpectroscopicAxis(X)
    yarr = pyspeckit.spectrum.units.SpectroscopicAxis(Y)
    sp = pyspeckit.Spectrum(xarr=xarr, data=yarr, header={})
    sp.specfit.Registry.add_fitter('lorentzian',
                                   lorentzian_fitter(),
                                   3,
                                   multisingle='multi',
                                   key='L')
    ## sp.Registry.add_fitter ('lorentzian',lorentzian_fitter(multisingle='multi'),3,multisingle='multi',key='L')
    sp.plotter()
    ## sp.smooth(2)
    guesses,tied=findpks(Y,X,1e5)
    if len(guesses) == 0:
        return [0.,1.,1.]
    minp, maxp, lmin, lmax = limitparams(1,0.02)
    sp.specfit(fittype='gaussian',multifit=True,negamp=False,annotate=False,
               limitedmin=lmin, limitedmax=lmax, minpars=minp, maxpars=maxp,
               guesses=guesses,tied=tied,quiet=True)
    guesses=sp.specfit.modelpars; fixed=fixparams([True,True,False])
    minp, maxp, lmin, lmax = limitparams(2,3)
    ## minp, maxp, lmin, lmax = limitparams(2,0.05)
    sp.specfit(fittype='gaussian',multifit=True,negamp=False,annotate=False,
               limitedmin=lmin, limitedmax=lmax, minpars=minp, maxpars=maxp,
               guesses=guesses,fixed=fixed,quiet=True)
    guesses=sp.specfit.modelpars; fixed=fixparams([False,True,True])
    sp.specfit(fittype='lorentzian',multifit=True,negamp=False,annotate=False,
               guesses=guesses,fixed=fixed,quiet=True)
    guesses=sp.specfit.modelpars; fixed=fixparams([True,True,False])
    minp, maxp, lmin, lmax = limitparams(2,0.2)
    sp.specfit(fittype='lorentzian',multifit=True,negamp=False,annotate=False,
               limitedmin=lmin, limitedmax=lmax, minpars=minp, maxpars=maxp,
               guesses=guesses,fixed=fixed,quiet=True)
    ## guesses=sp.specfit.modelpars
    ## sp.specfit(fittype='lorentzian',multifit=True,guesses=guesses,annotate=False)  
    return sp.specfit.modelpars

def savefit(n,pars):
    filename='khipos.dat'
    with open(filename, 'a') as f:
        savetxt(f,[n]+pars, fmt='%1.6e', newline='\t')
        print('', file=f)

field=linspace(1.2,-1.2,97)
for n in range(20,22):
    pars=fitrow(n)
    savefit(field[n],pars)

n=13
fitrow(n)



## n=12,16
## fitrow(n)

## sp.Registry.peakbgfitters
## sp.Registry.multifitters




## Y=z[239*n:239*(n+1)]; X=x[239*n:239*(n+1)]
## guesses,tied=findpks(Y,X,1e5)
## xarr = pyspeckit.spectrum.units.SpectroscopicAxis(X)
## yarr = pyspeckit.spectrum.units.SpectroscopicAxis(Y)
## sp = pyspeckit.Spectrum(xarr=xarr,data=yarr)
## sp.plotter()
## sp.specfit(fittype='gaussian',multifit=True,guesses=guesses,tied=tied,quiet=False,negamp=False,annotate=False)
## guesses=sp.specfit.modelpars
## fixed=lw(guesses)
## sp.specfit(fittype='lorentzian',multifit=True,guesses=guesses,fixed=fixed,quiet=False,negamp=False,annotate=False)

## sp.specfit.multifit(fittype='lorentzian',guesses=guesses,fixed=fixed)
