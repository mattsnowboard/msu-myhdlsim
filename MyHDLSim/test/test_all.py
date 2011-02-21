""" Run all unit tests. """


import test_And, test_Or, test_Not, test_MUX, test_Decoder, test_tff, test_dff,\
       test_Counter, test_Register

modules = (test_And, test_Or, test_Not, test_MUX, test_Decoder, test_tff, 
           test_dff, test_Counter, test_Register
          )

import unittest

tl = unittest.defaultTestLoader
def suite():
    alltests = unittest.TestSuite()
    for m in modules:
        alltests.addTest(tl.loadTestsFromModule(m))
    return alltests

def main():
    unittest.main(defaultTest='suite',
                  testRunner=unittest.TextTestRunner(verbosity=2))
    

if __name__ == '__main__':
    main()
