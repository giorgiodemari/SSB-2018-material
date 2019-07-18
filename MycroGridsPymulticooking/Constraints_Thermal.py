# -*- coding: utf-8 -*-
"""
Created on Wed Mar  7 16:41:38 2018

@author: pisto

check u.o.f. and variable existence in every comment
"""

# Thermal Model 
# Objective funtion
import numpy as np

def Net_Present_Cost(model): # OBJETIVE FUNTION: MINIMIZE THE NPC FOR THE SISTEM
    '''
    This function computes the sum of the multiplication of the net 
    present cost NPC (USD) of each scenario and their probability of 
    occurrence.
    UOF:
    VAR:
    :param model: Pyomo model as defined in the Model_creation 
    library
    '''
      
    return (sum(model.Scenario_Net_Present_Cost[i]*model.Scenario_Weight[i] for i in model.scenario ))

def NPC_Final(model):
    '''
    This function is only a repetition of the above one in order to 
    create a variable with NPC value for results'output needs
    '''
    return model.Final_NPC == (sum(model.Scenario_Net_Present_Cost[i]*model.Scenario_Weight[i] for i in model.scenario ))
     

######################### PV constraints ###########################
''' 
NO NEED TO MODIFY
'''
#1
def Solar_Energy(model,i,t): # Energy output of the solar panels
    '''
    This constraint calculates the energy produce by the solar 
    panels taking in account the efficiency of the inverter for each 
    scenario [Wh]
    UOM:ok
    VAR:ok
    :param model: Pyomo model as defined in the Model_creation 
    library
    '''
    return model.Total_Energy_PV[i,t] == model.PV_Energy_Production[i,t]*model.Inverter_Efficiency*model.PV_Units*model.Delta_Time
#2
def PV_Division(model,i,t): #division of Tot PV output contributions
    '''
    This constraint divides pv output into two different outputs 
    respectively going to cooking demand and el. demand [Wh]
    extra check to make sure we consider the right amount of energy
    input from the PV panels
    UOM:ok
    VAR:ok
    :param model: Pyomo model as defined in the Model_creation 
    library
    '''    
    return model.Total_Energy_PV[i,t] == model.Energy_PV[i,t] + model.Energy_PV_Cooking[i,t] + model.Energy_Battery_Flow_In[i,t]
#3
def PV_Installed(model,i): #Installed power of pv panels
    '''
    This constraint is used in the output phase directly. It
    computes the total installed power producing capacity of the
    PV solar panels. [W]
    UOM:ok
    VAR:ok
    :param model: Pyomo model as defined in the model_Creation 
    library
    '''
    return model.Installed_Power_PV[i] == (sum(model.PV_Units*model.PV_Nominal_Capacity*model.Scenario_Weight[i] for i in model.scenario))


################################# SC constraints ###################
#4
def Solar_Thermal_Energy (model,i,c,t): # Energy output of solar collectors

    '''
    This constraint calculates the energy produced by the solar 
    collectors for each scenario considering all the users for each 
    class (indicated by the parameter "c") [Wh]
    UOM:
    VAR:
    :param model: Pyomo model as defined in the Model_creation
    library.
    '''
    return model.Total_Energy_SC [i,c,t] == model.SC_Energy_Production[i,c,t]*model.SC_Units[c]*model.Delta_Time


############################## Battery constraints #################

#5
def State_of_Charge(model, i, t): # State of Charge of the battery
    '''
    This constraint calculates the State of charge of the battery 
    (State_Of_Charge) for each period of analysis. The 
    State_Of_Charge in the period 't' is equal to the 
    State_Of_Charge in period 't-1' plus the energy flow into the 
    battery, minus the energy flow out of the battery (flow OUT of 
    the battery is kept separated:
    -model.Energy_Battery_Flow_Out : Energy flow for electric and 
        thermal demand
    -model.Energy_Battery_Flow_Out_Cooking : Energy flow for cooking 
        purposes only ). 
    This is done for each scenario i.
    In time t=1 the State_Of_Charge_Battery is equal to a fully 
    charged battery.
    UOM:ok
    VAR:ok
    :param model: Pyomo model as defined in the Model_creation 
    library.
    '''
    if t==1: # The state of charge (State_Of_Charge) at t=0 is fully charged
        return model.State_Of_Charge_Battery[i,t] == model.Battery_Nominal_Capacity*1 + (model.Energy_Battery_Flow_In[i,t]*model.Charge_Battery_Efficiency - (model.Energy_Battery_Flow_Out[i,t] + model.Energy_Battery_Flow_Out_Cooking[i,t])/model.Discharge_Battery_Efficiency)
    if t>1:  
        return model.State_Of_Charge_Battery[i,t] == model.State_Of_Charge_Battery[i,t-1] + (model.Energy_Battery_Flow_In[i,t]*model.Charge_Battery_Efficiency - (model.Energy_Battery_Flow_Out[i,t] + model.Energy_Battery_Flow_Out_Cooking[i,t])/model.Discharge_Battery_Efficiency) 
