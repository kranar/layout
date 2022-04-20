from library.statement import *


class ConstraintSystem(Statement):
  '''Composes multiple Equations together into a system.'''

  def __init__(self, constraints):
    '''Constructs a ConstraintSystem from a list of constraints.'''
    self._constraints = constraints.copy()

  @property
  def constraints(self):
    '''Returns the list of constraints.'''
    return self._constraints.copy()

  def merge(self, system):
    '''
    Returns a new ConstraintSystem whose constraints are those of another
    system appended to the constraints of this system.
    '''
    constraints = self._constraints.copy()
    constraints.extend(system._constraints)
    return ConstraintSystem(constraints)

  def remove(self, system):
    '''
    Returns a new ConstraintSystem whose constraints are those of this system
    with those of another system removed from it.
    '''
    constraints = self._constraints.copy()
    for constraint in system.constraints:
      constraints.remove(constraint)
    return ConstraintSystem(constraints)

  def visit(self, visitor):
    return visitor.visit_constraint_system(self)

  def __eq__(self, right):
    return isinstance(right, ConstraintSystem) and \
      self._constraints == right._constraints

  def __str__(self):
    return '\n'.join([str(s) for s in self._constraints])
