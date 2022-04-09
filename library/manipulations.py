from library import AdditionExpression
from library import Equation
from library import StatementVisitor
from library import SubtractionExpression


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
  return expression.visit(Visitor())


def substitute(variable, substitution, expression):
  '''
  Replaces all VariableExpressions with a substitution in a given expression.
  '''
  class Visitor(StatementVisitor):
    def __init__(self, variable, substitution):
      self._variable = variable
      self._substitution = substitution

    def visit_equation(self, equation):
      return Equation(
        substitute(variable, self._substitution, equation.expression))

    def visit_expression(self, expression):
      return expression

    def visit_addition(self, expression):
      return substitute(variable, self._substitution, expression.left) + \
        substitute(variable, self._substitution, expression.right)

    def visit_subtraction(self, expression):
      return substitute(variable, self._substitution, expression.left) - \
        substitute(variable, self._substitution, expression.right)

    def visit_multiplication(self, expression):
      return substitute(variable, self._substitution, expression.left) * \
        substitute(variable, self._substitution, expression.right)

    def visit_division(self, expression):
      return substitute(variable, self._substitution, expression.left) / \
        substitute(variable, self._substitution, expression.right)

    def visit_variable(self, expression):
      if expression.name == self._variable:
        return self._substitution
      return self.visit_expression(expression)
  return expression.visit(Visitor(variable, substitution))
