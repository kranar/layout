import enum

from library import StatementVisitor


class SystemCategory:
  class Type(enum.IntEnum):
    CONSTANT = 1
    MONOMIAL = 2
    LINEAR = 3
    POLYNOMIAL = 4
    NON_LINEAR = 5

  def __init__(self, type, variables):
    self._type = type
    self._variables = variables.copy()

  @property
  def type(self):
    return self._type

  @property
  def variables(self):
    return self._variables.copy()

  def __str__(self):
    return f'({self._type.name} {self._variables})'


def categorize(expression):
  class Visitor(StatementVisitor):
    def visit_addition(self, expression):
      left_category = categorize(expression.left)
      right_category = categorize(expression.right)
      if right_category.type < left_category.type:
        tmp = left_category
        left_category = right_category
        right_category = tmp
      if left_category.type == SystemCategory.Type.CONSTANT:
        if right_category.type == SystemCategory.Type.MONOMIAL:
          return SystemCategory(
            SystemCategory.Type.LINEAR, right_category.variables)
      elif left_category.type == SystemCategory.Type.MONOMIAL:
        if right_category.type == SystemCategory.Type.MONOMIAL:
          if right_category.variables == left_category.variables:
            return SystemCategory(
              SystemCategory.Type.MONOMIAL, left_category.variables)
          else:
            return SystemCategory(SystemCategory.Type.LINEAR,
              left_category.variables | right_category.variables)
      return SystemCategory(right_category.type,
        left_category.variables | right_category.variables)

    def visit_subtraction(self, expression):
      return self.visit_addition(expression)

    def visit_multiplication(self, expression):
      left_category = categorize(expression.left)
      right_category = categorize(expression.right)
      if right_category.type < left_category.type:
        tmp = left_category
        left_category = right_category
        right_category = tmp
      if left_category.type == SystemCategory.Type.CONSTANT:
        return right_category
      elif left_category.type == SystemCategory.Type.MONOMIAL:
        if right_category.type == SystemCategory.Type.MONOMIAL:
          return SystemCategory(SystemCategory.Type.MONOMIAL,
            left_category.variables | right_category.variables)
      return SystemCategory(SystemCategory.Type.POLYNOMIAL,
        left_category.variables | right_category.variables)

    def visit_division(self, expression):
      raise RuntimeError('Not supported.')

    def visit_literal(self, expression):
      return SystemCategory(SystemCategory.Type.CONSTANT, set())

    def visit_variable(self, expression):
      return SystemCategory(SystemCategory.Type.MONOMIAL, {expression.name})
  return expression.visit(Visitor())
