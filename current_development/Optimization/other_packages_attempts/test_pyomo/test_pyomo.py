from pyomo.environ import Var, Constraint, Objective, ConcreteModel, Set, Param, SolverFactory, maximize
import pyomo.environ as pyo
from pyomo.opt import SolverFactory

# Create a model
model = ConcreteModel()

# Define sets
model.Categories = Set(initialize=['A', 'B', 'C', 'D'])

# Define parameters
model.cat_param = Param(model.Categories, initialize={'A': 1, 'B': 2, 'C': 3, 'D': 4})

# Define decision variables
model.x = Var(within=pyo.Integers)  # Integer variable
model.y = Var(within=pyo.Reals)     # Continuous variable

# Define an integer variable to represent the categorical choice
model.cat_index = Var(within=pyo.Integers, bounds=(1, 4))  # Assuming we have 4 categories

# Map integer variable to categorical variable

# Objective function
def obj_expression(model):
    return 2*model.x + 3*model.y
model.obj = Objective(rule=obj_expression, sense=maximize)

# Constraints
model.con1 = Constraint(expr=model.x + model.y <= 10)
model.con2 = Constraint(expr=model.x >= 0)
model.con3 = Constraint(expr=model.y >= 0)

# Solve the problem
solver = SolverFactory('couenne')  # Use COUENNE solver
result = solver.solve(model, tee=True)

# Print results
print(f"x = {model.x()}, y = {model.y()},")
