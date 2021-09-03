#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Python script of how to use XCLASS outside CASA
#
# Description:
#
# - this script contains examples of how to set the variables
#   and execute XCLASS outside CASA
#
# - play around with user parameters defined in lines 80 - 203
#
#
# Usage (in the terminal):
#
#   python3 my_myxclass_no-CASA.py
#
#
#  Who                  When            What
#
#  A. Sanchez-Monge     2015-07-01      initial version
#  T. Moeller           2020-02-12      porting to python 3
#
#******************************************************************************


#------------------------------------------------------------------------------
# import python packages
import sys
import os
#------------------------------------------------------------------------------


##-----------------------------------------------------------------------------
##
## start main program
##
if __name__ == '__main__':


    ## get path of current directory
    LocalPath = os.getcwd() + "/"

    #--------------------------------------------------------------------------
    # extend sys.path variable


    # get path of XCLASS directory
    XCLASSRootDir = str(os.environ.get('XCLASSRootDir', '')).strip()
    XCLASSRootDir = os.path.normpath(XCLASSRootDir) + "/"


    # extend sys.path variable
    NewPath = XCLASSRootDir + "build_tasks/"
    if (not NewPath in sys.path):
        sys.path.append(NewPath)


    # import XCLASS packages
    import task_UpdateDatabase
    import task_DatabaseQuery
    import task_ListDatabase
    import task_LoadASCIIFile
    import task_GetTransitions
    import task_MAGIX
    import task_myXCLASS
    import task_myXCLASSPlot
    import task_myXCLASSFit
    import task_myXCLASSMapFit
    import task_myXCLASSMapRedoFit


    #--------------------------------------------------------------------------
    # create synthetic spectrum with myXCLASSFit task


    ###########################################################################
    # TO MODIFY BY THE USER

    # define path and name of molfit file
    #DEFAULT MolfitsFileName = LocalPath + "files/my_molecules.molfit"
    MolfitsFileName = LocalPath + 'CH3OH_pure.molfit'

    # define min. freq. (in MHz)
    FreqMin = 215764.24

    # define max. freq. (in MHz)
    FreqMax = 225471.74

    # define freq. step (in MHz)
    FreqStep = 0.1

    # depending on parameter "Inter_Flag" define beam size (in arcsec)
    # (Inter_Flag = True) or size of telescope (in m) (Inter_Flag = False)
    TelescopeSize = 1.0 # arcseconds

    # define beam minor axis length (in arsec)
    BMIN = None

    # define beam major axis length (in arsec)
    BMAJ = None

    # define beam position angle (in degree)
    BPA = None

    # interferrometric data?
    Inter_Flag = True

    # define red shift
    Redshift = None

    # BACKGROUND: describe continuum with tBack and tslope only
    t_back_flag = True

    # BACKGROUND: define background temperature (in K)
    tBack = 0.0

    # BACKGROUND: define temperature slope (dimensionless)
    tslope = 0.0

    # BACKGROUND: define path and name of ASCII file describing continuum as function
    #             of frequency
    BackgroundFileName = ""

    # DUST: define hydrogen column density (in cm^(-2))
    N_H = 1.e22

    # DUST: define spectral index for dust (dimensionless)
    beta_dust = 0.0

    # DUST: define kappa at 1.3 mm (cm^(2) g^(-1))
    kappa_1300 = 0.0

    # DUST: define path and name of ASCII file describing dust opacity as
    #       function of frequency
    DustFileName = ""

    # FREE-FREE: define electronic temperature (in K)
    Te_ff = None

    # FREE-FREE: define emission measure (in pc cm^(-6))
    EM_ff = None

    # SYNCHROTRON: define kappa of energy spectrum of electrons (electrons m^(−3) GeV^(-1))
    kappa_sync = None

    # SYNCHROTRON: define magnetic field (in Gauss)
    B_sync = None

    # SYNCHROTRON: energy spectral index (dimensionless)
    p_sync = None

    # SYNCHROTRON: thickness of slab (in AU)
    l_sync = None

    # PHEN-CONT: define phenomenological function which is used to describe
    #            the continuum
    ContPhenFuncID = None

    # PHEN-CONT: define first parameter for phenomenological function
    ContPhenFuncParam1 = None

    # PHEN-CONT: define second parameter for phenomenological function
    ContPhenFuncParam2 = None

    # PHEN-CONT: define third parameter for phenomenological function
    ContPhenFuncParam3 = None

    # PHEN-CONT: define fourth parameter for phenomenological function
    ContPhenFuncParam4 = None

    # PHEN-CONT: define fifth parameter for phenomenological function
    ContPhenFuncParam5 = None

    # use iso ratio file?
    iso_flag = True

    # define path and name of iso ratio file
    #DEFAULT IsoTableFileName = LocalPath + "files/my_isonames.txt"
    IsoTableFileName = LocalPath + "my_isonames.txt"

    # define path and name of file describing Non-LTE parameters
    CollisionFileName = ""

    # define number of pixels in x-direction (used for sub-beam description)
    NumModelPixelXX = 100

    # define number of pixels in y-direction (used for sub-beam description)
    NumModelPixelYY = 100

    # take local-overlap into account or not
    LocalOverlapFlag = False

    # disable sub-beam description
    NoSubBeamFlag = True

    # define path and name of database file
    dbFilename = ""

    # define rest freq. (in MHz)
    RestFreq = 0.0

    # define v_lsr (in km/s)
    vLSR = 0.0
    ###########################################################################


    ## call myXCLASS function
    modeldata, log, TransEnergies, IntOpt, JobDir = task_myXCLASS.myXCLASS(
                                                FreqMin, FreqMax, FreqStep,
                                                TelescopeSize, BMIN, BMAJ,
                                                BPA, Inter_Flag, Redshift,
                                                t_back_flag, tBack, tslope,
                                                BackgroundFileName,
                                                N_H, beta_dust, kappa_1300,
                                                DustFileName, Te_ff, EM_ff,
                                                kappa_sync, B_sync, p_sync,
                                                l_sync, ContPhenFuncID,
                                                ContPhenFuncParam1,
                                                ContPhenFuncParam2,
                                                ContPhenFuncParam3,
                                                ContPhenFuncParam4,
                                                ContPhenFuncParam5,
                                                MolfitsFileName, iso_flag,
                                                IsoTableFileName,
                                                CollisionFileName,
                                                NumModelPixelXX,
                                                NumModelPixelYY,
                                                LocalOverlapFlag,
                                                NoSubBeamFlag,
                                                dbFilename,
                                                RestFreq, vLSR)


## finished!
##-----------------------------------------------------------------------------
##-----------------------------------------------------------------------------
##-----------------------------------------------------------------------------
