from library import ConstraintSystem
from library import LiteralExpression
from library import StatementVisitor
from library import VariableExpression
from library.manipulations import *


def evaluate_constants(expression):
  class Visitor(StatementVisitor):
    def visit_addition(self, expression):
      return evaluate_constants(expression.left) + \
        evaluate_constants(expression.right)

    def visit_subtraction(self, expression):
      return evaluate_constants(expression.left) - \
        evaluate_constants(expression.right)

    def visit_multiplication(self, expression):
      return evaluate_constants(expression.left) * \
        evaluate_constants(expression.right)

    def visit_division(self, expression):
      return evaluate_constants(expression.left) / \
        evaluate_constants(expression.right)

    def visit_literal(self, expression):
      return expression.value
  return expression.visit(Visitor())


def find_coefficients(expression):
  class Visitor(StatementVisitor):
    def visit_expression(self, expression):
      return {}

    def visit_addition(self, expression):
      left = find_coefficients(expression.left)
      right = find_coefficients(expression.right)
      return {key: left.get(key, 0) + right.get(key, 0) for
        key in set(left) | set(right)}

    def visit_subtraction(self, expression):
      left = find_coefficients(expression.left)
      right = find_coefficients(expression.right)
      return {key: left.get(key, 0) - right.get(key, 0) for
        key in set(left) | set(right)}

    def visit_multiplication(self, expression):
      left = find_coefficients(expression.left)
      right = find_coefficients(expression.right)
      coefficients = {key: left.get(key, 1) * right.get(key, 1) for
        key in set(left) | set(right)}
      constant = coefficients.get('', 1)
      for variable in coefficients:
        if variable != '':
          term = coefficients[variable]
          coefficients = {variable: term * constant}
          break
      return coefficients

    def visit_division(self, expression):
      coefficient = evaluate_constants(expression.right)
      if type(expression.left) is VariableExpression:
        return {expression.left.name: 1.0 / coefficient}
      return {'': evaluate_constants(expression.left) / coefficient}

    def visit_variable(self, expression):
      return {expression.name: 1}

    def visit_literal(self, expression):
      return {'': expression.value}
  return expression.visit(Visitor())


def build_from_coefficients(coefficients):
  expression = None
  for variable in coefficients:
    if variable == '':
      extension = LiteralExpression(coefficients[variable])
    else:
      coefficient = coefficients[variable]
      if coefficient == 1:
        extension = VariableExpression(variable)
      else:
        extension = coefficients[variable] * VariableExpression(variable)
    if expression is None:
      expression = extension
    else:
      expression += extension
  return expression


def solve(system):
  if len(system.constraints) == 1:
    coefficients = find_coefficients(expand(system.constraints[0].expression))
    constant = 0
    for key in coefficients:
      if key == '':
        constant = coefficients[key]
      else:
        variable = key
        coefficient = coefficients[key]
    return {variable: -constant / coefficient}
  coefficients = find_coefficients(expand(system.constraints[0].expression))
  for key in coefficients:
    if key != '':
      target = key
      break
  coefficient = coefficients[target]
  del coefficients[target]
  substitution = -1 * (build_from_coefficients(coefficients) / coefficient)
  substitutions = []
  for constraint in system.constraints[1:]:
    substitutions.append(substitute(target, substitution, constraint))
  solution = solve(ConstraintSystem(substitutions))
  print(solution)
  return {}
