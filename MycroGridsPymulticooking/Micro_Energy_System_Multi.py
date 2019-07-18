#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 17 11:23:40 2019

@author: giorgio
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Mar  7 19:27:29 2018

@author: pisto
"""


import pandas as pd
from pyomo.environ import  AbstractModel

from Results_multienergy import Load_results_general, Load_results_Electric, Load_Results_Thermal, Load_Results_Cooking, Load_Results, Plot_Energy_Total
from Model_Creation_Thermal import Model_Creation
from Model_Resolution_Thermal import Model_Resolution
from Economical_Analysis import Levelized_Cost_Of_Energy


# Type of problem formulation:
formulation='LP'

model = AbstractModel() # define type of optimization problem

if formulation == 'LP':
    # Optimization model
    Model_Creation(model) # Creation of the Sets, parameters and variables.
    instance = Model_Resolution(model) # Resolution of the instance
    ## Upload the resulst from the instance and saving it in excel files
    Time_Series_General,Scenarios = Load_results_general(instance) # Extract the results of energy from the instance and save it in a excel file 
    Time_Series_Electric = Load_results_Electric(instance)
    Time_Series_Thermal = Load_Results_Thermal(instance) # Save results into a excel file
    Time_Series_Cooking = Load_Results_Cooking(instance)
    Size_variables = Load_Results(instance)

elif formulation == 'Binary':
    Model_Creation_binary(model) # Creation of the Sets, parameters and variables.
    instance = Model_Resolution_binary(model) # Resolution of the instance    
    Time_Series = Load_results1_binary(instance) # Extract the results of energy from the instance and save it in a excel file 
    Results = Load_results2_binary(instance) # Save results into a excel file
elif formulation =='Integer':
    Model_Creation_Integer(model)
    instance = Model_Resolution_Integer(model)
    Time_Series = Load_results1_Integer(instance) # Extract the results of energy from the instance and save it in a excel file 
    Results = Load_results2_Integer(instance)
# Post procesing tools

Plot_Energy_Total(instance, Time_Series_Electric)

#PercentageOfUse = Percentage_Of_Use(Time_Series) # Plot the percentage of use 
#Energy_Flow = Energy_Flow(Time_Series) # Plot the quantity of energy of each technology analized
#Energy_Participation = Energy_Participation(Energy_Flow)
#LDR(Time_Series)


# Calculation of the Levelized cost of energy
LCOE = round(Levelized_Cost_Of_Energy(Time_Series_Electric, Size_variables, instance),2)

# messages
#print 'Net present cost of the project is ' + str(round((instance.Final_NPC()/1000000),2)) + ' millions of USD' # Print net present cost of the project 

