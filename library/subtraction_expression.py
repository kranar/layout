from library.expression import *


class SubtractionExpression(Expression):
  '''Implements an Expression for the subtraction of two sub-expressions.'''

  def __init__(self, left, right):
    '''
    Constructs a SubtractionExpression that subtracts a left sub-expression by a
    right sub-expression.
    '''
    super().__init__()
    self._left = left
    self._right = right

  @property
  def left(self):
    '''Returns the left sub-expression to subtract.'''
    return self._left

  @property
  def right(self):
    '''Returns the right sub-expression to subtract.'''
    return self._right

  def visit(self, visitor):
    return visitor.visit_subtraction(self)

  def __eq__(self, right):
    return isinstance(right, SubtractionExpression) and \
      self._left == right._left and self._right == right._right

  def __str__(self):
    return f'({self.left} - {self.right})'
