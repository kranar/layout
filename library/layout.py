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
    self._height = VariableExpression(f'{name}.height')
    self._top = VariableExpression(f'{name}.top')
    self._left = VariableExpression(f'{name}.left')

  @property
  def width(self):
    return self._width

  @property
  def height(self):
    return self._height

  @property
  def top(self):
    return self._top

  @property
  def left(self):
    return self._left


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
    constraints = []
    last_item = None
    width_sum = None
    height_sum = None
    for item in self._items:
      item_expression = LayoutExpression(item.name)
      if item.left == 0:
        constraints.append(Equation(item_expression.left)) 
      if last_item is not None:
        constraints.append(
          Equation(item_expression.left - (last_item.left + last_item.width)))
      if item.top == 0:
        constraints.append(Equation(item_expression.top))
      if item.width_policy == LayoutPolicy.FIXED:
        constraints.append(Equation(item_expression.width - item.width))
      if item.height_policy == LayoutPolicy.FIXED:
        constraints.append(Equation(item_expression.height - item.height))
      if width_sum is None:
        width_sum = item_expression.width
      else:
        width_sum += item_expression.width
      if height_sum is None:
        height_sum = item_expression.height
      last_item = item_expression
    width_expression = VariableExpression('width')
    constraints.append(Equation(width_expression - width))
    width_sum -= width_expression
    constraints.append(Equation(width_sum))
    height_expression = VariableExpression('height')
    constraints.append(Equation(height_expression - height))
    height_sum -= height_expression
    constraints.append(Equation(height_sum))
    print(ConstraintSystem(constraints))
    solution = solve(ConstraintSystem(constraints))
    for case in solution:
      name_index = case.find('.')
      if name_index == -1:
        continue
      item = self._name_to_item[case[0:name_index]]
      property = case[name_index + 1:]
      if property == 'top':
        item.top = solution[case]
      elif property == 'left':
        item.left = solution[case]
      elif property == 'width':
        item.width = solution[case]
      elif property == 'height':
        item.height = solution[case]
    print(solution)
    self._width = solution['width']
    self._height = solution['height']


def check_is_fit(components, width, height):
  area = 0
  for component in components:
    area += component.width * component.height
  return area == width * height
