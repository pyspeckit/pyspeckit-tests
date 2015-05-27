#!/usr/bin/python

from astropy.io import fits
from astropy import wcs
import IPython
import sys

import os
for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith(".fits"):
            try:
                hdr = fits.getheader(file)
                print "%s naxis before: %d" % (file, hdr.get('NAXIS'))
                oldwcs = wcs.WCS(hdr)
                # IPython.embed()
                newwcs = oldwcs.sub([wcs.WCSSUB_SPECTRAL])
                print "%s naxis: %d" % (file, newwcs.naxis)
            except:
                print "skipping "+ file
