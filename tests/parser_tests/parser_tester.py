import unittest

from library import *


class ParserTester(unittest.TestCase):
  def test_parse(self):
    add = AdditionExpression(5, 6)
    self.assertEqual(add.left, 2)


if __name__ == '__main__':
  unittest.main()
