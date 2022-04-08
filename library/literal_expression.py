from library.expression import *


class LiteralExpression(Expression):
  '''Implements an Expression representing a literal value.'''

  def __init__(self, value):
    '''Constructs a LiteralValue representing a Python object.'''
    super().__init__()
    self._value = value

  @property
  def type(self):
    '''Returns the type of value represented.'''
    return type(self._value)

  @property
  def value(self):
    '''Returns the value represented.'''
    return self._value

  def visit(self, visitor):
    return visitor.visit_literal(self)

  def __eq__(self, right):
    return self._value == right._value

  def __str__(self):
    return str(self._value)
