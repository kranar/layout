from library.expression import *


class VariableExpression(Expression):
  '''Implements an Expression representing a variable.'''

  def __init__(self, name):
    '''Constructs a VariableExpression with a given name.'''
    super().__init__()
    self._name = name

  @property
  def name(self):
    '''Returns the name of the variable represented.'''
    return self._name

  def visit(self, visitor):
    return visitor.visit_variable(self)

  def __str__(self):
    return self._name
