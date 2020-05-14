# Import packages
import numpy as np
import itertools as it
from scipy import optimize
from tqdm import tqdm


# A function that calls a solver to optimize the choice of labour supply
def find_solution(budget_constraint, utility, m, w, epsilon, kappa, nu, tau0, tau1):
    '''Finds the optimal labour supply, consumption level, and resulting utility of individual
    with specified budget constraint and utility function. 
    
    Inputs:
    -------
    budget_constraint (callable): The budget constraint of the individual
    utility (callable):           Utility function of the individual
    m (float):                    Cash on hand
    w (float):                    Wage rate
    epsilon (float):              Frisch elasticity of labour supply
    kappa (float):                Income cut-off for paying top tax
    nu (float):                   Labour disutility scalar
    tau0 (float):                 Standard labour tax rate
    tau1 (float):                 Extra tax when paying top tax
    
    Returns:
    --------
    l_star (float):               Optimal labour supply
    c_star (float):               Optimal consumption level
    utility_star (float)          Utility resulting from the optimal labour and consumption
    '''
    
    # a. Define the objective function to minimize
    obj = lambda l: -utility(l, budget_constraint(l, m, w, kappa, tau0, tau1), epsilon, nu) 
    
    # b. Minimize the objective function using scipy optimize
    res = optimize.minimize_scalar(
        obj,
        method = 'bounded', 
        bounds = (0,1)
    )
    
    # c. Get the optimal labour, consumption, and resulting utility
    l_star = res.x
    c_star = budget_constraint(l_star, m, w, kappa, tau0, tau1)
    utility_star = utility(l_star, c_star, epsilon, nu)

    return [l_star, c_star, utility_star]


def total_tax(N, low, high, seed, budget_constraint, utility, m, epsilon, kappa, nu, tau0, tau1):
    '''Calculates the total tax revenue in a population with N individuals and wages that are 
    randomly drawn from a uniform distribution.
    
    Inputs:
    -------
    N (integer):                  Size of population
    low (float):                  Lower boundary of uniform distribution wage rates are drawn from
    high (float):                 Upper boundary of uniform distribution wage rates are drawn from
    seed (int):                   Random seed
    budget_constraint (callable): The budget constraint of the individuals
    utility (callable):           Utility function of the individuals
    m (float):                    Cash on hand
    epsilon (float):              Frisch elasticity of labour supply
    kappa (float):                Income cut-off for paying top tax
    nu (float):                   Labour disutility scalar
    tau0 (float):                 Standard labour tax rate
    tau1 (float):                 Extra tax when paying top tax
    
    Returns:
    --------
    T:                            Total tax revenue
    '''
    
    # a. Set random seed and initialise sum of tax revenue
    np.random.seed(seed)
    T = 0
    
    # b. Randomly draw N wage rates from uniform distribution
    w_vec = np.random.uniform(low=low, high=high, size=N)

    # c. Loop over all individuals in the population
    for i in range(N):

        # i. Find the individual's optimal labour supply
        sol = find_solution(budget_constraint, utility, m, w_vec[i], epsilon, kappa, nu, tau0, tau1)
        l_opt = sol[0]

        # ii. Calculate the individual's tax constribution given the optimal labour supply
        tax_contr = tau0*w_vec[i]*l_opt + tau1*max((w_vec[i]*l_opt - kappa), 0)

        # iii. Add the tax contribution to the total tax revenue
        T += tax_contr
        
    return T