from library.expression import *


class AdditionExpression(Expression):
  '''Implements an Expression for the addition of two sub-expressions.'''

  def __init__(self, left, right):
    '''
    Constructs an AdditionExpression that adds a left sub-expression with a
    right sub-expression.
    '''
    super().__init__()
    self._left = left
    self._right = right

  @property
  def left(self):
    '''Returns the left sub-expression to add.'''
    return self._left

  @property
  def right(self):
    '''Returns the right sub-expression to add.'''
    return self._right

  def visit(self, visitor):
    return visitor.visit_addition(self)

  def __eq__(self, right):
    return self._left == right._left and self._right == right._right

  def __str__(self):
    return f'({self.left} + {self.right})'
