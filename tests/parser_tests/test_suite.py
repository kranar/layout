import unittest

from tests.parser_tests.parser_tester import ParserTester


def suite():
  suite = unittest.TestSuite()
  suite.addTest(unittest.makeSuite(ParserTester))
  return suite


if __name__ == '__main__':
  runner = unittest.TextTestRunner()
  runner.run(suite())