#6
def Maximun_Charge(model, i, t): # Maximun state of charge of the Battery
    '''
    This constraint keeps the state of charge of the battery equal 
    or under the size of the battery for each scenario i.
    UOM:ok
    VAR:ok
    :param model: Pyomo model as defined in the Model_creation
    library.
    '''
    return model.State_Of_Charge_Battery[i,t] <= model.Battery_Nominal_Capacity
#7
def Minimun_Charge(model,i, t): # Minimun state of charge
    '''
    This constraint maintains the level of charge of the battery 
    above the deep of discharge in each scenario i.
    UOM:ok
    VAR:ok
    :param model: Pyomo model as defined in the Model_creation 
    library.
    '''
    return model.State_Of_Charge_Battery[i,t] >= model.Battery_Nominal_Capacity*model.Deep_of_Discharge
#8
def Max_Power_Battery_Charge(model): 
    '''
    This constraint calculates the Maximum power of charge of the 
    battery. Taking in account the capacity of the battery and a 
    time frame in which the battery has to be fully loaded for each 
    scenario.
    UOM:ok
    VAR:ok !!! dovrebbe essere minimum charge time nella divisione
    :param model: Pyomo model as defined in the Model_creation 
    library.
    '''
    return model.Maximun_Charge_Power== model.Battery_Nominal_Capacity/model.Maximun_Battery_Charge_Time
#9
def Max_Power_Battery_Discharge(model):
    '''
    This constraint calculates the Maximum power of discharge of the 
    battery. For each scenario i.
    UOM:ok
    VAR:ok
    :param model: Pyomo model as defined in the Model_creation
    library.
    '''
    return model.Maximun_Discharge_Power == model.Battery_Nominal_Capacity/model.Maximun_Battery_Discharge_Time
#10
def Max_Bat_in(model, i, t): #Maximum flow of energy for the charge phase
    '''
    This constraint maintains the energy in to the battery, below 
    the maximum power of charge of the battery for each scenario i.
    
    THINK CHARGE POWER IS INSTEAD CHARGE ENERGY GIVEN IN THE DELTA
    TIME PERIOD! - this way it should all make sense
    
    :param model: Pyomo model as defined in the Model_creation
    library.
    '''
    return model.Energy_Battery_Flow_In[i,t]/model.Delta_Time <= model.Maximun_Charge_Power
#11
def Max_Bat_out(model,i,c,t): #Maximum flow of energy for the discharge phase
    '''
    This constraint maintains the energy from the battery, below the 
    maximum power of discharge of the battery for each scenario i.
    Modified to account for cooking component too.
    UOM:ok
    VAR:ok
    :param model: Pyomo model as defined in the Model_creation 
    library.
    '''
    return (model.Energy_Battery_Flow_Out[i,t] + model.Energy_Battery_Flow_Out_Cooking[i,t])/model.Delta_Time <= model.Maximun_Discharge_Power
#12
def Total_Bat_Out(model,i,t): #total flow out of batt
    '''
    This constraint is applied only to create a easier variable 
    to deal with in the data frame for output phase
    UOM:ok
    VAR:ok
    :param model: Pyomo model as defined in the Model_Creation
    library.
    '''
    return model.Total_Battery_Flow_Out[i,t] == model.Energy_Battery_Flow_Out_Cooking[i,t] + model.Energy_Battery_Flow_Out[i,t]
########################### TANK constraints #######################
#13
def State_Of_Charge_Tank (model,i,c,t): # State of Charge (SOC) of the thermal storage (Tank)
    '''
    This constraint calculates the state of charge of the thermal 
    storage tank for each period of analysis and for each class of 
    users. It is an energy balance on the hot water storage tank 
    unit in each period. The SOC_Tank in the period 't' is equal to 
    the SOC_Tank in the period 't-1' plus the energy flow into the 
    tank, minus the energy flow out of the tank, plus the 
    resistance heat, curtailment and losses. This is done for each 
    class c and scenario i. In time t=1 the SOC_Tank is equal to a 
    ully charged tank.
    UOM:
    VAR:
    :param model: Pyomo model as defined in the Model_creation 
    library.
     '''
    if t==1: # SOC_Tank  for the period 0 is equal to the Tank size.
        return model.SOC_Tank[i,c,t] == model.Tank_Nominal_Capacity[c]*1 + model.Total_Energy_SC [i,c,t] + model.Resistance_Thermal_Energy [i,c,t]*model.Electric_Resistance_Efficiency - model.Energy_Tank_Flow_Out[i,c,t] 

    if t>1:  
        return model.SOC_Tank [i,c,t] == model.SOC_Tank[i,c,t-1]*model.Tank_Efficiency + model.Total_Energy_SC [i,c,t] + model.Resistance_Thermal_Energy [i,c,t]*model.Electric_Resistance_Efficiency - model.Energy_Tank_Flow_Out[i,c,t] 
