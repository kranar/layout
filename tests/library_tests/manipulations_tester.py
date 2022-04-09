import unittest

from library import *


a = VariableExpression('a')
b = VariableExpression('b')
c = VariableExpression('c')
x = VariableExpression('x')
y = VariableExpression('y')
z = VariableExpression('z')


class ManipulationsTester(unittest.TestCase):
  def test_expanding_literal(self):
    expression = LiteralExpression(5)
    expansion = expand(expression)
    self.assertEqual(expansion, expression)

  def test_expanding_variable(self):
    expansion = expand(x)
    self.assertEqual(expansion, x)

  def test_distribute_multiplication_addition(self):
    expression = x * (y + z)
    expansion = expand(expression)
    self.assertEqual(expansion, x * y + x * z)

  def test_distribute_multiplication_subtraction(self):
    expression = x * (y - z)
    expansion = expand(expression)
    self.assertEqual(expansion, x * y - x * z)

  def test_distribute_recursive_multiplication_addition(self):
    expression = (a + b) * (x + y)
    expansion = expand(expression)
    self.assertEqual(expansion, (x * a + x * b) + (y * a + y * b))

  def test_distribute_division_addition(self):
    expression = (a + b) / (x + y)
    expansion = expand(expression)
    self.assertEqual(expansion, a / (x + y) + b / (x + y))

  def test_distribute_division_subtraction(self):
    expression = (a - b) / (x + y)
    expansion = expand(expression)
    self.assertEqual(expansion, a / (x + y) - b / (x + y))

  def test_distribute_addition(self):
    expression = (x * (y + z)) + (a * (b + c))
    expansion = expand(expression)
    self.assertEqual(expansion, (x * y + x * z) + (a * b + a * c))

  def test_distribute_subtraction(self):
    expression = (x * (y + z)) - (a * (b + c))
    expansion = expand(expression)
    self.assertEqual(expansion, (x * y + x * z) - (a * b + a * c))


if __name__ == '__main__':
  unittest.main()
