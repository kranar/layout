import unittest

from library import *


class LayoutTester(unittest.TestCase):
  def test_single_fixed_solution(self):
    a = LayoutItem('A', 0, 0, 100, LayoutPolicy.FIXED, 100, LayoutPolicy.FIXED)
    layout = Layout([a], [])
    self.assertEqual(layout.items, [a])
    self.assertEqual(layout.constraints, [])
    self.assertEqual(layout.width, 100)
    self.assertEqual(layout.height, 100)
    layout.resize(200, 100)
    self.assertEqual(layout.width, 100)
    self.assertEqual(layout.height, 100)
    self.assertEqual(layout.items, [a])

  def test_single_horizontal_expanding_solution(self):
    a = LayoutItem(
      'A', 0, 0, 100, LayoutPolicy.EXPANDING, 100, LayoutPolicy.FIXED)
    layout = Layout([a], [])
    self.assertEqual(layout.items, [a])
    self.assertEqual(layout.constraints, [])
    self.assertEqual(layout.width, 100)
    self.assertEqual(layout.height, 100)
    layout.resize(200, 100)
    self.assertEqual(layout.width, 200)
    self.assertEqual(layout.height, 100)
    a.width = 200
    self.assertEqual(layout.items, [a])

  def test_double_fixed_solution(self):
    a = LayoutItem('A', 0, 0, 100, LayoutPolicy.FIXED, 100, LayoutPolicy.FIXED)
    b = LayoutItem(
      'B', 0, 100, 200, LayoutPolicy.FIXED, 100, LayoutPolicy.FIXED)
    layout = Layout([a, b], [])
    self.assertEqual(layout.items, [a, b])
    self.assertEqual(layout.constraints, [])
    self.assertEqual(layout.width, 300)
    self.assertEqual(layout.height, 100)
    layout.resize(200, 100)
    self.assertEqual(layout.width, 300)
    self.assertEqual(layout.height, 100)
    self.assertEqual(layout.items, [a, b])
    layout.resize(600, 100)
    self.assertEqual(layout.width, 300)
    self.assertEqual(layout.height, 100)
    self.assertEqual(layout.items, [a, b])

  def test_double_expanding_solution(self):
    a = LayoutItem(
      'A', 0, 0, 100, LayoutPolicy.EXPANDING, 100, LayoutPolicy.FIXED)
    b = LayoutItem(
      'B', 0, 100, 200, LayoutPolicy.EXPANDING, 100, LayoutPolicy.FIXED)
    layout = Layout([a, b], [])
    self.assertEqual(layout.items, [a, b])
    self.assertEqual(layout.constraints, [])
    self.assertEqual(layout.width, 300)
    self.assertEqual(layout.height, 100)
    layout.resize(500, 100)
    self.assertEqual(layout.width, 500)
    self.assertEqual(layout.height, 100)
    a.width = 200
    b.left = 200
    b.width = 300
    self.assertEqual(layout.items, [a, b])

  def test_two_fixed_rows(self):
    a = LayoutItem('A', 0, 0, 100, LayoutPolicy.FIXED, 100, LayoutPolicy.FIXED)
    b = LayoutItem(
      'B', 100, 0, 100, LayoutPolicy.FIXED, 100, LayoutPolicy.FIXED)
    layout = Layout([a, b], [])
    self.assertEqual(layout.items, [a, b])
    self.assertEqual(layout.constraints, [])
    self.assertEqual(layout.width, 100)
    self.assertEqual(layout.height, 200)
    layout.resize(200, 100)
    self.assertEqual(layout.width, 100)
    self.assertEqual(layout.height, 200)
    self.assertEqual(layout.items, [a, b])

  def test_two_expanding_rows(self):
    a = LayoutItem(
      'A', 0, 0, 100, LayoutPolicy.EXPANDING, 100, LayoutPolicy.FIXED)
    b = LayoutItem(
      'B', 100, 0, 100, LayoutPolicy.EXPANDING, 100, LayoutPolicy.FIXED)
    layout = Layout([a, b], [])
    self.assertEqual(layout.items, [a, b])
    self.assertEqual(layout.constraints, [])
    self.assertEqual(layout.width, 100)
    self.assertEqual(layout.height, 200)
    layout.resize(200, 100)
    self.assertEqual(layout.width, 200)
    self.assertEqual(layout.height, 200)
    a.width = 200
    b.width = 200
    self.assertEqual(layout.items, [a, b])

if __name__ == '__main__':
  unittest.main()