#14
def Maximun_Tank_Charge(model,i,c,t): # Maximun state of charge of the Tank in terms of thermal energy
    '''
    This constraint keeps the state of charge of the tank equal or 
    under the size of the tank for each scenario i and each class c.
    UOM:
    VAR:
    :param model: Pyomo model as defined in the Model_creation 
    library.    
    '''
    return model.SOC_Tank[i,c,t] <= model.Tank_Nominal_Capacity[c]
#15
def Minimun_Tank_Charge(model,i,c,t): # Minimun state of charge
    '''
    This constraint maintains the level of charge of the tank above 
    the deep of discharge in each scenario i.
    UOM:
    VAR:
    :param model: Pyomo model as defined in the Model_creation
    library.
    '''
    return model.SOC_Tank [i,c,t] >= model.Tank_Nominal_Capacity[c]*model.Deep_of_Tank_Discharge
#16
def Max_Power_Tank_Discharge(model,c):
    '''
    This constraint calculates the Maximum power of discharge of the 
    battery for each scenario i.
    UOM:
    VAR:
    :param model: Pyomo model as defined in the Model_creation 
    library.
    '''
    return model.Maximun_Tank_Discharge_Power[c] == model.Tank_Nominal_Capacity[c]/(model.Maximun_Tank_Discharge_Time)
#17
def Max_Tank_out(model,i,c, t): #minimun flow of energy for the discharge fase
    '''
    This constraint maintains the energy from the battery, below the 
    maximum power of discharge of the battery for each scenario i.
    UOM:
    VAR:
    :param model: Pyomo model as defined in the Model_creation 
    library.
    '''
    return model.Energy_Tank_Flow_Out[i,c,t]/model.Delta_Time <= model.Maximun_Tank_Discharge_Power[c]


#################### Electrical Resistance ########################
#18
def Maximum_Resistance_Thermal_Energy (model,i,c,t):
    '''
    This constraint calculates the maximum thermal energy produced 
    by the electrical resistance for each scenario i and class c.
    UOM:
    VAR:
    :param model: Pyomo model as defined in the Model_creation 
    library.
    '''
    return model.Resistance_Thermal_Energy[i,c,t]/model.Delta_Time <= model.Nominal_Power_Resistance[c] #*model.Resistance_Units[c]


######################### Boiler constraints #######################

#19
def Maximum_Boiler_Energy(model,i,c,t): # Maximun energy output of the Boiler    
    '''
    This constraint ensures that the boiler will not exceed his 
    nominal capacity in each period in each scenario i and class c.
    UOM:
    VAR:
    :param model: Pyomo model as defined in the Model_creation 
    library.
    '''
    return model.Boiler_Energy[i,c,t] <= model.Boiler_Nominal_Capacity[c]

#20
def NG_Consumption(model,i,c,t): # NG comsuption 
    '''
    This constraint transforms the energy produced by the boiler 
    generator into kg of natural gas in each scenario i and class c.
    This is done using the lower heating value (LHV)
    of the natural gas and the efficiency of the boiler.
    since the NG consumption for thermal needs is divided into 
    classes we need to add another constraint 
    (NG_Consumption_Cooking) which accounts for NG consumed cooking 
    purposes for exclusively.
    UOM:
    VAR:
    :param model: Pyomo model as defined in the Model_Creation 
    library.
    '''
    return model.NG_Consume[i,c,t] == model.Boiler_Energy[i,c,t]/(model.Boiler_Efficiency*(model.Low_Heating_Value_NG))

#stessa formula ma girata rispetto a NG_Energy_Cooking
#def NG_Consumption_Cooking(model,i,c,t): # NG consumption related to cooking demand
#    '''
#    This constraint computes kg of NG used for cooking purposes 
#    starting from cooking energy demand in each scenario i and time 
#    period t. In a similar manner to the above constraint this is 
#    done using LHV of the natural gas and efficiency of the NG 
#    cooking stoves.
#    
#    :param model: Pyomo model as defined in the Model_Creation 
#    library.
#    '''
#    return model.NG_Consume_Cooking[i,c,t] == model.NG_Energy_Cooking[i,c,t]/(model.NG_Stove_Efficiency*(model.Low_Heating_Value_NG/model.Delta_Time))


