from library.statement import *


class Expression(Statement):
  '''
  Base class representing an expression. An expression is a Statement that can
  be evaluated.
  '''

  def __init__(self):
    super().__init__()

  def __add__(self, right):
    if isinstance(right, Expression):
      return AdditionExpression(self, right)
    return self + LiteralExpression(right)

  def __radd__(self, left):
    if isinstance(left, Expression):
      return AdditionExpression(left, self)
    return LiteralExpression(left) + self

  def __sub__(self, right):
    if isinstance(right, Expression):
      return SubtractionExpression(self, right)
    return self - LiteralExpression(right)

  def __rsub__(self, left):
    if isinstance(left, Expression):
      return SubtractionExpression(left, self)
    return LiteralExpression(left) - self

  def __mul__(self, right):
    if isinstance(right, Expression):
      return MultiplicationExpression(self, right)
    return self * LiteralExpression(right)

  def __rmul__(self, left):
    if isinstance(left, Expression):
      return MultiplicationExpression(self, left)
    return LiteralExpression(left) * self

  def __truediv__(self, right):
    if isinstance(right, Expression):
      return DivisionExpression(self, right)
    return self / LiteralExpression(right)

  def __rtruediv__(self, left):
    if isinstance(left, Expression):
      return DivisionExpression(left, self)
    return LiteralExpression(left) / self

from library.addition_expression import *
from library.division_expression import *
from library.literal_expression import *
from library.multiplication_expression import *
from library.subtraction_expression import *
