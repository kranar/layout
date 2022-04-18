from library import StatementVisitor


class StatementWalker(StatementVisitor):
  '''Implements a depth-first AST walker.'''

  def visit_constraint_system(self, statement):
    for constraint in statement.constraints:
      constraint.visit(self)
    return self.visit_statement(statement)

  def visit_equation(self, statement):
    statement.expression.visit(self)
    return self.visit_statement(statement)

  def visit_expression(self, expression):
    return self.visit_statement(expression)

  def visit_addition(self, expression):
    expression.left.visit(self)
    expression.right.visit(self)
    return self.visit_expression(expression)

  def visit_subtraction(self, expression):
    expression.left.visit(self)
    expression.right.visit(self)
    return self.visit_expression(expression)

  def visit_multiplication(self, expression):
    expression.left.visit(self)
    expression.right.visit(self)
    return self.visit_expression(expression)

  def visit_division(self, expression):
    expression.left.visit(self)
    expression.right.visit(self)
    return self.visit_expression(expression)