################ ENERGY BALANCES FOR NG / EL STOVES ################
'''
In this section I will put two GLOBAL constraints: one on power and 
one on number of stoves. These two will surely be correlated by the 
decision of the type of to be installed stoves but I still want to 
make sure there is a minimum number of stoves even if their total 
power satisfies cooking energy demand a maximum energy constraint is 
also established in order to not overload the electric stoves with 
energy coming from batteries or generator.
'''
#   21 
def Maximum_Energy_El_Stove(model,i,t): # Maximum Energy to each electric stove
    '''
    This constraint ensures that energy flow to cooking stoves stays
    below their nominal capacity. I have considered both energy from 
    the battery and from the Diesel Generator in case both these 
    contributions need to be used. This generated another constraint 
    - modify generator constraint so that:
        nominalPWR(El. cooking stoves)>=energy produced by generator 
        for gen purposes + energy by generator for cooking only.
    UOM:ok
    VAR:ok
    :param model: Pyomo model as defined in the Model_Creation 
    library.
    '''
    return model.El_Stove_Nominal_Power * model.El_Stove_Units >= (model.Energy_Battery_Flow_Out_Cooking[i,t]*model.Discharge_Battery_Efficiency + model.Generator_Energy_Cooking[i,t] + model.Energy_PV_Cooking[i,t])/model.Delta_Time



#22
def Energy_Cooking_Balance(model,i,t): #balance between actual energy input to stoves and energy demand
    '''
    This constraint ensures that actual energy input to both stoves 
    (electric+NG) meets minimum energy cooking demand requirements.
    UOM:ok
    VAR:ok
    :param model: Pyomo model as defined in the Model_Creation 
    library.
    '''
    return model.Energy_Demand_Cooking[i,t] ==  model.NG_Energy_Cooking[i,t] + model.El_Energy_Cooking[i,t] 

#23
def Limit_NG_Cooking_Demand(model,i,t):
    '''
    This constraint ensures that the NG demand which varies in time 
    is never more than the installed NG cooking power
    UOM:ok
    VAR:ok
    :param model: Pyomo model as defined in the Model_Creation 
    library.
    '''
    return model.NG_Energy_Cooking[i,t] <= model.NG_Stove_Nominal_Power*model.NG_Stove_Units*model.Delta_Time
#24
def Limit_El_Cooking_Demand(model,i,t):
    '''
    This constraint ensures the El cooking demand is not higher than
    installed el cooking power
    UOM:ok
    VAR:ok
    :param model: Pyomo model as defined in the Model_Creation
    library.
    '''
    return model.El_Energy_Cooking[i,t] <= model.El_Stove_Nominal_Power*model.El_Stove_Units*model.Delta_Time
#25
def El_Energy_Cooking_Balance(model,i,t): #global balance of the power output of electric stoves 
    '''
    This equals energy from generator (cooking) and battery to 
    electric stoves to a new variable called El_Energy_Cooking = 
    actual el cooking output from electric stoves.
    UOM:ok
    VAR:ok
    :param model: Pyomo model as defined in the Model_Creation
    library.
    '''
    return model.El_Energy_Cooking[i,t] == (model.Energy_PV_Cooking[i,t] + (model.Generator_Energy_Cooking[i,t] + model.Energy_Battery_Flow_Out_Cooking[i,t]*model.Discharge_Battery_Efficiency))*model.El_Stove_Efficiency
#26
def NG_Energy_Cooking_Balance(model,i,t): #global balance of the power output of NG stoves
    '''
    This constraint computes actual energy output from all NG stoves
    starting from NG used and its LHV
    UOM:CHECK LHV udm
    VAR:ok
    :param model: Pyomo model as defined in the Model_Creation
    library.
    '''
    return model.NG_Energy_Cooking[i,t] == model.NG_Consume_Cooking[i,t]*model.Low_Heating_Value_NG*model.NG_Stove_Efficiency
#27
def Installed_Power_Balance_Cooking(model,i): # INSTALLED POWER BALANCE (installed cooking power)
    '''
    This constraint ensures the total installed power (electric + NG 
    stove) satisfies the maximum cooking energy demand.
    UOM:ok
    VAR:ok
    :param model: Pyomo model as defined in the Model_creation 
    library.
    '''
    return max(sum(model.Energy_Demand_Cooking[i,t]*model.Scenario_Weight[i] for i in model.scenario) for t in range (1,model.Periods+1)) >= (model.NG_Stove_Units*model.NG_Stove_Nominal_Power + model.El_Stove_Units*model.El_Stove_Nominal_Power)*model.Delta_Time
#28
def NG_Total_Consumption(model,i,t): #total NG consumed in every time period t
    '''
    computes sum of NG consumed for thermal and cooking purposes for
    semplification of output phase
    UOM:ok
    VAR:ok
    :param model: Pyomo model as defined in the Model_Creation
    library.
    '''
    return model.NG_Consumption_Total[i,t] == model.NG_Consume_Cooking[i,t]+ sum(model.NG_Consume[i,c,t] for c in model.classes)

