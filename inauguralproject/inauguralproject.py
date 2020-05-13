# importint packages
import numpy as np
import itertools as it
from scipy import optimize
from tqdm import tqdm

# question 1 #

# b. Define the utility function
def utility(l, c):
    return np.log(c) - nu*(l**(1 + 1/epsilon)/(1 + 1/epsilon))

# c. Define budget constraint
def budget_constraint(l):
    return m + w*l - (tau0*w*l + tau1*max((w*l - kappa), 0))

# d. Define objective function (to minimize)
def objective(l):
    c = budget_constraint(l)
    
    return -utility(l, c) # It is negative since we're going to minimize the objective function

# e. Write a function that calls a solver to optimize the choice of labour supply
def find_solution():
    res = optimize.minimize_scalar(
        objective,
        method = 'bounded', 
        bounds = (0,1)
    )
    
    l_star = res.x
    c_star = budget_constraint(l_star)
    utility_star = utility(l_star, c_star)

    
    return [l_star, c_star, utility_star]

#Question 2-4 see the ipynb file



# question 5

#defining f again, but with given l and c
def f(c = 1, l = 1, nu = 10, epsilon = 0.3):
    return np.log(c) - nu*(l**(1+1/epsilon))/(1+1/epsilon)

#We define a new tax function
TAX = 0
def tottax(tau0, tau1, kappa, m, nu, epsilon, w):
    global TAX
    TAX = 0
    #The total amount of resources given by l is defined:
    def x(l):
        x = 0
        for wrand in w:
            x = x + m + wrand*l - (tau0*wrand*l + tau1*np.fmax(wrand*l-kappa,0))
        return x
    #Optimizing with l as variable
    def obj3(l):
        c = x(l)
        return -f(c,l)

    # calculation total tax revenue now with bounded, and create a list with the optimal taxes
    for wrand in w:
        sol = optimize.minimize_scalar(obj3, bounds=(0,1), method='bounded')
        ltax = sol.x # the current optimal l given wage
        TAX = TAX + tau0*wrand*ltax+tau1*np.fmax(wrand*ltax-kappa,0) # sum total tax revenue
    #The total tax is the sum of all the individual taxes.
    return TAX

def find_solution2(c,l,u,TAX):
    print(f'The optimal tau0 is thus = {c:.8f}')
    print(f'The optimal tau1 is thus = {l:.8f}')
    print(f'The optimal kappa is thus = {u:.8f}')
    print(f'These give a tax revenue of = {TAX:.8f}')