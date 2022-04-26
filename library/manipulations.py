from library import AdditionExpression
from library import DivisionExpression
from library import Equation
from library import StatementVisitor
from library import SubtractionExpression
from library.literal_expression import LiteralExpression
from library.multiplication_expression import MultiplicationExpression


def normalize_division(expression):
  '''
  Transforms an expression of the form (a * (b / c)) into ((a * b) / c) and
  an expression of the form ((a / b) * c) into ((a * c) / b), otherwise returns
  the expression unchanged.
  '''
  class Visitor(StatementVisitor):
    def visit_expression(self, expression):
      return expression

    def visit_multiplication(self, expression):
      if issubclass(type(expression.left), DivisionExpression):
        return normalize_division(
          (expression.left.left * expression.right) / expression.left.right)
      elif issubclass(type(expression.right), DivisionExpression):
        return normalize_division(
          (expression.left * expression.right.left) / expression.right.right)
      return expression
  return expression.visit(Visitor())


def expand(expression):
  '''Expands an expression by distributing all multiplications and divisions.'''
  class Visitor(StatementVisitor):
    def visit_expression(self, expression):
      return expression

    def visit_addition(self, expression):
      left = expand(expression.left)
      right = expand(expression.right)
      if issubclass(type(left), AdditionExpression):
        return expand(left.left + (left.right + right))
      elif issubclass(type(left), LiteralExpression):
        if issubclass(type(right), LiteralExpression):
          return LiteralExpression(left.value + right.value)
        return expand(right + left)
      elif right == LiteralExpression(0):
        return left
      elif left == expression.left and right == expression.right:
        return expression
      return left + right

    def visit_subtraction(self, expression):
      left = expand(expression.left)
      right = expand(expression.right)
      return expand(left + -1 * right)

    def visit_multiplication(self, expression):
      left = expand(expression.left)
      right = expand(expression.right)
      if issubclass(type(left), MultiplicationExpression):
        return expand(left.left * (left.right * right))
      elif issubclass(type(right), LiteralExpression):
        if issubclass(type(left), LiteralExpression):
          return LiteralExpression(left.value * right.value)
        return expand(right * left)
      elif left == LiteralExpression(1):
        return right
      elif left == LiteralExpression(0):
        return LiteralExpression(0)
      elif issubclass(type(left), LiteralExpression) and \
          issubclass(type(right), MultiplicationExpression) and \
          issubclass(type(right.left), LiteralExpression):
        return expand(
          LiteralExpression(left.value * right.left.value) * right.right)
      elif issubclass(type(right), AdditionExpression):
        return expand(left * right.left + left * right.right)
      elif left == expression.left and right == expression.right:
        return expression
      return left * right

    def visit_division(self, expression):
      left = expand(expression.left)
      right = expand(expression.right)
      if issubclass(type(left), LiteralExpression) and \
          issubclass(type(right), LiteralExpression) and \
            right != LiteralExpression(0):
        return LiteralExpression(left.value / right.value)
      elif left == LiteralExpression(0):
        return LiteralExpression(0)
      elif right == LiteralExpression(1):
        return left
      elif right == LiteralExpression(-1):
        return expand(-1 * left)
      distributive_operators = [AdditionExpression, SubtractionExpression]
      operation = type(left)
      if operation in distributive_operators:
        return expand(operation(left.left / right, left.right / right))
      return left / right
  return normalize_division(expression.visit(Visitor()))


def substitute(variable, substitution, expression):
  '''
  Replaces all VariableExpressions with a substitution in a given expression.
  '''
  class Visitor(StatementVisitor):
    def __init__(self, variable, substitution):
      self._variable = variable
      self._substitution = substitution

    def visit_equation(self, equation):
      expression_substitution = substitute(
        variable, self._substitution, equation.expression)
      if substitution == equation.expression:
        return equation
      return Equation(expression_substitution)

    def visit_expression(self, expression):
      return expression

    def visit_addition(self, expression):
      left_substitution = substitute(
        variable, self._substitution, expression.left)
      right_substitution = substitute(
        variable, self._substitution, expression.right)
      if left_substitution == expression.left and \
          right_substitution == expression.right:
        return expression
      return left_substitution + right_substitution

    def visit_subtraction(self, expression):
      left_substitution = substitute(
        variable, self._substitution, expression.left)
      right_substitution = substitute(
        variable, self._substitution, expression.right)
      if left_substitution == expression.left and \
          right_substitution == expression.right:
        return expression
      return left_substitution - right_substitution

    def visit_multiplication(self, expression):
      left_substitution = substitute(
        variable, self._substitution, expression.left)
      right_substitution = substitute(
        variable, self._substitution, expression.right)
      if left_substitution == expression.left and \
          right_substitution == expression.right:
        return expression
      return left_substitution * right_substitution

    def visit_division(self, expression):
      left_substitution = substitute(
        variable, self._substitution, expression.left)
      right_substitution = substitute(
        variable, self._substitution, expression.right)
      if left_substitution == expression.left and \
          right_substitution == expression.right:
        return expression
      return left_substitution / right_substitution

    def visit_variable(self, expression):
      if expression.name == self._variable:
        return self._substitution
      return expression
  return expression.visit(Visitor(variable, substitution))