def NG_Consumption_Thermal(model,i,t):
    '''
    computes total NG consumed for thermal use exclusively in each
    period t
    '''
    return model.NG_Consume_Thermal[i,t] == sum(model.NG_Consume[i,c,t] for c in model.classes)

######################### Energy Constraints #######################

#29
def Total_Thermal_Energy_Demand(model, i, c, t):
    ''' 
    This constraint calculates the thermal energy demand for all the 
    users in each classs c and for each scenario i. 
    UOM:
    VAR:
    :param model: Pyomo model as defined in the Model_creation 
    library.
    '''
    return model.Total_Thermal_Energy_Demand[i,c,t] == (model.Thermal_Energy_Demand[i,c,t]*model.Users_Number_Class[c])
#30
def Thermal_Energy_Balance(model,i,c,t): # Thermal energy balance
    '''
    This costraint ensures the perfect match between the energy 
    demand of the system and the different sources to meet the 
    thermal energy demand for each class c and each scenario i
    UOM:
    VAR:
    :param model: Pyomo model as defined in the Model_creation 
    library.
    '''
    return  model.Total_Thermal_Energy_Demand[i,c,t] == model.Boiler_Energy[i,c,t]  + model.Energy_Tank_Flow_Out[i,c,t] - model.Thermal_Energy_Curtailment[i,c,t] + model.Lost_Load_Th[i,c,t]
#31
def Total_Electrical_Resistance_Demand (model,i,t): # The summation of the electrical resistance demand of each class. 
    '''
    This constraint defines the electrical demand that comes from 
    the electrical resistance to satisfy the thermal demand. 
    This term is involved in the electrical energy balance.
    UOM:
    VAR:
    :param model: Pyomo model as defined in the Model_creation 
    library.
    '''
    return model.Total_Electrical_Resistance_Demand[i,t] == sum(model.Resistance_Thermal_Energy[i,c,t] for c in model.classes)
#32
def Energy_balance(model, i, t): # Energy balance
    '''
    This constraint ensures the perfect match between the energy 
    demand of the system and the differents sources to meet the 
    energy demand including the electric resistance demand of 
    thermal part each scenario i.
    UOM:
    VAR:
    :param model: Pyomo model as defined in the Model_creation 
    library.
    '''
    return model.Energy_Demand[i,t] == model.Energy_PV[i,t] + model.Generator_Energy[i,t] + model.Energy_Battery_Flow_Out[i,t]*model.Discharge_Battery_Efficiency*model.Inverter_Efficiency + model.Lost_Load[i,t] - model.Energy_Curtailment[i,t] - model.Total_Electrical_Resistance_Demand[i,t] 
#33
def Maximun_Lost_Load(model,i): # Maximum permissible lost load
    '''
    This constraint ensures that the ratio between the lost load and 
    the energy demand does not exceeds the value of the permisible 
    lost load each scenario i. 
    UOM:ok
    VAR:ok
    :param model: Pyomo model as defined in the Model_creation 
    library.
    '''
    return model.Lost_Load_Probability >= (sum(model.Lost_Load[i,t] for t in model.periods)/sum(model.Energy_Demand[i,t] for t in model.periods))
#33
def Maximun_Lost_Load_Th(model,i,c): # Maximum permissible lost load thermal
    '''
    This constraint ensures that the ratio between the lost load and 
    the energy Demand does not exceeds the value of the permisible 
    lost load each scenario i and class c. 
    UOM:ok
    VAR:ok
    :param model: Pyomo model as defined in the Model_Creation 
    library.
    '''
    return model.Lost_Load_Probability*sum(model.Total_Thermal_Energy_Demand[i,c,t] for t in model.periods) >= sum(model.Lost_Load_Th[i,c,t] for t in model.periods)

#def Maximum_Lost_Load_Cooking(model,i): #Maximum permissible lost load for cooking demand
#    '''
#    This constraint ensures that the ratio between the lost load and 
#    the cooking energy demand does not exceed the value of the 
#    permissible load in each scenario i (should I add class?).
#    
#    :param model: Pyomo model as defined in the Model_creation
#    library.
#    '''
#    return model.Lost_Load_Probability_Cooking >= sum(model.Lost_Load_Cooking[i,t] for t in model.periods)/sum(model.Energy_Demand_Cooking[i,t] for t in model.periods)

#def Renewable_Penetration(model):
#    '''
#    This constraint computes the fraction of renewable energy source
#    based technologies with respect to the total installed power in 
#    the plant
#    UOM:ok
#    VAR:ok
#    :param model: Pyomo model as defined in the Model_Creation
#    library.
#    '''
#    return model.Installed_Renewable_Penetration == (model.PV_Units*model.PV_Nominal_Capacity) / (model.PV_Units*model.PV_Nominal_Capacity + model.Generator_Nominal_Capacity)

