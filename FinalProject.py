import sympy as sym
from sympy import *

"""
Fritz-John Necessary Conditions Algorithm
"""

x, y = sym.symbols('x y', real = True)

# Inputs
# Input Objective Function
f_eq = (x - 3)**2 + (y - 2)**2 # Objective function

# Input Constraints
# If different number of constraints, add or remove accordingly with same naming convention g#, add to constraints
g1 = x**2 + y**2 -5 <= 0
g2 = x + 2*y - 4 <= 0
g3 = -x <= 0
g4 = -y <= 0
constraints = [g1, g2, g3, g4]

# Adjust # of lambdas based on how many constraints used
l0, l1, l2, l3, l4 = sym.symbols('l0 l1 l2 l3 l4', real = True)
lambdas_list_start = [l0, l1, l2, l3, l4] # Make sure this matches the line above

# Remove the inequality to be able to solve for them later
list_constraints = [x.lhs for x in constraints]

# Graph of Constraints, add any necessary constraints here
plot_of_constraints = plot_implicit(And(g1, g2, g3, g4), line_color = "steelblue")

# Finds all intersections of constraints, outputs points
list_points = []
for i in range(0, len(list_constraints)):
    for j in range(0, len(list_constraints)):
        if i < j:
            list_points.append(sym.solve([list_constraints[i], list_constraints[j]]))

# Find Gradient of objective function
Obj_gradient = [diff(f_eq, x), diff(f_eq, y)]

# Find gradient of all constraints
list_gradient_constraints = []
for i in range(0, len(list_constraints)):
    list_gradient_constraints.append([diff(list_constraints[i], x), diff(list_constraints[i], y)])

# Print them all out
print(f"Gradient of Objective Function: {Obj_gradient}")
print(f"Gradient of all constraints: {list_gradient_constraints}")

# Rounds the output to 3 decimal points
for point in list_points:
    if type(point) is list:
        for soln in point:
            for key in soln:
                soln[key] = soln[key].evalf(4)
    else:
        for key in point:
            point[key] = point[key].evalf(4)

final_point_list = []
# Convert to usable list
for i in range(0, len(list_points)):
    if type(list_points[i]) is list:
        for j in range(0, len(list_points[i])):
            final_point_list.append([list_points[i][j][x], list_points[i][j][y]])
    else:
        final_point_list.append(list(list_points[i].values()))

# Eliminate any points not in the bounds
for i in range(0, len(final_point_list)):
    for j in range(0, len(list_constraints)):
        # There is an error when you try to sub in for example y into equation with only an x variable, this is to handle those
        try:
            # If there is no error when subbing both run the if statement
            # If any constraint(x, y) > 0, remove the point
            if list_constraints[j].subs(x, final_point_list[i][0]).subs(y, final_point_list[i][1]).evalf() > 0:
                del final_point_list[i][0]
                del final_point_list[i][0]
                break

            # If there is an error do this
        except IndexError:
            try:
                if list_constraints[j].subs(x, final_point_list[i][0]).evalf() > 0:
                    del final_point_list[i][0]
                    del final_point_list[i][0]
                    break
            except IndexError:
                if list_constraints[j].subs(y, final_point_list[i][1]).evalf() > 0:
                    del final_point_list[i][0]
                    del final_point_list[i][0]
                    break

# When removing items from a list it doesn't remove the brackets so need to ammend it with a new list
bound_point_list = []
for i in range(0, len(final_point_list)):
    # If an element is none empty add it to the final bound list
    if final_point_list[i] != []:
        bound_point_list.append(final_point_list[i])
        
print(f"Possible points found: {bound_point_list}")

