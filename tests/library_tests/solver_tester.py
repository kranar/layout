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
    self.assertEqual(len(actual.assignments), len(expected.assignments))
    for key in actual.assignments:
      self.assertAlmostEqual(actual.assignments[key], expected.assignments[key],
        msg=key)
    self.assertEqual(actual.inconsistencies, expected.inconsistencies)
    self.assertEqual(actual.underdetermined, expected.underdetermined)

  def test_solve_single_variable(self):
    equations = []
    equations.append(Equation(x))
    system = ConstraintSystem(equations)
    solution = solve(system)
    self.assertSolutionEqual(solution, Solution({'x': 0}))

  def test_solve_single_variable_addition(self):
    equations = []
    equations.append(Equation(x + 5))
    system = ConstraintSystem(equations)
    solution = solve(system)
    self.assertSolutionEqual(solution, Solution({'x': -5}))

  def test_solve_single_variable_subtraction(self):
    equations = []
    equations.append(Equation(x - 5))
    system = ConstraintSystem(equations)
    solution = solve(system)
    self.assertSolutionEqual(solution, Solution({'x': 5}))

  def test_solve_single_variable_multiplication(self):
    equations = []
    equations.append(Equation(3 * x))
    system = ConstraintSystem(equations)
    solution = solve(system)
    self.assertSolutionEqual(solution, Solution({'x': 0}))

  def test_solve_single_variable_division(self):
    equations = []
    equations.append(Equation(x / 6))
    system = ConstraintSystem(equations)
    solution = solve(system)
    self.assertSolutionEqual(solution, Solution({'x': 0}))

  def test_solve_single_variable_multiply_and_add(self):
    equations = []
    equations.append(Equation(2 * x - 6))
    system = ConstraintSystem(equations)
    solution = solve(system)
    self.assertSolutionEqual(solution, Solution({'x': 3}))

  def test_solve_single_variable_collect_terms(self):
    equations = []
    equations.append(Equation(2 * x - 6 * x + 12))
    system = ConstraintSystem(equations)
    solution = solve(system)
    self.assertSolutionEqual(solution, Solution({'x': 3}))

  def test_solve_two_variables(self):
    equations = []
    equations.append(Equation(3 * x - y - 7))
    equations.append(Equation(2 * x + 3 * y - 1))
    system = ConstraintSystem(equations)
    solution = solve(system)
    self.assertSolutionEqual(solution, Solution({'x': 2, 'y': -1}))

  def test_solve_three_variables(self):
    equations = []
    equations.append(Equation(x - 2 * y + 3 * z - 9))
    equations.append(Equation(3 * y - x - z + 6))
    equations.append(Equation(2 * x - 5 * y + 5 * z - 17))
    system = ConstraintSystem(equations)
    solution = solve(system)
    self.assertSolutionEqual(solution, Solution({'x': 1, 'y': -1, 'z': 2}))

  def test_single_variable_inconsistent_solution(self):
    equations = []
    equations.append(Equation(x + 1))
    equations.append(Equation(x + 2))
    system = ConstraintSystem(equations)
    solution = solve(system)
    self.assertSolutionEqual(solution, Solution(inconsistencies={'x'}))

  def test_single_variable_contradiction(self):
    equations = []
    equations.append(Equation(x + 1))
    equations.append(Equation(LiteralExpression(5)))
    system = ConstraintSystem(equations)
    solution = solve(system)
    self.assertSolutionEqual(
      solution, Solution({'x': -1}, inconsistencies={''}))

  def test_semiconsistent_solution(self):
    equations = []
    equations.append(Equation(x + 1))
    equations.append(Equation(x + 2))
    equations.append(Equation(y - 3))
    system = ConstraintSystem(equations)
    solution = solve(system)
    self.assertSolutionEqual(
      solution, Solution(assignments={'y': 3}, inconsistencies={'x'}))

  def test_inconsistent_solution_multiple_variables(self):
    equations = []
    equations.append(Equation(x + y - 1))
    equations.append(Equation(2 * x + y - 1))
    equations.append(Equation(3 * x + 2 * y - 3))
    system = ConstraintSystem(equations)
    solution = solve(system)
    self.assertSolutionEqual(solution, Solution(inconsistencies={'x', 'y'}))

  def test_inconsistent_propagation(self):
    equations = []
    equations.append(Equation(x - 1))
    equations.append(Equation(y - 2))
    equations.append(Equation(z - 3))
    equations.append(Equation(x - y))
    system = ConstraintSystem(equations)
    solution = solve(system)
    self.assertSolutionEqual(
      solution, Solution({'z': 3}, inconsistencies={'x', 'y'}))

  def test_underdetermined_solution(self):
    equations = []
    equations.append(Equation(x + y))
    system = ConstraintSystem(equations)
    solution = solve(system)
    self.assertSolutionEqual(solution, Solution(underdetermined={'x', 'y'}))

  def test_underdetermined_solution_with_cancelling(self):
    equations = []
    equations.append(Equation(x + y - y + 5))
    system = ConstraintSystem(equations)
    solution = solve(system)
    self.assertSolutionEqual(
      solution, Solution({'x': -5}, underdetermined={'y'}))

  def test_underdetermined_solution_multiple_equations(self):
    equations = []
    equations.append(Equation(x + y))
    equations.append(Equation(2 * x + 2 * y))
    system = ConstraintSystem(equations)
    solution = solve(system)
    self.assertSolutionEqual(solution, Solution(underdetermined={'x', 'y'}))

  def test_cancelling_out(self):
    equations = []
    equations.append(Equation(x + y))
    equations.append(Equation(y - y + x + 2))
    equations.append(Equation(x - x + y - 2))
    system = ConstraintSystem(equations)
    solution = solve(system)
    self.assertEqual(solution, Solution({'x': -2, 'y': 2}))

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
    self.assertSolutionEqual(solution,
      Solution({width.name: 1000, height.name: 200,
       a_top.name: 0, a_left.name: 0, a_width.name: 100, a_height.name: 200,
       b_top.name: 0, b_left.name: 100, b_width.name: 800, b_height.name: 200,
       c_top.name: 0, c_left.name: 900, c_width.name: 100, c_height.name: 200}))

  def test_underdetermined_layout(self):
    a_left = VariableExpression('A.left')
    a_width = VariableExpression('A.width')
    a_width_growth = VariableExpression('A.width_growth')
    b_left = VariableExpression('B.left')
    b_width = VariableExpression('B.width')
    width = VariableExpression('width')
    equations = []
    equations.append(Equation(a_left))
    equations.append(Equation(a_width - width))
    equations.append(Equation(-1 + a_width_growth))
    equations.append(Equation(b_left))
    equations.append(Equation(b_width - 100))
    equations.append(Equation(b_width - width))
    equations.append(Equation(a_width - 100 - a_width_growth * (width - 100)))
    system = ConstraintSystem(equations)
    solution = solve(system)
    self.assertFalse(solution.is_inconsistent)

  def test_mixed_equation(self):
    system = ConstraintSystem([Equation(x + y + y - 2 * y - 5)])
    solution = solve(system)
    self.assertSolutionEqual(
      solution, Solution({x.name: 5}, underdetermined={y.name}))

  def test_isolate_zero_coefficient(self):
    expression = Equation(x + y - x)
    x_isolate = isolate('x', expression)
    self.assertEqual(x_isolate, None)

  def test_composite_isolate_zero_coefficient(self):
    expression = Equation((x + y) - (x + 200.0))
    x_isolate = isolate('x', expression)
    self.assertEqual(x_isolate, None)
