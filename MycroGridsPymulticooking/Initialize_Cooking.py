#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 10:53:56 2019

@author: giorgio
"""

import pandas as pd

def Initialize_years(model, i):
    
    '''
    Not sure if I need to inizialize years since it is already initialized in the Thermal section
    
    '''
    return i

Cooking_Demand = pd.read_excel('Example/Cooking_Demand.xlsx')  #open cooking demand file 

def Initialize_Cooking_Demand(model, i, t ):
    
    '''
    This function returns the value of the cooking energy demand from a system for each period of analysis from a excel file.
    
    :param model: Pyomo model as defined in the Model_Creation script.
        
    :return: The cooking energy demand for the period t. 
    '''
    
    return float(Cooking_Demand[i][t])

PV_Energy = pd.read_excel('Example/PV_Energy.xlsx') # open the PV energy yield file

def Initialize_PV_Energy(model, i, t):
    '''
    NOT SURE IF THIS IS NEEDED ! ! !
    
    This function returns the value of the energy yield by one PV under the characteristics of the system 
    analysis for each period of analysis from a excel file.
    
    :param model: Pyomo model as defined in the Model_Creation script.
    
    :return: The energy yield of one PV for the period t.
    '''
    return float(PV_Energy[i][t])   

def Marginal_Cost_NG_Stove_1(model):
    '''
    This function computes the NG needed for every W of power output from a NG Stove
    '''
    return model.NG_Cost/(model.Low_Heating_Value*model.NG_Stove_Efficiency)

def Start_Cost_NG_Stove(model):
    '''
    This function computes start cost of a NG stove --- ASK FOR BETTER EXPLANATION OF START COST
    '''
    return model.Marginal_Cost_NG_Stove_1*model.NG_Stove_Nominal_Capacity*model.Cost_Increase

def Marginal_Cost_NG_Stove(model):
    
    return (model.Marginal_Cost_NG_Stove_1*model.NG_Stove_Nominal_Capacity-model.Start_Cost_NG_Stove)/model.NG_Stove_Nominal_Capacity
 