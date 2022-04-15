from asyncio import constants
import unittest

from library import *


class LayoutTester(unittest.TestCase):
  pass
'''
  def test_single_fixed_solution(self):
    a = LayoutItem('A', 0, 0, 100, LayoutPolicy.FIXED, 100, LayoutPolicy.FIXED)
    layout = Layout([a], [])
    self.assertEqual(layout.items, [a])
    self.assertEqual(layout.constraints, [])
    self.assertEqual(layout.width, 100)
    self.assertEqual(layout.height, 100)
    layout.resize(200, 200)
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
'''

if __name__ == '__main__':
  unittest.main()
