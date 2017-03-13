def run_tests(module):

    for entry in dir(module):
        if entry[:4] == 'test':
            testfunc = getattr(module, entry)
            return testfunc()
