import os
import sys
sys.path.insert(
  0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import json
import tkinter as tk

from library import *


def parse_components(solution):
  items = {}
  for case in solution:
    name_index = case.find('.')
    if name_index == -1:
      continue
    name = case[0:name_index]
    if name not in items:
      items[name] = LayoutItem(name)
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
    self._height = self.winfo_reqheight()
    self._width = self.winfo_reqwidth()

  def on_resize(self, event):
    components = self._components.copy()
    components.append(Equation(VariableExpression('width') - event.width))
    components.append(Equation(VariableExpression('height') - event.height))
    system = ConstraintSystem(components)
    solution = solve(system)
    components = parse_components(solution)
    if check_is_fit(components, event.width, event.height):
      self.master.geometry(f'{self._width}x{self._height}')
      return
    self._width = event.width
    self._height = event.height
    self._canvas.delete('all')
    for component in components:
      self._canvas.create_rectangle(
        component.left, component.top, component.left + component.width,
        component.top + component.height, fill='red', outline='black')


def parse_policy(source):
  if source == 'fixed':
    return LayoutPolicy.FIXED
  elif source == 'expanding':
    return LayoutPolicy.EXPANDING


def parse_size(source):
  tokens = source.split(' ')
  if len(tokens) == 1:
    return (int(tokens[0]), LayoutPolicy.FIXED)
  elif len(tokens) == 2:
    return (int(tokens[0]), parse_policy(tokens[1]))


def parse_layout_items(source):
  items = []
  unnamed_count = 0
  for layout in source['layout']:
    if 'name' in layout:
      name = layout['name']
    else:
      name = f'@unnamed_{unnamed_count}'
      unnamed_count += 1
    item = LayoutItem(name)
    item.top = layout['top']
    item.left = layout['left']
    width = parse_size(layout['width'])
    item.width = width[0]
    item.width_policy = width[1]
    height = parse_size(layout['height'])
    item.height = height[0]
    item.height_policy = height[1]
    items.append(item)
  return items


def parse_system(items):
  top_items = sorted(items, key=lambda x: (x.top, x.left))
  constraints = []
  last_item = None
  for item in top_items:
    if item.left == 0:
      constraints.append(Equation(VariableExpression(item.name + '.left'))) 
    elif last_item is not None:
      constraints.append(Equation(
        VariableExpression(item.name + '.left') -
        (VariableExpression(last_item.name + '.left') +
        VariableExpression(last_item.name + '.width'))))
    if item.top == 0:
      constraints.append(Equation(VariableExpression(item.name + '.top')))
    if item.width_policy == LayoutPolicy.FIXED:
      constraints.append(
        Equation(VariableExpression(item.name + '.width') - item.width))
    if item.height_policy == LayoutPolicy.FIXED:
      constraints.append(
        Equation(VariableExpression(item.name + '.height') - item.height))
    last_item = item
  width_sum = None
  for item in top_items:
    if item.top == 0:
      extension = VariableExpression(item.name + '.width')
    if width_sum is None:
      width_sum = extension
    else:
      width_sum += extension
  width_sum -= VariableExpression('width')
  constraints.append(Equation(width_sum))
  system = ConstraintSystem(constraints)
  return ConstraintSystem(constraints)


def main():
  items = parse_layout_items(json.load(open(sys.argv[1])))
  system = parse_system(items)
  window = tk.Tk()
  window.geometry('200x100')
  LayoutWidget(window, system.constraints).place(
    x=0, y=0, relwidth=1, relheight=1)
  window.mainloop()


if __name__ == '__main__':
  main()
