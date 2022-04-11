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
      left = find_coefficients(expression.left)
      denominator = evaluate_constants(expression.right)
      has_variable = False
      for variable in left:
        if variable != '':
          term = left[variable]
          left = {variable: term / denominator}
          has_variable = True
          break
      if not has_variable:
        left = {'': left.get('', 0) / denominator}
      return left

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
  if expression is None:
    return LiteralExpression(0)
  return expression


def solve(system):
  '''
  Takes a ConstraintSystem and returns a dict whose keys are variable names and
  values are the solution to the given system. If no solution exists None is
  returned, if the solution is infinite then an empty dict is returned.
  '''
  coefficients = find_coefficients(expand(system.constraints[0].expression))
  if len(system.constraints) == 1:
    constant = 0
    variable = None
    for key in coefficients:
      if key == '':
        constant = coefficients[key]
      else:
        variable = key
        coefficient = coefficients[key]
    if variable is None:
      if constant == 0:
        return {'': 0}
      return None
    if coefficient == 0:
      return {}
    return {variable: -constant / coefficient}
  for key in coefficients:
    if key != '' and coefficients[key] != 0:
      target = key
      break
  coefficient = coefficients[target]
  del coefficients[target]
  if coefficient == 1:
    substitution = -1 * build_from_coefficients(coefficients)
  else:
    substitution = -1 * (build_from_coefficients(coefficients) / coefficient)
  substitutions = []
  for constraint in system.constraints[1:]:
    substitutions.append(substitute(target, substitution, constraint))
  solution = solve(ConstraintSystem(substitutions))
  if solution is None or solution == {}:
    return solution
  if '' in solution:
    del solution['']
  top_constraint = system.constraints[0]
  for term in solution:
    top_constraint = substitute(
      term, LiteralExpression(solution[term]), top_constraint)
  top_solution = solve(ConstraintSystem([top_constraint]))
  return solution | top_solution
