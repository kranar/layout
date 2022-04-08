from library.statement import *


class ConstraintSystem(Statement):
  '''Composes multiple constraints together into a system.'''

  def __init__(self, constraints):
    '''Constructs a ConstraintSystem from a list of constraints.'''
    self._constraints = constraints.copy()

  @property
  def constraints(self):
    return self._constraints.copy()

  def visit(self, visitor):
    return visitor.visit_constraint_system(self)

  def __eq__(self, right):
    return self._constraints == right._constraints

  def __str__(self):
    return '\n'.join([str(s) for s in self._constraints])
