from Testing import ZopeTestCase as ztc
from ftw.globalstatusmessage.tests.base import GSMTestCase
import doctest
import unittest


MODULENAMES = ()


TESTFILES = (
    'globalstatusmessage.txt',
    )


OPTIONFLAGS = (doctest.NORMALIZE_WHITESPACE |
               doctest.ELLIPSIS |
               doctest.REPORT_NDIFF)


# def test_suite():
# 
#     suite = unittest.TestSuite()
# 
#     for testfile in TESTFILES:
#         fdfs = ZopeTestCase.FunctionalDocFileSuite(
#             'globalstatusmessage.txt',
#             optionflags=OPTIONFLAGS,
#             test_class=ptc.FunctionalTestCase,)
#         fdfs.layer = layer.gsm_integration_layer
#         suite.addTest(fdfs)
#         
#     return suite
# 
# if __name__ == '__main__':
#     unittest.main(defaultTest='test_suite')
def test_suite():
    return unittest.TestSuite([
        # doctests in file bar.txt
        ztc.ZopeDocFileSuite(
            'globalstatusmessage.txt', package='ftw.globalstatusmessage.tests',
            test_class=GSMTestCase, optionflags=OPTIONFLAGS),

        # docstring tests for module ftw.foo.bar
             ztc.ZopeDocTestSuite(
                         'ftw.globalstatusmessage.config',
                          test_class=GSMTestCase, optionflags=OPTIONFLAGS),
                 ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')