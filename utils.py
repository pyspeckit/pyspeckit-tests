from astropy import log

def run_tests(module, verbose=True):

    for entry in dir(module):
        if entry[:4] == 'test':
            testfunc = getattr(module, entry)
            if verbose:
                log.info("Running test {0}".format(entry))
            return testfunc()
