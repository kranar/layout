from library import AdditionExpression
from library import DivisionExpression
from library import Equation
from library import StatementVisitor
from library import SubtractionExpression


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
      return expand(expression.left) + expand(expression.right)

    def visit_subtraction(self, expression):
      return expand(expression.left) - expand(expression.right)

    def visit_multiplication(self, expression):
      distributive_operators = [AdditionExpression, SubtractionExpression]
      operation = type(expression.right)
      if operation in distributive_operators:
        return expand(operation((expression.left * expression.right.left),
          (expression.left * expression.right.right)))
      elif type(expression.left) in distributive_operators:
        return expand(expression.right * expression.left)
      else:
        result = expand(expression.left) * expand(expression.right)
        if type(result.left) in distributive_operators or \
            type(result.right) in distributive_operators:
          return expand(result)
        return result

    def visit_division(self, expression):
      distributive_operators = [AdditionExpression, SubtractionExpression]
      operation = type(expression.left)
      if operation in distributive_operators:
        return expand(operation((expression.left.left / expression.right),
          (expression.left.right / expression.right)))
      else:
        result = expand(expression.left) / expand(expression.right)
        if type(result.left) in distributive_operators:
          return expand(result)
        return result
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
