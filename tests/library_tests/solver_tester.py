import unittest

from library import *


a = VariableExpression('a')
b = VariableExpression('b')
c = VariableExpression('c')
x = VariableExpression('x')
y = VariableExpression('y')
z = VariableExpression('z')


class SolverTester(unittest.TestCase):
  def assertSolutionEqual(self, actual, expected):
    for key in actual:
      self.assertAlmostEqual(actual[key], expected[key])
    self.assertEqual(len(actual), len(expected))

  def test_solve_single_variable(self):
    equations = []
    equations.append(Equation(x))
    system = ConstraintSystem(equations)
    solution = solve(system)
    self.assertSolutionEqual(solution, {'x': 0})

  def test_solve_single_variable_addition(self):
    equations = []
    equations.append(Equation(x + 5))
    system = ConstraintSystem(equations)
    solution = solve(system)
    self.assertSolutionEqual(solution, {'x': -5})

  def test_solve_single_variable_subtraction(self):
    equations = []
    equations.append(Equation(x - 5))
    system = ConstraintSystem(equations)
    solution = solve(system)
    self.assertSolutionEqual(solution, {'x': 5})

  def test_solve_single_variable_multiplication(self):
    equations = []
    equations.append(Equation(3 * x))
    system = ConstraintSystem(equations)
    solution = solve(system)
    self.assertSolutionEqual(solution, {'x': 0})

  def test_solve_single_variable_division(self):
    equations = []
    equations.append(Equation(x / 6))
    system = ConstraintSystem(equations)
    solution = solve(system)
    self.assertSolutionEqual(solution, {'x': 0})

  def test_solve_single_variable_multiply_and_add(self):
    equations = []
    equations.append(Equation(2 * x - 6))
    system = ConstraintSystem(equations)
    solution = solve(system)
    self.assertSolutionEqual(solution, {'x': 3})

  def test_solve_single_variable_collect_terms(self):
    equations = []
    equations.append(Equation(2 * x - 6 * x + 12))
    system = ConstraintSystem(equations)
    solution = solve(system)
    self.assertSolutionEqual(solution, {'x': 3})

  def test_solve_two_variables(self):
    equations = []
    equations.append(Equation(3 * x - y - 7))
    equations.append(Equation(2 * x + 3 * y - 1))
    system = ConstraintSystem(equations)
    solution = solve(system)
    self.assertSolutionEqual(solution, {'x': 2, 'y': -1})

  def test_solve_three_variables(self):
    equations = []
    equations.append(Equation(x - 2 * y + 3 * z - 9))
    equations.append(Equation(3 * y - x - z + 6))
    equations.append(Equation(2 * x - 5 * y + 5 * z - 17))
    system = ConstraintSystem(equations)
    solution = solve(system)
    self.assertSolutionEqual(solution, {'x': 1, 'y': -1, 'z': 2})

  def test_no_solution(self):
    equations = []
    equations.append(Equation(x + 1))
    equations.append(Equation(x + 2))
    system = ConstraintSystem(equations)
    solution = solve(system)
    self.assertEqual(solution, None)

  def test_no_solution_multiple_variables(self):
    equations = []
    equations.append(Equation(x + y - 1))
    equations.append(Equation(2 * x + y - 1))
    equations.append(Equation(3 * x + 2 * y - 3))
    system = ConstraintSystem(equations)
    solution = solve(system)
    self.assertEqual(solution, None)

  def test_ambiguous_solution(self):
    equations = []
    equations.append(Equation(x + y))
    equations.append(Equation(2 * x + 2 * y))
    system = ConstraintSystem(equations)
    solution = solve(system)
    self.assertEqual(solution, {})

  def test_layout_solution(self):
    equations = []
    a_top = VariableExpression('A.top')
    a_left = VariableExpression('A.left')
    a_width = VariableExpression('A.width')
    a_height = VariableExpression('A.height')
    b_top = VariableExpression('B.top')
    b_left = VariableExpression('B.left')
    b_width = VariableExpression('B.width')
    b_height = VariableExpression('B.height')
    c_top = VariableExpression('C.top')
    c_left = VariableExpression('C.left')
    c_width = VariableExpression('C.width')
    c_height = VariableExpression('C.height')
    width = VariableExpression('width')
    height = VariableExpression('height')
    equations.append(Equation(width - 1000))
    equations.append(Equation(height - 200))
    equations.append(Equation(a_height - height))
    equations.append(Equation(a_top))
    equations.append(Equation(a_left))
    equations.append(Equation(b_top))
    equations.append(Equation(b_left - a_left - a_width))
    equations.append(Equation(b_height - height))
    equations.append(Equation(c_top))
    equations.append(Equation(c_left - b_left - b_width))
    equations.append(Equation(c_height - height))
    equations.append(Equation(a_width + b_width + c_width - width))
    equations.append(Equation(a_width - 100))
    equations.append(Equation(c_width - 100))
    system = ConstraintSystem(equations)
    solution = solve(system)


if __name__ == '__main__':
  unittest.main()
