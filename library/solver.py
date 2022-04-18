import math

from library import ConstraintSystem
from library import LiteralExpression
from library import StatementVisitor
from library import StatementWalker
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


class Solution:
  '''Stores the solution to a ConstraintSystem.'''

  def __init__(
      self, assignments = {}, underdetermined = set(), inconsistencies = set()):
    self._assignments = assignments.copy()
    self._underdetermined = underdetermined.copy()
    self._inconsistencies = inconsistencies.copy()

  @property
  def is_solved(self):
    return not self.is_underdetermined() and not self.is_inconsistent()

  @property
  def assignments(self):
    return self._assignments

  @property
  def underdetermined(self):
    return self._underdetermined

  @property
  def is_underdetermined(self):
    return len(self._underdetermined) != 0

  @property
  def inconsistencies(self):
    return self._inconsistencies

  @property
  def is_inconsistent(self):
    return len(self._inconsistencies) != 0

  def merge(self, solution):
    inconsistencies = self._inconsistencies | solution.inconsistencies
    underdetermined = self._underdetermined | solution.underdetermined
    assignments = {}
    for assignment in self._assignments:
      if assignment in inconsistencies:
        continue
      value = self._assignments[assignment]
      if assignment in solution.assignments:
        if not math.isclose(value, solution.assignments[assignment]):
          inconsistencies.add(assignment)
        else:
          assignments[assignment] = value
          if assignment in underdetermined:
            underdetermined.remove(assignment)
      else:
        assignments[assignment] = value
        if assignment in underdetermined:
          underdetermined.remove(assignment)
    for assignment in solution.assignments:
      if assignment in inconsistencies:
        continue
      if assignment not in self._assignments:
        assignments[assignment] = solution.assignments[assignment]
        if assignment in underdetermined:
          underdetermined.remove(assignment)
    if '' in inconsistencies and len(inconsistencies) != 1:
      inconsistencies.remove('')
    return Solution(assignments, underdetermined, inconsistencies)

  def __eq__(self, other):
    return isinstance(other, Solution) and \
      self._assignments == other._assignments and \
      self._inconsistencies == other._inconsistencies and \
      self._underdetermined == other._underdetermined


def collect_variables(statement):
  class Collector(StatementWalker):
    def __init__(self):
      self._variables = set()

    def visit_variable(self, expression):
      self._variables.add(expression.name)
  collector = Collector()
  statement.visit(collector)
  return collector._variables


def solve_equation(equation):
  '''
  Solves an Equation, if it consists of more than one variable then the Solution
  shall have no assignments and all variables shall be underdetermined.
  '''
  coefficients = find_coefficients(expand(equation.expression))
  non_trivial_variable_count = 0
  for key in coefficients:
    if key != '' and coefficients[key] != 0:
      non_trivial_variable_count += 1
  if non_trivial_variable_count == 0:
    if coefficients.get('', 0) == 0:
      return Solution()
    return Solution(inconsistencies={''})
  elif non_trivial_variable_count > 1:
    return Solution(underdetermined=collect_variables(equation.expression))
  constant = coefficients.get('', 0)
  for key in coefficients:
    if key != '':
      variable = key
      coefficient = coefficients[key]
      break
  if coefficient == 0:
    return Solution(underdetermined={variable})
  return Solution({variable: -constant / coefficient})


def solve(system):
  '''
  Takes a ConstraintSystem and returns a Solution that satisfies all of the
  system's equations.
  '''
  if len(system.constraints) == 1:
    return solve_equation(system.constraints[0])
  coefficients = find_coefficients(expand(system.constraints[0].expression))
  target = None
  for key in coefficients:
    if key != '' and coefficients[key] != 0:
      target = key
      break
  if target is None:
    solution = solve(ConstraintSystem(system.constraints[1:]))
    if coefficients.get('', 0) == 0:
      return solution
    else:
      return solution.merge(Solution(inconsistencies={''}))
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
  if solution.is_inconsistent:
    variables = collect_variables(system.constraints[0].expression)
    is_shared_inconsistency = False
    for variable in solution.inconsistencies:
      if variable in variables:
        is_shared_inconsistency = True
        break
    inconsistencies = set()
    if is_shared_inconsistency:
      inconsistencies = variables
    elif len(solution.inconsistencies) != 0:
      inconsistencies = {target}
    if len(inconsistencies) != 0:
      return solution.merge(Solution(inconsistencies=inconsistencies))
  top_constraint = system.constraints[0]
  for term in solution.assignments:
    top_constraint = substitute(
      term, LiteralExpression(solution.assignments[term]), top_constraint)
  top_solution = solve(ConstraintSystem([top_constraint]))
  return solution.merge(top_solution)
