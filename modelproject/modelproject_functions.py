# Import modules
import sympy as sm
import matplotlib.pyplot as plt
import numpy as np
import types

# Function that plot relevant function in project
def make_plot(f, xs, alpha_val, phi_val, epsilon_val):
    '''Plots the function f for the input values in xs
    given the parameter values alpha, phi, and epsilon.
    
    Parameters
    ----------
    f (sympy expression): Function to plot
    xs (np.ndarray):      Array of xs to plot f for
    alpha_val (float):    Parameter value for alpha
    phi_val (float):      Parameter value for phi
    epsilon_val (float):  Paramter value for epsilon
    
    Returns
    -------
    fig (figure):         The plot of f
    '''
    
    # Define parameters as sympy symbols
    epsilon = sm.symbols('epsilon')
    phi = sm.symbols('phi')
    alpha = sm.symbols('alpha')
    w = sm.symbols('w')
    
    # a. Labour demand should also have all paramters as input (or else error)
    f = f + phi*0 + epsilon*0
    
    # Make sympy expression a Python function
    func = sm.lambdify((w, alpha, phi, epsilon), f)
    
    # Generate function values for all x
    ys = []
    
    for x in xs:
        ys.append(func(x, alpha_val, phi_val, epsilon_val))
        
    ys = np.array(ys)
    
    # Make plot
    return plt.plot(xs, ys)

# Function that finds root with bisection method
def bisection(f, a, b, max_iter=1000, tol=1e-6):
    '''Solves f(x) = 0 for a <= x <= b. I.e. the function f()
    has a root in the interval [a,b], which bisection() finds. 
    
     Parameters
     ----------
        f (callable):   Function
        a (float):      Left bound of interval
        b (float):      Right bound of interval
        max_iter (int): Maximum number of iterations
        tol (float):    Tolerance on solution
        
    Returns
    -------    
         m (float):     x value at the root found (should be close to 0)
         fm (float):    Function value at m
         i (int):       Number of iterations
    '''
    
    # Check that the bisection methods works for inputs
    if f(a)*f(b) >= 0:
        print("Bisection method cannot find potential root in this interval")
        return None
    
    if not isinstance(f, types.FunctionType):
        print("f needs to be a Python function")
        return None
    
    # Step 1: Define interval
    x_left = a
    x_right = b
    
    i = 0
    while i < max_iter:
        # Step 2: Compute function value at midpoint 
        m = (x_left + x_right)/2
        fm = f(m)

        # Step 3: Reduce interval
        if abs(fm) < tol:
            break    # Break if function value at midpoint is smaller than the tolerance
            
        elif fm*f(x_left) < 0:
            x_right = m
            
        elif fm*f(x_right) < 0:
            x_left = m
            
        i += 1
            
    return m, fm, i