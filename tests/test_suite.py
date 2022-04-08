import unittest

from parser_tests.test_suite import suite as ParserSuite


def suite():
  suite = unittest.TestSuite()
  suite.addTests(ParserSuite())
  return suite


if __name__ == '__main__':
  runner = unittest.TextTestRunner(buffer=True)
  runner.run(suite())
