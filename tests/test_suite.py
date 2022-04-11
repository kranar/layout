import unittest

from library_tests.test_suite import suite as LibrarySuite


def suite():
  suite = unittest.TestSuite()
  suite.addTests(LibrarySuite())
  return suite


if __name__ == '__main__':
  runner = unittest.TextTestRunner()
  runner.run(suite())