#def Stress_Condition_Renewable_Penetration(model):
#    '''
#    This constraint calculates how much of the power comes from 
#    renewable sources in times when the total energy demand is 
#    highest
#    UOM:
#    VAR:
#    :param model: Pyomo model as defined in the Model_Creation
#    library.
#    '''
#    for i in model.scenario:
#        for t in model.periods:
#            model.Overall_Demand[i,t] = model.Energy_Demand_Cooking[i,t] + sum(model.Thermal_Energy_Demand[i,c,t] for c in model.classes) + model.Energy_Demand[i,t]       
#    
#    index_max=np.argmax(model.Overall_Demand[i,t])
#    
#    return model.Stress_Renewable_Penetration == sum((model.Delta_Time*model.Energy_Battery_Flow_Out[i,index_max]+model.Delta_Time*model.Energy_Battery_Flow_Out_Cooking[i,index_max] + model.Energy_PV[i,index_max] + model.Energy_PV_Cooking[i,index_max])*model.Scenario_Weight[i] for i in model.scenario)/model.Overall_Demand[index_max]
#
#def Cooking_Renewable_Penetration_Period(model,i,t): 
#    '''
#    This model calculates the level of renewable penetration for the 
#    cooking section of the grid period by period
#    UOM:ok
#    VAR:ok
#    :param model: Pyomo model as defined in the Model_Creation
#    library.
#    '''
#    for i in model.scenario:
#        for t in model.periods:
#            if model.Energy_Demand_Cooking[i,t] == 0:
#                model.Renewable_Penetration_Cooking_Computation[i,t] == 0
#            else:
#                model.Renewable_Penetration_Cooking_Computation[i,t] == (model.Energy_Battery_Flow_Out_Cooking[i,t] + model.Energy_PV_Cooking[i,t]/model.Energy_Demand_Cooking[i,t])*100
#
#    return model.Renewable_Penetration_Cooking_Period[i,t] == model.Renewable_Penetration_Cooking_Computation[i,t]

############## Diesel generator constraints ########################
#34
def Maximun_Diesel_Energy(model,i, t): # Maximun energy output of the diesel generator
    '''
    This constraint ensures that the generator will not exceed his 
    nominal capacity in each period in each scenario i.
    It has been modified to account for energy produced for cooking 
    purposes only.
    WHY NOT model.Generator_Nominal_Capacity*model.Generator_Units?-
    that's because a gnerator units parameter is never defined
    we work with a hypothetical non-discretized modular generator
    as a result the capacity can be any value!
    UOM:
    VAR:ok
    :param model: Pyomo model as defined in the Model_creation 
    library.
    '''
    return model.Generator_Energy[i,t] + model.Generator_Energy_Cooking[i,t] <= model.Generator_Nominal_Capacity
#35
def Diesel_Comsuption(model,i, t): # Diesel comsuption 
    '''
    This constraint transforms the energy produce by the diesel 
    generator in to liters of diesel in each scenario i.This is done 
    using the low heating value of the diesel and the efficiency of 
    the diesel generator. Same modification as above to account for 
    consumption by Diesel Generator for producing cooking energy.
    UOM:!!! check for LHV 
    VAR:
    :param model: Pyomo model as defined in the Model_creation 
    library.
    '''
    return model.Diesel_Consume[i,t] == model.Generator_Energy[i,t]/(model.Generator_Efficiency*(model.Low_Heating_Value)) + model.Generator_Energy_Cooking[i,t]/(model.Generator_Efficiency*(model.Low_Heating_Value))                                                                                                                              
#36
def Diesel_Consume_Cooking(model,i,t):
    
    return model.Diesel_Consumption_Cooking[i,t] == model.Generator_Energy_Cooking[i,t]/(model.Generator_Efficiency*(model.Low_Heating_Value))

######################### Economical Constraints ##################
    
def SC_Financial_Cost(model):
   '''
   This constraint defines the financial cost of the solar collector 
   technology as the summation of each class that will be considered 
   in the Financial Cost. In this way all costs of each class will 
   be considered.
   :param model: Pyomo model as defined in the Model_creation 
   library.
   '''
   return model.SC_Financial_Cost == sum(model.SC_Units[c]*model.SC_investment_Cost*model.SC_Nominal_Capacity for c in model.classes)

def Tank_Financial_Cost (model):
   '''
   This constraint defines the financial cost of the tank technology 
   as the summation of each class that will be considered in the 
   Financial Cost.In this way all costs of each class will be
   considered.
   :param model: Pyomo model as defined in the Model_creation 
   library.
   '''
   return model.Tank_Financial_Cost == sum(model.Tank_Nominal_Capacity[c]*model.Tank_Invesment_Cost*model.Delta_Time for c in model.classes)

