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


if __name__ == '__main__':
  unittest.main()
