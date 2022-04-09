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

  def test_distribute_multiplication_over_addition(self):
    expression = x * (y + z)
    expansion = expand(expression)
    self.assertEqual(expansion, x * y + x * z)

  def test_repeated_distribute_multiplication_over_addition(self):
    expression = (a + b) * (x + y)
    expansion = expand(expression)
    self.assertEqual(expansion, (x * a + x * b) + (y * a + y * b))

  def test_distribute_multiplication_over_subtraction(self):
    expression = x * (y - z)
    expansion = expand(expression)
    self.assertEqual(expansion, x * y - x * z)

  def test_repeated_distribute_multiplication_over_subtraction(self):
    expression = (a - b) * (x - y)
    expansion = expand(expression)
    self.assertEqual(expansion, (x * a - x * b) - (y * a - y * b))

  def test_distribute_division_over_addition(self):
    expression = (a + b) / (x + y)
    expansion = expand(expression)
    self.assertEqual(expansion, a / (x + y) + b / (x + y))

  def test_distribute_division_over_subtraction(self):
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

  def test_literal_substitution(self):
    expression = LiteralExpression(5)
    substitution = substitute('x', LiteralExpression('100'), expression)
    self.assertEqual(substitution, expression)

  def test_unmatching_variable_substitution(self):
    expression = VariableExpression('foo')
    substitution = substitute('x', LiteralExpression('100'), expression)
    self.assertEqual(substitution, expression)

  def test_matching_variable_substitution(self):
    expression = VariableExpression('x')
    substitution = substitute('x', LiteralExpression('100'), expression)
    self.assertEqual(substitution, LiteralExpression('100'))

  def test_binary_substitution(self):
    replacement = LiteralExpression('100')
    for operation in [AdditionExpression, SubtractionExpression,
        MultiplicationExpression, DivisionExpression]:
      expression = operation(x, y)
      unmatched_substitution = substitute('foo', replacement, expression)
      self.assertEqual(unmatched_substitution, operation(x, y))
      left_substitution = substitute(x.name, replacement, expression)
      self.assertEqual(left_substitution, operation(replacement, y))
      right_substitution = substitute(y.name, replacement, expression)
      self.assertEqual(right_substitution, operation(x, replacement))


if __name__ == '__main__':
  unittest.main()
