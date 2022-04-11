import os
import sys
sys.path.insert(
  0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk

from library import *


class LayoutItem:
  def __init__(self, top=0, left=0, width=0, height=0):
    self.top = top
    self.left = left
    self.width = width
    self.height = height

  def __repr__(self):
    return f'LayoutItem({self.top}, {self.left}, {self.width}, {self.height})'


def parse_components(solution):
  items = {}
  for case in solution:
    name_index = case.find('.')
    if name_index == -1:
      continue
    name = case[0:name_index]
    if name not in items:
      items[name] = LayoutItem()
    item = items[name]
    property = case[name_index + 1:]
    if property == 'top':
      item.top = solution[case]
    elif property == 'left':
      item.left = solution[case]
    elif property == 'width':
      item.width = solution[case]
    elif property == 'height':
      item.height = solution[case]
  return [value for value in items.values()]


class LayoutWidget(tk.Frame):
  def __init__(self, parent, components):
    tk.Frame.__init__(self, parent)
    self._components = components.copy()
    self._canvas = tk.Canvas(self)
    self._canvas.pack(fill=tk.BOTH, expand=tk.YES)
    self._canvas.bind('<Configure>', self.on_resize)

  def on_resize(self, event):
    components = self._components.copy()
    components.append(Equation(VariableExpression('width') - event.width))
    components.append(Equation(VariableExpression('height') - event.height))
    system = ConstraintSystem(components)
    solution = solve(system)
    components = parse_components(solution)
    print(components)
    self._canvas.delete('all')
    for component in components:
      self._canvas.create_rectangle(
        component.left, component.top, component.left + component.width,
        component.top + component.height, fill='red', outline='black')


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


def main():
  window = tk.Tk()
  components = []
  a = LayoutExpression('A')
  b = LayoutExpression('B')
  width = VariableExpression('width')
  height = VariableExpression('height')
  components.append(Equation(a.width - 100))
  components.append(Equation(a.height - 100))
  components.append(Equation(a.top))
  components.append(Equation(a.left))
  components.append(Equation(b.height - 100))
  components.append(Equation(b.top))
  components.append(Equation(b.left - (a.left + a.width)))
  components.append(Equation(a.width + b.width - width))
  LayoutWidget(window, components).place(x=0, y=0, relwidth=1, relheight=1)
  window.mainloop()


if __name__ == '__main__':
  main()
