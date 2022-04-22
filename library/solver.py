import math

from library import ConstraintSystem
from library import LiteralExpression
from library import StatementVisitor
from library import StatementWalker
from library.division_expression import DivisionExpression
from library.expression import Expression
from library.manipulations import *


class UnderdeterminedType:
  def __init__(self):
    pass

  def __eq__(self, other):
    return isinstance(other, UnderdeterminedType)

UNDERDETERMINED = UnderdeterminedType()


def evaluate(expression):
  class Visitor(StatementVisitor):
    def visit_addition(self, expression):
      left = evaluate(expression.left)
      if left is UNDERDETERMINED:
        return UNDERDETERMINED
      right = evaluate(expression.right)
      if right is UNDERDETERMINED:
        return UNDERDETERMINED
      return left + right

    def visit_subtraction(self, expression):
      left = evaluate(expression.left)
      if left is UNDERDETERMINED:
        return UNDERDETERMINED
      right = evaluate(expression.right)
      if right is UNDERDETERMINED:
        return UNDERDETERMINED
      return left - right

    def visit_multiplication(self, expression):
      left = evaluate(expression.left)
      if left is UNDERDETERMINED:
        return UNDERDETERMINED
      right = evaluate(expression.right)
      if right is UNDERDETERMINED:
        return UNDERDETERMINED
      return left * right

    def visit_division(self, expression):
      numerator = evaluate(expression.left)
      if numerator is UNDERDETERMINED:
        return UNDERDETERMINED
      denominator = evaluate(expression.right)
      if denominator == 0 or denominator is UNDERDETERMINED:
        return UNDERDETERMINED
      return numerator / denominator

    def visit_literal(self, expression):
      return expression.value

    def visit_variable(self, expression):
      return expression
  return expression.visit(Visitor())


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


def isolate(variable, equation):
  class Walker(StatementWalker):
    def __init__(self):
      self._terms = []
      self._sign = 1

    def append(self, expression):
      if self._sign == 1:
        self._terms.append(expression)
      else:
        self._terms.append(-1 * expression)

    def visit_literal(self, expression):
      self.append(expression)

    def visit_division(self, expression):
      self.append(expression)

    def visit_multiplication(self, expression):
      self.append(expression)

    def visit_subtraction(self, expression):
      expression.left.visit(self)
      self._sign *= -1
      expression.right.visit(self)
      self._sign *= -1

    def visit_variable(self, expression):
      self.append(expression)
  walker = Walker()
  expand(equation.expression).visit(walker)
  terms = walker._terms
  numerator = None
  denominator = None
  for term in terms:
    variables = collect_variables(term)
    if variable not in variables:
      if numerator is None:
        numerator = -1 * term
      else:
        numerator += -1 * term
    else:
      if denominator is None:
        denominator = substitute(variable, LiteralExpression(1), term)
      else:
        denominator += substitute(variable, LiteralExpression(1), term)
  if numerator is None:
    numerator = LiteralExpression(0)
  if denominator is None:
    denominator = LiteralExpression(1)
  return numerator / denominator


def make_substituted_system(variable, system):
  substitution = isolate(
    variable, Equation(expand(system.constraints[0].expression)))
  print(variable, ': ', substitution)
  substitutions = []
  is_consistent = True
  for constraint in system.constraints[1:]:
    substituted_constraint = substitute(variable, substitution, constraint)
    if is_consistent and substituted_constraint != constraint:
      variables = collect_variables(substituted_constraint)
      if len(variables) == 0:
        solution = solve_equation(substituted_constraint)
        if solution.is_inconsistent:
          is_consistent = False
    substitutions.append(substituted_constraint)
  return ConstraintSystem(substitutions), is_consistent


def solve_equation(equation):
  '''
  Solves an Equation, if it consists of more than one variable then the Solution
  shall have no assignments and all variables shall be underdetermined.
  '''
  variables = collect_variables(equation.expression)
  if len(variables) == 0:
    if evaluate(equation.expression) == 0:
      return Solution()
    return Solution(inconsistencies={''})
  underdetermined = set()
  expressions = {}
  while len(variables) != 0:
    variable = variables.pop()
    expression = isolate(variable, equation)
    if issubclass(type(expression), DivisionExpression) and \
        evaluate(expression.right) == 0:
      underdetermined.add(variable)
    else:
      expressions[variable] = expression
  assignments = {}
  unresolved = set()
  for (variable, expression) in expressions.items():
    for u in underdetermined:
      expression = substitute(u, LiteralExpression(0), expression)
    evaluation = evaluate(expression)
    if issubclass(type(evaluation), Expression):
      unresolved.add(variable)
    else:
      assignments[variable] = evaluation
  return Solution(assignments, underdetermined=underdetermined | unresolved)


def solve(system):
  '''
  Takes a ConstraintSystem and returns a Solution that satisfies all of the
  system's equations.
  '''
  print('----------------')
  print(system)
  if len(system.constraints) == 1:
    return solve_equation(system.constraints[0])
  variables = collect_variables(system.constraints[0])
  if len(variables) == 0:
    return solve_equation(system.constraints[0]).merge(
      solve(ConstraintSystem(system.constraints[1:])))
  variable = variables.pop()
  substituted_system, is_substitution_consistent = make_substituted_system(
    variable, system)
  solution = solve(substituted_system)
  if not is_substitution_consistent:
    solution = solution.merge(Solution(inconsistencies={variable}))
  if solution.is_inconsistent:
    inconsistencies = set()
    for constraint in system.constraints:
      variables = collect_variables(constraint)
      if not solution.inconsistencies.isdisjoint(variables):
        inconsistencies |= variables
    if len(inconsistencies) != 0:
      return solution.merge(Solution(inconsistencies=inconsistencies))
  top_constraint = system.constraints[0]
  for term in solution.assignments:
    top_constraint = substitute(
      term, LiteralExpression(solution.assignments[term]), top_constraint)
  top_solution = solve(ConstraintSystem([top_constraint]))
  return solution.merge(top_solution)
