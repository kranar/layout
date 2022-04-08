import collections

from library.addition_expression import *
from library.constraint_system import *
from library.equation import *
from library.variable_expression import *


def parse_variable(source, c):
  '''Parses a variable and returns it as a VariableExpression.'''
  i = c
  while i != len(source):
    if source[i].isdigit() and i == c or \
        not source[i].isalnum() and not source[i] == '.':
      break
    i += 1
  if i != c:
    return VariableExpression(source[c:i]), i
  return None, c


def parse_literal(source, c):
  '''Parses a literal value and returns it as a LiteralExpression.'''
  i = c
  has_dot = False
  while i != len(source):
    if source[i] == '.':
      if has_dot:
        break
      has_dot = True
    elif not source[i].isdigit():
      break
    i += 1
  if i != c:
    return LiteralExpression(float(source[c:i])), i
  return None, c


def parse_operator(source, c):
  '''Parses an operator.'''
  if source[c] == '+':
    return AdditionExpression, c + 1
  if source[c] == '-':
    return SubtractionExpression, c + 1
  if source[c] == '*':
    return MultiplicationExpression, c + 1
  if source[c] == '/':
    return DivisionExpression, c + 1
  if source[c] == '=':
    return Equation, c + 1
  return None


def get_precedence(operator):
  '''Returns the precedence of an operator.'''
  if operator == Equation:
    return 0
  elif operator == AdditionExpression:
    return 1
  elif operator == SubtractionExpression:
    return 1
  elif operator == MultiplicationExpression:
    return 2
  elif operator == DivisionExpression:
    return 2


def pop_operators(operators, operands, precedence):
  while len(operators) != 0 and (precedence == '(' and
      operators[-1] != '(' or operators[-1] != '(' and
      get_precedence(operators[-1]) >= precedence):
    o = operators.pop()
    right = operands.pop()
    left = operands.pop()
    if o == Equation:
      if isinstance(right, LiteralExpression) and right.value == 0:
        operands.append(Equation(left))
      else:
        operands.append(Equation(SubtractionExpression(left, right)))
    else:
      operands.append(o(left, right))
  if precedence == '(':
    operators.pop()


def parse_constraint(source, c):
  OPERAND = 1
  OPERATOR = 2
  state = OPERAND
  operands = collections.deque()
  operators = []
  while c != len(source) and source[c] != '\n':
    if source[c].isspace():
      c += 1
    elif state == OPERAND:
      if source[c] == '(':
        operators.append('(')
        c += 1
      else:
        operand, c = parse_variable(source, c)
        if not operand:
          operand, c = parse_literal(source, c)
          if not operand:
            raise RuntimeError(f'Syntax error at {c}.')
        operands.append(operand)
        state = OPERATOR
    elif state == OPERATOR:
      if source[c] == ')':
        pop_operators(operators, operands, '(')
        c += 1
      else:
        operator, c = parse_operator(source, c)
        if operator is None:
          raise RuntimeError('Operator expected.')
        pop_operators(operators, operands, get_precedence(operator))
        operators.append(operator)
        state = OPERAND
  pop_operators(operators, operands, -1)
  return operands.pop(), c


def parse(source):
  c = 0
  constraints = []
  while c != len(source):
    if source[c].isspace():
      c += 1
    else:
      constraint, c = parse_constraint(source, c)
      constraints.append(constraint)
  return ConstraintSystem(constraints)
