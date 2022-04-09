from library.expression import *


class DivisionExpression(Expression):
  '''Implements an Expression for the division of two sub-expressions.'''

  def __init__(self, left, right):
    '''
    Constructs a DivisionExpression that divides a left sub-expression by a
    right sub-expression.
    '''
    super().__init__()
    self._left = left
    self._right = right

  @property
  def left(self):
    '''Returns the left sub-expression to divide.'''
    return self._left

  @property
  def right(self):
    '''Returns the right sub-expression to divide.'''
    return self._right

  def visit(self, visitor):
    return visitor.visit_division(self)

  def __eq__(self, right):
    return isinstance(right, DivisionExpression) and \
      self._left == right._left and self._right == right._right

  def __str__(self):
    return f'({self.left} / {self.right})'
