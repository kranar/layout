import copy
import enum
from library.constraint_system import ConstraintSystem

from library.equation import *
from library.solver import *
from library.variable_expression import *


class LayoutPolicy(enum.Enum):
  FIXED = 0
  EXPANDING = 1


class LayoutItem:
  def __init__(self, name, top=0, left=0, width=0,
      width_policy=LayoutPolicy.FIXED, height=0,
      height_policy=LayoutPolicy.FIXED):
    self.name = name
    self.top = top
    self.left = left
    self.width = width
    self.width_policy = width_policy
    self.height = height
    self.height_policy = height_policy

  @property
  def bottom(self):
    return self.top + self.height - 1

  @property
  def right(self):
    return self.left + self.width - 1

  def __eq__(self, other):
    return isinstance(other, LayoutItem) and \
      self.name == other.name and self.top == other.top and \
      self.left == other.left and self.width == other.width and \
      self.width_policy == other.width_policy and \
      self.height == other.height and self.height_policy == other.height_policy

  def __repr__(self):
    return f'LayoutItem({self.name}, {self.top}, {self.left}, {self.width}, '\
      f'{self.width_policy}, {self.height}, {self.height_policy})'


class LayoutExpression:
  def __init__(self, name):
    self._width = VariableExpression(f'{name}.width')
    self._width_growth = VariableExpression(f'{name}.width_growth')
    self._height = VariableExpression(f'{name}.height')
    self._height_growth = VariableExpression(f'{name}.height_growth')
    self._top = VariableExpression(f'{name}.top')
    self._left = VariableExpression(f'{name}.left')

  @property
  def width(self):
    return self._width

  @property
  def width_growth(self):
    return self._width_growth

  @property
  def height(self):
    return self._height

  @property
  def height_growth(self):
    return self._height_growth

  @property
  def top(self):
    return self._top

  @property
  def left(self):
    return self._left


def build_row_system(items, width, top):
  row_items = []
  bottom = top
  for item in items:
    if item.top <= top and item.bottom > top:
      row_items.append(item)
      bottom = max(bottom, item.bottom)
  row_items.sort(key=lambda key: key.left)
  width_expression = VariableExpression('width')
  equations = []
  growth_sum = LiteralExpression(-1)
  last_item = None
  width_sum = None
  for item in row_items:
    item_expression = LayoutExpression(item.name)
    if item.left == 0:
      equations.append(Equation(item_expression.left)) 
    if last_item is not None:
      equations.append(
        Equation(item_expression.left - (last_item.left + last_item.width)))
    if item.width_policy == LayoutPolicy.FIXED:
      equations.append(Equation(item_expression.width - item.width))
    elif item.width_policy == LayoutPolicy.EXPANDING:
      equations.append(Equation(item_expression.width -
        item.width - item_expression.width_growth * (width_expression - width)))
      growth_sum += item_expression.width_growth
    if width_sum is None:
      width_sum = item_expression.width
    else:
      width_sum += item_expression.width
    last_item = item_expression
  width_sum -= width_expression
  equations.append(Equation(width_sum))
  if growth_sum != LiteralExpression(-1):
    equations.append(Equation(growth_sum))
  return ConstraintSystem(equations), bottom + 1


def build_column_system(items, height, left):
  column_items = []
  right = left
  for item in items:
    if item.left <= left and item.right > left:
      column_items.append(item)
      right = max(right, item.right)
  column_items.sort(key=lambda key: key.top)
  height_expression = VariableExpression('height')
  equations = []
  growth_sum = LiteralExpression(-1)
  last_item = None
  height_sum = None
  for item in column_items:
    item_expression = LayoutExpression(item.name)
    if item.top == 0:
      equations.append(Equation(item_expression.top)) 
    if last_item is not None:
      equations.append(
        Equation(item_expression.top - (last_item.top + last_item.height)))
    if item.height_policy == LayoutPolicy.FIXED:
      equations.append(Equation(item_expression.height - item.height))
    elif item.height_policy == LayoutPolicy.EXPANDING:
      equations.append(Equation(item_expression.height - item.height -
        item_expression.height_growth * (height_expression - height)))
      growth_sum += item_expression.height_growth
    if height_sum is None:
      height_sum = item_expression.height
    else:
      height_sum += item_expression.height
    last_item = item_expression
  height_sum -= height_expression
  equations.append(Equation(height_sum))
  if growth_sum != LiteralExpression(-1):
    equations.append(Equation(growth_sum))
  return ConstraintSystem(equations), right + 1


def make_determined_growths(solution, direction):
  if not solution.is_underdetermined:
    return None
  underdetermined = solution.underdetermined
  while len(underdetermined) != 0:
    base = VariableExpression(underdetermined.pop())
    if base.name.endswith(f'{direction}_growth'):
      break
  constraints = []
  for variable in underdetermined:
    if variable.endswith(f'{direction}_growth'):
      constraints.append(Equation(base - VariableExpression(variable)))
  return ConstraintSystem(constraints)


class Layout:
  def __init__(self, items, constraints):
    self._items = copy.deepcopy(items)
    self._items.sort(key=lambda key: (key.top, key.left))
    self._constraints = constraints.copy()
    self._width = 0
    self._height = 0
    self._name_to_item = {}
    for item in self._items:
      self._name_to_item[item.name] = item
    for item in self._items:
      self._width = max(self._width, item.left + item.width)
      self._height = max(self._height, item.top + item.height)

  @property
  def items(self):
    return self._items.copy()

  @property
  def constraints(self):
    return self._constraints.copy()

  @property
  def width(self):
    return self._width

  @property
  def height(self):
    return self._height

  def resize(self, width, height):
    top = 0
    rows_system = ConstraintSystem([])
    while top != self._height:
      system, top = build_row_system(self._items, self._width, top)
      rows_system = rows_system.merge(system)
    left = 0
    columns_system = ConstraintSystem([])
    while left != self._width:
      system, left = build_column_system(self._items, self._height, left)
      columns_system = columns_system.merge(system)
    width_system = ConstraintSystem(
      [Equation(VariableExpression('width') - width)])
    height_system = ConstraintSystem(
      [Equation(VariableExpression('height') - height)])
    system = width_system.merge(height_system).merge(rows_system).merge(
      columns_system)
    solution = solve(system)
    update_solution = False
    if 'width' in solution.inconsistencies:
      system = system.remove(width_system)
      update_solution = True
    if 'height' in solution.inconsistencies:
      system = system.remove(height_system)
      update_solution = True
    for direction in ['width', 'height']:
      growths = make_determined_growths(solution, direction)
      if growths is not None:
        system = system.merge(growths)
        update_solution = True
    if update_solution:
      solution = solve(system)
    for case in solution.assignments:
      name_index = case.find('.')
      if name_index == -1:
        continue
      item = self._name_to_item[case[0:name_index]]
      property = case[name_index + 1:]
      if property == 'top':
        item.top = solution.assignments[case]
      elif property == 'left':
        item.left = solution.assignments[case]
      elif property == 'width':
        item.width = solution.assignments[case]
      elif property == 'height':
        item.height = solution.assignments[case]
    self._width = solution.assignments['width']
    self._height = solution.assignments['height']


def check_is_fit(components, width, height):
  area = 0
  for component in components:
    area += component.width * component.height
  return area == width * height
