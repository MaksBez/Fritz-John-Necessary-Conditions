# %%
# Fritz-John Necessary Conditions Algorithm

Fritz-John Necessary Conditions tell you if a certain point holds for an multi-variable objective function under constraints.

This code will input an objective function (f(x, y)) and inequality constraints (g(x, y)) then it finds potential points on the bound and see if those points pass the Fritz-John Necessary Conditions

This algorithm thus far only works for **two variables** objective function and requires **minimum two inequality constraints**.

This will require the installation of SymPy as it is the main package used in this algorithm.

This will not require any data, just functions.

## Input

**Objective Function**: the input is on line 12 it is titled "f_eq = " your objective function goes after that = sign. Use normal python syntax for equations. The objective function can be nonlinear.

**Inequality Constraints**: Located right below with "g#" as its title. The # represents what constraint # it is. Enter as many as you would like with the same format and a <= 0 at the end (convert inequalities to this format for the algorithm to work). The constraints can be nonlinear, there is no limiation.

Minimum two inequality constraints required.

**Lambdas**: You also need to input the matching lambdas. You need as many lambdas as you do inequality constraints. They are named with the format "l#"

**Graphing**: Enter all of the used constraints in line 30.

## How it Works

**Plotting Possible Points**: First, the code from lines 29 to 37 uses the SymPy package to implicit graph the inequality constraints then a for loop is ran to find the intersection between all of the constraints. To find the intersection a simple solver is used. Those points are then put into a list which will be used later.

**Gradient Calculations**: Next, the code finds the gradient of the objective function and the constraints and puts them into a list

**Possible Points Elimination**: The points are outputted as dictionary because of the package, so it is converted into just a list of points. Then it looks to see which of those points are actually in the bound and keeps them.

**Algorithm**: The algorithm is just a for loop that runs for all points. First we bring down the lambdas and then begin by seeing which constraits are inactive at that point, if they are inactive l#constraint is set to 0. Next the algorithm test l0 = 0 and if that yields lambdas that are either negative or all 0, it tries l0 = 1. It does the same thing for l0 = 1 and if there are negatives or all are 0 (except for l0) then that point does not hold. If it does pass for either of the l0's though then that point passes the Fritz-John Neccesary Conditions.

## Output

After inputting you will be shown a graph of your bound and possible points on that bound. The algorithm makes sure they are within the constraints.

The program will then test each one individually, outputting each step in the algorithm specifically.

It will run for all points, no matter if they pass the Fritz-John Necessary Conditions or not.

If it does pass, at the bottom it will say "Fritz-John Necessary Conditions holds at point [x, y]"
If it does not pass, at the bottom it will say "Fritz-John Necessary Conditions do not hold at point [x, y]"

## Limitations

1. The algorithm currently only works for two variables (you can change their name).

2. The constraints must be inequality constraints in the form "xy <= 0"

3. Minimum two constraints required so that it can find possible points to work with

4. Cannot input any point you want

## Issues

1. Lambdas must be inputted manually.

2. Graph must get its inequalities inputted manually.

3. If the constraints do not intersect or there aren't enough of them it will not find any points.

## Future Implimintation

1. Works to be able to input any point by the user.

2. Work for any number of variables.

3. For for equality constraints as well.

# Required Resources to Run Code

1. SymPy installation
