from library.expression import *


class MultiplicationExpression(Expression):
  '''Implements an Expression for the multiplication of two sub-expressions.'''

  def __init__(self, left, right):
    '''
    Constructs a MultiplicationExpression that multiplies a left sub-expression
    with a right sub-expression.
    '''
    super().__init__()
    self._left = left
    self._right = right

  @property
  def left(self):
    '''Returns the left sub-expression to multiply.'''
    return self._left

  @property
  def right(self):
    '''Returns the right sub-expression to multiply.'''
    return self._right

  def visit(self, visitor):
    return visitor.visit_multiplication(self)

  def __str__(self):
    return f'({self.left} * {self.right})'
