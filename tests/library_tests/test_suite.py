import unittest

from tests.library_tests.layout_tester import LayoutTester
from tests.library_tests.manipulations_tester import ManipulationsTester
from tests.library_tests.solver_tester import SolverTester


def suite():
  suite = unittest.TestSuite()
  suite.addTest(unittest.makeSuite(ManipulationsTester))
  suite.addTest(unittest.makeSuite(SolverTester))
  suite.addTest(unittest.makeSuite(LayoutTester))
  return suite


if __name__ == '__main__':
  runner = unittest.TextTestRunner()
  runner.run(suite())
