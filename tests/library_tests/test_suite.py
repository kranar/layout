import unittest

from tests.library_tests.manipulations_tester import ManipulationsTester
from tests.library_tests.parser_tester import ParserTester


def suite():
  suite = unittest.TestSuite()
  suite.addTest(unittest.makeSuite(ManipulationsTester))
  suite.addTest(unittest.makeSuite(ParserTester))
  return suite


if __name__ == '__main__':
  runner = unittest.TextTestRunner()
  runner.run(suite())
