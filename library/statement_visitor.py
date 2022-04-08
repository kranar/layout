class StatementVisitor:
  '''
  Base class for a visitor over a Statement, allowing an open set of operations
  to be added to a Statement.
  '''

  def visit_statement(self, statement):
    '''Visits the base Statement class.'''
    return

  def visit_constraint_system(self, statement):
    '''Visits the ConstraintSystem class, delegates to the Statement visitor.'''
    return self.visit_statement(statement)

  def visit_equation(self, statement):
    '''Visits the Equation class, delegates to the Statement visitor.'''
    return self.visit_statement(statement)

  def visit_expression(self, expression):
    '''Visits the base Expression class, delegates to the Statement visitor.'''
    return self.visit_statement(expression)

  def visit_addition(self, expression):
    '''
    Visits the AdditionExpression class, delegates to the Expression visitor.
    '''
    return self.visit_expression(expression)

  def visit_subtraction(self, expression):
    '''
    Visits the SubtractionExpression class, delegates to the Expression visitor.
    '''
    return self.visit_expression(expression)

  def visit_multiplication(self, expression):
    '''
    Visits the MultiplicationExpression class, delegates to the Expression
    visitor.
    '''
    return self.visit_expression(expression)

  def visit_division(self, expression):
    '''
    Visits the DivisionExpression class, delegates to the Expression visitor.
    '''
    return self.visit_expression(expression)

  def visit_literal(self, expression):
    '''
    Visits the LiteralExpression class, delegates to the Expression visitor.
    '''
    return self.visit_expression(expression)

  def visit_variable(self, expression):
    '''
    Visits the VariableExpression class, delegates to the Expression visitor.
    '''
    return self.visit_expression(expression)
