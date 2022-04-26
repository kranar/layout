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
    self.assertEqual(expansion, a * x + a * y + b * x + b * y)

  def test_distribute_multiplication_over_subtraction(self):
    expression = x * (y - z)
    expansion = expand(expression)
    self.assertEqual(expansion, x * y + -1 * x * z)

  def test_repeated_distribute_multiplication_over_subtraction(self):
    expression = (a - b) * (x - y)
    expansion = expand(expression)
    self.assertEqual(expansion, a * x + -1 * a * y + -1 * b * x + b * y)

  def test_distribute_division_over_addition(self):
    expression = (a + b) / (x + y)
    expansion = expand(expression)
    self.assertEqual(expansion, a / (x + y) + b / (x + y))

  def test_distribute_division_over_subtraction(self):
    expression = (a - b) / (x + y)
    expansion = expand(expression)
    self.assertEqual(expansion, a / (x + y) + -1 * b / (x + y))

  def test_distribute_addition(self):
    expression = (x * (y + z)) + (a * (b + c))
    expansion = expand(expression)
    self.assertEqual(expansion, x * y + x * z + a * b + a * c)

  def test_distribute_subtraction(self):
    expression = (x * (y + z)) - (a * (b + c))
    expansion = expand(expression)
    self.assertEqual(expansion, x * y + x * z + -1 * a * b + -1 * a * c)

  def test_normalizing_term_constants(self):
    expression = x * 5
    expansion = expand(expression)
    self.assertEqual(expansion, 5 * x)

  def test_propagating_term_constants(self):
    expression = x * y * 5
    expansion = expand(expression)
    self.assertEqual(expansion, 5 * x * y)

  def test_extracting_term_constants(self):
    expression = x * 5 * y
    expansion = expand(expression)
    self.assertEqual(expansion, 5 * x * y)

  def test_normalizing_constant_terms(self):
    expression = 5 + y
    expansion = expand(expression)
    self.assertEqual(expansion, y + 5)

  def test_propagating_constant_terms(self):
    expression = 5 + x + y
    expansion = expand(expression)
    self.assertEqual(expansion, x + y + 5)

  def test_extracting_constant_terms(self):
    expression = x + 5 + y
    expansion = expand(expression)
    self.assertEqual(expansion, x + y + 5)

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