def Boiler_Financial_Cost (model):
   ''' 
   This constraint defines the financial cost of the boiler 
   technology as the summation of each class that will be considered 
   in the Financial Cost. In this way all costs of each class will 
   be considered.
   :param model: Pyomo model as defined in the Model_creation 
   library.
   '''
   return model.Boiler_Financial_Cost == sum(model.Boiler_Nominal_Capacity[c]*model.Boiler_Invesment_Cost for c in model.classes)

def Resistance_Financial_Cost (model):
   ''' 
   This constraint defines the financial cost of the resistance 
   technology as the summation of each class that will be considered 
   in the Financial Cost. In this way all costs of each class will 
   be considered.
   :param model: Pyomo model as defined in the Model_creation 
   library.
   '''
   return model.Resistance_Financial_Cost == sum(model.Nominal_Power_Resistance[c]*model.Resistance_Invesment_Cost for c in model.classes)

def Financial_Cost(model): 
    '''
    This constraint calculates the yearly payment for the borrow 
    money.
    
    :param model: Pyomo model as defined in the Model_creation 
    library.
    '''
    return model.Cost_Financial == ((model.PV_Units*model.PV_invesment_Cost*model.PV_Nominal_Capacity + model.Battery_Nominal_Capacity*model.Battery_Invesment_Cost*model.Delta_Time + model.Generator_Nominal_Capacity*model.Generator_Invesment_Cost + model.SC_Financial_Cost + model.Tank_Financial_Cost + model.Boiler_Financial_Cost + model.Resistance_Financial_Cost)*model.Porcentage_Funded*model.Interest_Rate_Loan)/(1-((1+model.Interest_Rate_Loan)**(-model.Years)))

def Diesel_Cost_Total(model,i):
    '''
    This constraint calculates the total cost due to the use of 
    diesel to generate electricity in the generator in each scenario 
    i. The Diesel consume as defined above accounts for all diesel 
    consumption terms (cooking and general purposes)
    
    :param model: Pyomo model as defined in the Model_creation 
    library.
    '''    
    foo=[]
    for f in range(1,model.Periods+1):
        foo.append((i,f))
    return model.Diesel_Cost_Total[i] == sum(((sum(model.Diesel_Consume[i,t]*model.Diesel_Unitary_Cost for i,t in foo))/((1+model.Discount_Rate)**model.Project_Years[y])) for y in model.years) 
    
def NG_Cost_Total (model,i):
    '''
    This constraint calculates the total cost due to the use of 
    Natural Gas to generate thermal energy in the boiler in each 
    scenario i. 
    
    :param model: Pyomo model as defined in the Model_creation 
    library.
    '''    
    foo=[] 
    for c in range (1,model.Classes+1): 
        for f in range(1,model.Periods+1):
            foo.append((i,c,f))
    goo=[]
    for g in range(1,model.Periods+1):
        goo.append((i,g))
    return  model.NG_Cost_Total[i] == sum((((sum(model.NG_Consume[i,c,t] for i,c,t in foo) + sum(model.NG_Consume_Cooking[i,t] for i,t in goo))*model.NG_Unitary_Cost)/((1+model.Discount_Rate)**model.Project_Years[y])) for y in model.years)

def Total_Cost_Fuel(model):
    '''
    This constraint is made to compute a value that will be used in 
    output directly: the total cost of both fuels accounted in every
    scenario mean.
    '''
    return model.Total_Fuel_Cost == sum (model.NG_Cost_Total[i]*model.Scenario_Weight[i] +model.Diesel_Cost_Total[i]*model.Scenario_Weight[i] for i in model.scenario)

def Scenario_Lost_Load_Cost(model, i):
    '''
    This constraint calculates the cost due to the lost load in each 
    scenario i. 
    
    :param model: Pyomo model as defined in the Model_creation 
    library.
    '''
    foo=[]
    for f in range(1,model.Periods+1):
        foo.append((i,f))
        
    return  model.Scenario_Lost_Load_Cost[i] == sum(((sum(model.Lost_Load[i,t]*model.Value_Of_Lost_Load*model.Delta_Time for i,t in foo))/((1+model.Discount_Rate)**model.Project_Years[y])) for y in model.years)  

def Scenario_Lost_Load_Cost_Th (model,i):
    '''
    This constraint calculates the total cost due to the use of 
    Natural Gas to generate thermal energy in the boiler in each 
    scenario i. 
    
    :param model: Pyomo model as defined in the Model_creation 
    library.
    '''    
    foo=[] 
    for c in range (1,model.Classes+1): 
        for f in range(1,model.Periods+1):
            foo.append((i,c,f))
    return  model.Scenario_Lost_Load_Cost_Th[i] == sum(((sum(model.Lost_Load_Th[i,c,t]*model.Value_Of_Lost_Load for i,c,t in foo))/((1+model.Discount_Rate)**model.Project_Years[y])) for y in model.years) 
 
