import copy
import enum
import math

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

class Direction(enum.Enum):
  HORIZONTAL = 1
  VERTICAL = 2


def build_span_system(items, width, height, direction):
  position = 0
  fixed_equations = []
  expanding_equations = []
  growth_equations = []
  if direction == Direction.HORIZONTAL:
    size = width
    size_expression = VariableExpression('width')
    end = height
    get_item_span_start = lambda item: item.top
    get_item_span_end = lambda item: item.bottom
    get_item_start = lambda item: item.left
    get_item_size = lambda item: item.width
    get_item_policy = lambda item: item.width_policy
    get_item_growth = lambda item: item.width_growth
  else:
    size = height
    size_expression = VariableExpression('height')
    end = width
    get_item_span_start = lambda item: item.left
    get_item_span_end = lambda item: item.right
    get_item_start = lambda item: item.top
    get_item_size = lambda item: item.height
    get_item_policy = lambda item: item.height_policy
    get_item_growth = lambda item: item.height_growth
  while position != end:
    span_items = []
    span_end = math.inf
    for item in items:
      if get_item_span_start(item) <= position and \
          get_item_span_end(item) > position:
        span_items.append(item)
        span_end = min(span_end, get_item_span_end(item))
    span_items.sort(key=get_item_start)
    growth_sum = LiteralExpression(-1)
    last_item = None
    total_size_expression = None
    for item in span_items:
      item_expression = LayoutExpression(item.name)
      if get_item_start(item) == 0:
        fixed_equations.append(Equation(get_item_start(item_expression)))
      if last_item is not None:
        fixed_equations.append(Equation(get_item_start(item_expression) -
          (get_item_start(last_item) + get_item_size(last_item))))
      if get_item_policy(item) == LayoutPolicy.FIXED:
        fixed_equations.append(
          Equation(get_item_size(item_expression) - get_item_size(item)))
      elif item.width_policy == LayoutPolicy.EXPANDING:
        expanding_equations.append(
          Equation(get_item_size(item_expression) - get_item_size(item) -
            get_item_growth(item_expression) * (size_expression - size)))
        growth_sum += get_item_growth(item_expression)
      if total_size_expression is None:
        total_size_expression = get_item_size(item_expression)
      else:
        total_size_expression += get_item_size(item_expression)
      last_item = item_expression
    total_size_expression -= size_expression
    fixed_equations.append(Equation(total_size_expression))
    if growth_sum != LiteralExpression(-1):
      growth_equations.append(Equation(growth_sum))
    position = span_end + 1
  growth_solution = solve(ConstraintSystem(growth_equations))
  growth_resolution = []
  underdetermined_growths = growth_solution.underdetermined
  if len(underdetermined_growths) != 0:
    base = VariableExpression(underdetermined_growths.pop())
    for underdetermined in underdetermined_growths:
      growth_resolution.append(
        Equation(base - VariableExpression(underdetermined)))
  return ConstraintSystem(fixed_equations + growth_equations +
    growth_resolution + expanding_equations)


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
    rows_system = build_span_system(
      self._items, self._width, self._height, Direction.HORIZONTAL)
    columns_system = build_span_system(
      self._items, self._width, self._height, Direction.VERTICAL)
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