# Run Fritz-John Algorithm for all found feasible points.
for p in range(0, len(bound_point_list)):
    # Bring down the lambdas, reset values with every run
    lambdas_list = lambdas_list_start.copy()

    # Keep track which ones have already been solved for
    place_hold_list = [1] * len(lambdas_list)

    # First find which constraints are active
    test_point = bound_point_list[p]
    print(" ")
    print(f"Testing point: {test_point}")
    print(f"Lambda values: {lambdas_list}")
    for i in range(0, len(list_constraints)):
        for j in range(0, len(list_constraints)):
            if list_constraints[j].subs(x, test_point[0]).subs(y, test_point[1]).evalf() < 0:
                lambdas_list[j+1] = 0

    for i in range(0, len(lambdas_list)):
        if lambdas_list[i] == 0:
            print(f"Found constraint {i} to be inactive, setting l{i} = 0")

    # Output the updated values
    print(f"Lambda values: {lambdas_list}")

    # Update the list that keeps track which have been solved
    for i in range(1, len(lambdas_list)):
        if lambdas_list[i] != 0:
            place_hold_list[i] = 0

    # Seperate the gradient into two sides, the x and y
    gradient_x_list = []
    gradient_y_list = []
    for i in range(0, len(list_gradient_constraints)):
        gradient_x_list.append(list_gradient_constraints[i][0])
        gradient_y_list.append(list_gradient_constraints[i][1])

    # Initialize, obj function always the same
    eq1 = lambdas_list[0]*Obj_gradient[0] 
    eq2 = lambdas_list[0]*Obj_gradient[1] 

    # Next, put the equations together and solve for the lambdas
    # Since unknown constraints need a loop to make the full equation
    for i in range(0, len(gradient_x_list)):
        eq1 = eq1 + lambdas_list[i+1]*gradient_x_list[i]
        eq2 = eq2 + lambdas_list[i+1]*gradient_y_list[i]
    print(f"X Equation: {eq1} = 0")
    print(f"Y Equation: {eq2} = 0")

    # Plug in the point being tested
    eq1 = eq1.subs(x, test_point[0]).subs(y, test_point[1])
    eq2 = eq2.subs(y, test_point[1]).subs(x, test_point[0])
    print(f"Plugging in point {test_point}")
    print(f"X Equation: {eq1} = 0")
    print(f"Y Equation: {eq2} = 0")

    # First we try l0 = 0 (KKT way of solving)
    eq1_test = eq1.subs(l0, 0)
    eq2_test = eq2.subs(l0, 0)
    lambdas_list[0] = 0
    print(f"Trying lambda_0 = 0")
    print(f"X Equation: {eq1_test} = 0")
    print(f"Y Equation: {eq2_test} = 0")

    # Solve for remaining lambdas with l0 = 0
    sol0 = sym.solve([eq1_test, eq2_test])
    sol0_list = list(sol0.values()) 

    # Update the lambda values based on the previous solver, 
    # to automate needed to make it a loop since we don't know which lambdas will not be solved by this points
    for i in range(0, len(place_hold_list)):
        if place_hold_list[i] == 0:
            lambdas_list[i] = sol0_list[0]
            sol0_list.pop(0)

    # Output the updated list
    print("Solving for remaining values...")
    print(f"Lambda values: {lambdas_list} for (x, y) = {test_point}")

    # If any of these are negative the solution is bad
    negative_found = 0
    for i in range(0, len(lambdas_list)):
        if lambdas_list[i] < 0:
            negative_found = 1

    # If all the lambdas are equal to 0 or a negative is there, try l0 = 1
    if lambdas_list == ([0] * len(lambdas_list)) or negative_found == 1:
        print("Did not hold with lambda_0 = 0, trying lambda_0 = 1")

        # Same algorithm as before
        eq1_test1 = eq1.subs(l0, 1)
        eq2_test1 = eq2.subs(l0, 1)
        lambdas_list[0] = 1
        print(f"X Equation: {eq1_test1} = 0")
        print(f"Y Equation: {eq2_test1} = 0")

        # Solve for remaining values
        try:
            sol1 = sym.solve([eq1_test1, eq2_test1])
            sol1_list = list(sol1.values()) 
            for i in range(0, len(place_hold_list)):
                if place_hold_list[i] == 0:
                    lambdas_list[i] = sol1_list[0]
                    sol1_list.pop(0)
            print("Solving for remaining values...")
            print(f"Lambda values: {lambdas_list} for (x, y) = {test_point}")

        # Sometimes there can be an error if not enough unsolved lambdas such as -1.5 = 0, this gives an error that shows that the solution is bad
        except AttributeError:
            print(f"Lambda values: {lambdas_list} for (x, y) = {test_point}")
            print(f"Fritz-John Neccesary Conditions do not hold at point {test_point}")
            continue

    # See if the point passes Fritz-John Necessary Conditions
    found_negative = 0
    all_zeroes = 0
    if lambdas_list == ([0] * len(lambdas_list)):
        all_zeroes = 1
    for i in range(1, len(lambdas_list)):
        # Any of the values negative, FJNC failed
        if lambdas_list[i] < 0:
            found_negative = 1

    if found_negative == 1:
        print(f"Fritz-John Neccesary Conditions do not hold at point {test_point}")
    # No negative values so FJNC works
    elif found_negative == 0 and all_zeroes == 0:
        print(f"Fritz-John Neccesary Conditions holds at point {test_point}")
# %%
