from library.statement import *


class Equation(Statement):
  '''
  Implements a statement representing an expression that must be equal zero.
  '''

  def __init__(self, expression):
    '''
    Constructs an Equation specifying that an expression must be equal to zero.
    '''
    self._expression = expression

  @property
  def expression(self):
    return self._expression

  def visit(self, visitor):
    return visitor.visit_equation(self)

  def __eq__(self, right):
    return self._expression == right._expression

  def __str__(self):
    return f'{self._expression} = 0'
