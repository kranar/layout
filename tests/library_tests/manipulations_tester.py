import unittest

from library import *


class ManipulationsTester(unittest.TestCase):
  def test_expanding_literal(self):
    expression = LiteralExpression(5)
    expansion = expand(expression)
    self.assertEqual(expansion, expression)

  def test_distribute_multiplication_addition(self):
    x = VariableExpression('x')
    y = VariableExpression('y')
    z = VariableExpression('z')
    expression = x * (y + z)
    expansion = expand(expression)
    self.assertEqual(expansion, x * y + x * z)


if __name__ == '__main__':
  unittest.main()
