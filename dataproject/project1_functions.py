import ipywidgets as widgets
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')
import pandas as pd


def static_plot(dataframe, group='municipality'):
    '''Plots varaible from dataframe for all years available as a static plot.
    
    Parameters
    ----------
    dataframe: DataFrame to choose variable from
    
    variable: Variable to use as y in plot
    '''
    
    fig = plt.figure(dpi=100)
    ax = fig.add_subplot(1,1,1)
    
    # Convert year and variable to numeric
    variable = dataframe.columns[2]
    dataframe.loc[:,['year']] = pd.to_numeric(dataframe['year'])
    
    # Make static plot    
    mun = dataframe['municipality']==group
    x = dataframe.loc[mun,'year'] 
    y = dataframe.loc[mun,variable]
    ax.plot(x,y) 
    ax.set_xlabel('Year')
    
    if variable=='income':
        ax.set_ylabel('Income before taxation (DKK)')
        ax.set_title('Figure 3 Development in Income in Danish Municipalities')
        
    elif variable=='life_expectancy':
        ax.set_ylabel('Years')
        ax.set_title('Figure 4 Development in Life Expectancy in Danish Municipalities')

def interactive_plot(dataframe):
    '''Plots static plot from static_plot() as an interactive figure with drop-down menu to choose between municipalities.
    
    Parameters
    ----------
    dataframe: DataFrame to choose variable from
    '''
    
    # Make list of municipalities
    list_m = []
    for i in dataframe.municipality.unique():
        list_m.append(i)
    
    widgets.interact(static_plot, dataframe = widgets.fixed(dataframe), 
                     group = widgets.Dropdown(description='Municipality', options=list_m, value='Aabenraa'));