#def Scenario_Lost_Load_Cost_Cooking (model,i):
#    '''
#    This constraint computes the total cost due to the loss of 
#    demand requirements in the cooking sector for each scenario i.
#    
#    :param model: Pyomo model as defined in Model_Creation library.
#    '''
#    foo=[]
#    for f in range(1,model.Periods+1):
#        foo.append((i,f))
#    return model.Scenario_Lost_Load_Cost_Cooking[i] == sum(((sum(model.Lost_Load_Cooking[i,t]*model.Value_Of_Lost_Load_Cooking*model.Delta_Time for i,t in foo))/((1+model.Discount_Rate)**model.Project_Years[y])) for y in model.years)
   
def Initial_Inversion(model):
    '''
    This constraint calculates the initial investment for the system.
    The total investment cost is multiplied times (1-funded%), the 
    constraint computes the initial investment to be sustained by 
    the inhabitants exclusively, not the real total cost of the 
    project.
    
    :param model: Pyomo model as defined in the Model_creation 
    library.
    '''    
    return model.Initial_Inversion == (model.PV_Units*model.PV_invesment_Cost*model.PV_Nominal_Capacity + model.Battery_Nominal_Capacity*model.Battery_Invesment_Cost*model.Delta_Time + model.Generator_Nominal_Capacity*model.Generator_Invesment_Cost + model.SC_Financial_Cost + model.Tank_Financial_Cost + model.Boiler_Financial_Cost + model.Resistance_Financial_Cost + model.El_Stove_Investment_Cost*model.El_Stove_Units + model.NG_Stove_Investment_Cost*model.NG_Stove_Units)*(1-model.Porcentage_Funded) 

def Operation_Maintenance_Cost(model):
    '''
    This funtion calculates the operation and maintenance for the 
    system. 
    
    :param model: Pyomo model as defined in the Model_creation
    library.
    '''    
    return model.Operation_Maintenance_Cost == sum(((model.PV_Units*model.PV_invesment_Cost*model.PV_Nominal_Capacity*model.Maintenance_Operation_Cost_PV + model.Battery_Nominal_Capacity*model.Battery_Invesment_Cost*model.Delta_Time*model.Maintenance_Operation_Cost_Battery + model.Generator_Nominal_Capacity*model.Generator_Invesment_Cost*model.Maintenance_Operation_Cost_Generator + model.SC_Financial_Cost*model.Maintenance_Operation_Cost_SC + model.Tank_Financial_Cost*model.Maintenance_Operation_Cost_Tank + model.Boiler_Financial_Cost*model.Maintenance_Operation_Cost_Boiler + model.Resistance_Financial_Cost*model.Maintenance_Operation_Cost_Resistance + model.El_Stove_Investment_Cost*model.Maintenance_Operation_Cost_El_Stove*model.El_Stove_Units + model.NG_Stove_Investment_Cost*model.Maintenance_Operation_Cost_NG_Stove*model.NG_Stove_Units)/((1+model.Discount_Rate)**model.Project_Years[y])) for y in model.years) 

def Total_Finalcial_Cost(model):
    '''
    This funtion calculates the total financial cost of the system. 
    
    :param model: Pyomo model as defined in the Model_creation 
    library.
    '''    
    return model.Total_Finalcial_Cost == sum((model.Cost_Financial/((1+model.Discount_Rate)**model.Project_Years[y])) for y  in model.years) 
    
def Battery_Reposition_Cost(model):
    '''
    This funtion calculates the reposition of the battery after a 
    stated time of use. 
    
    :param model: Pyomo model as defined in the Model_creation
    library.
    ''' 
    return model.Battery_Reposition_Cost == (model.Battery_Nominal_Capacity*model.Battery_Invesment_Cost*model.Delta_Time)/((1+model.Discount_Rate)**model.Battery_Reposition_Time)

def Scenario_Net_Present_Cost(model, i): 
    '''
    This function computes the Net Present Cost for the life time of 
    the project, taking in account that the cost are fix for each 
    year.
    
    :param model: Pyomo model as defined in the Model_creation 
    library.
    '''            
    return model.Scenario_Net_Present_Cost[i] == model.Initial_Inversion + model.Operation_Maintenance_Cost + model.Total_Finalcial_Cost + model.Battery_Reposition_Cost + model.Scenario_Lost_Load_Cost[i] + model.Scenario_Lost_Load_Cost_Th[i] + model.Diesel_Cost_Total[i] + model.NG_Cost_Total[i]
                