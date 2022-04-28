import sys
import unittest

from tests.library_tests.layout_tester import LayoutTester
from tests.library_tests.manipulations_tester import ManipulationsTester
from tests.library_tests.solver_tester import SolverTester


def make_suite(type):
  if len(sys.argv) < 2:
    pattern = None
  else:
    pattern = [sys.argv[1]]
  loader = unittest.TestLoader()
  loader.sortTestMethodsUsing = unittest.util.three_way_cmp
  loader.testMethodPrefix = 'test'
  loader.testNamePatterns = pattern
  loader.suiteClass = unittest.suite.TestSuite
  return loader.loadTestsFromTestCase(type)

def suite():
  suite = unittest.TestSuite()
  suite.addTest(make_suite(ManipulationsTester))
  suite.addTest(make_suite(SolverTester))
  suite.addTest(make_suite(LayoutTester))
  return suite


if __name__ == '__main__':
  runner = unittest.TextTestRunner()
  runner.run(suite())
