#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 17 11:31:43 2019

@author: giorgio
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 17:22:11 2019

@author: giorgio
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import matplotlib.ticker as mtick
import matplotlib.pylab as pylab

'''
This new results script is going to divide results output into 
5 different files: the first 4 will include time-dependent
output data respectively related to general aspects, electric 
section, thermal section and cooking section, the fourth will 
include non-time-dependent data
'''

def Load_results_general(instance):
    '''
    First excel data file will include general data such as SOC, 
    total Diesel consumed, total NG consumed, total 
    Batt_Flow_Out
    '''
    
#    Load the variables that depend of the periods in python 
#    dyctionarys a
    
    
    Number_Scenarios = int(instance.Scenarios.extract_values()[None])
    Number_Periods = int(instance.Periods.extract_values()[None])
    
    #Scenarios = [[] for i in range(Number_Scenarios)]
    
    columns = []
    for i in range(1, Number_Scenarios+1):
        columns.append('Scenario_'+str(i))
        
    Scenarios = pd.DataFrame()
    
    SOC = instance.State_Of_Charge_Battery.get_values()
    NG_Consumption = instance.NG_Consumption_Total.get_values()
    Diesel_Consumption = instance.Diesel_Consume.get_values()
    Total_Batt_Flow_Out = instance.Total_Battery_Flow_Out.get_values()
    Batt_Flow_In = instance.Energy_Battery_Flow_In.get_values()
    
    Scenarios_Periods = [[] for i in range(Number_Scenarios)]
    
    for i in range(0,Number_Scenarios):
        for j in range(1,Number_Periods+1):
            Scenarios_Periods[i].append((i+1,j))
    foo=0
    for i in columns:
        Information = [[] for i in range(0,5)]
        for j in Scenarios_Periods[foo]:
            Information[0].append(SOC[j])
            Information[1].append(NG_Consumption[j])
            Information[2].append(Diesel_Consumption[j])
            Information[3].append(Total_Batt_Flow_Out[j])
            Information[4].append(Batt_Flow_In[j])
            
            
        Scenarios = Scenarios.append(Information)
        foo+=1
    
    index=[]
    for j in range(1,Number_Scenarios+1):
        index.append('SOC [Wh] ' +str(j))
        index.append('NG_Consumption [kg] ' + str(j))
        index.append('Diesel_Consumption [l] ' + str(j))
        index.append('Total_Battery_Flow_Out [Wh] ' +str(j))
        index.append('Battery_Flow_In [Wh] ' +str(j))
    Scenarios.index = index
    
    # Creation of an index starting in the 'model.StartDate' value with a frequency step equal to 'model.Delta_Time'
    if instance.Delta_Time() >= 1 and type(instance.Delta_Time()) == type(1.0) : # if the step is in hours and minutes
        foo = str(instance.Delta_Time()) # trasform the number into a string
        hour = foo[0] # Extract the first character
        minutes = str(int(float(foo[1:3])*60)) # Extrac the last two character
        columns = pd.DatetimeIndex(start=instance.StartDate(), 
                                   periods=instance.Periods(), 
                                   freq=(hour + 'h'+ minutes + 'min')) # Creation of an index with a start date and a frequency
    elif instance.Delta_Time() >= 1 and type(instance.Delta_Time()) == type(1): # if the step is in hours
        columns = pd.DatetimeIndex(start=instance.StartDate(), 
                                   periods=instance.Periods(), 
                                   freq=(str(instance.Delta_Time()) + 'h')) # Creation of an index with a start date and a frequency
    else: # if the step is in minutes
        columns = pd.DatetimeIndex(start=instance.StartDate(), 
                                   periods=instance.Periods(), 
                                   freq=(str(int(instance.Delta_Time()*60)) + 'min'))# Creation of an index with a start date and a frequency
    
    Scenarios.columns = columns
    Scenarios = Scenarios.transpose()
    
    Scenarios.to_excel('Results_multi/Time_Series_General.xls') # Creating an excel file with the values of the variables that are in function of the periods
    
    S = instance.PlotScenario.value
    Time_Series_General = pd.DataFrame(index=range(0,35040))
    Time_Series_General.index = Scenarios.index
    
    Time_Series_General['State Of Charge [Wh]']          = Scenarios ['SOC [Wh] ' +str(S)]
    Time_Series_General['NG Consumed [kg]']              = Scenarios ['NG_Consumption [kg] ' +str(S)]
    Time_Series_General['Diesel Consumed [l]']           = Scenarios ['Diesel_Consumption [l] ' +str(S)]
    Time_Series_General['Battery Flow Out (total) [Wh]'] = Scenarios ['Total_Battery_Flow_Out [Wh] ' +str(S)]
    Time_Series_General['Battery Flow In [Wh]']          = Scenarios ['Battery_Flow_In [Wh] ' + str(S)]
    
    return Time_Series_General, Scenarios



def Load_results_Electric(instance):
    '''
    Second excel file containing time-dependant 
    electric-part-related data such as:
    -Electric energy demand
    -PV ENERGY
    -diesel energy (el+th)
    -Lost Load
    -Battery flow out (el+th)
    '''

    Number_Scenarios = int(instance.Scenarios.extract_values()[None])
    Number_Periods   = int(instance.Periods.extract_values()[None])
    
    columns = []
    for i in range(1, Number_Scenarios+1):
        columns.append('Scenario_'+str(i))
    
    Scenarios = pd.DataFrame()
    
    El_Demand        = instance.Energy_Demand.extract_values()
    Resistance_Demand = instance.Total_Electrical_Resistance_Demand.extract_values()
    PV_Energy        = instance.Total_Energy_PV.get_values()
    Generator_Energy = instance.Generator_Energy.get_values()
    Lost_Load        = instance.Lost_Load.get_values()
    Battery_Flow_Out = instance.Energy_Battery_Flow_Out.get_values()
    
    Scenarios_Periods = [[] for i in range(Number_Scenarios)]
    
    for i in range(0,Number_Scenarios):
        for j in range(1,Number_Periods+1):
            Scenarios_Periods[i].append((i+1,j))
    foo=0
    for i in columns:
        Information = [[] for i in range(0,6)]
        for j in Scenarios_Periods[foo]:
            Information[0].append(El_Demand[j])
            Information[1].append(Resistance_Demand[j])
            Information[2].append(PV_Energy[j])
            Information[3].append(Generator_Energy[j])
            Information[4].append(Lost_Load[j])
            Information[5].append(Battery_Flow_Out[j]) 
            
        Scenarios = Scenarios.append(Information)
        foo+=1
    
    index=[]
    for j in range(1,Number_Scenarios+1):
        index.append('El_Demand [Wh] ' + str(j))
        index.append('Res_Demand [Wh] ' +str(j))
        index.append('PV_Energy [Wh] ' + str(j))
        index.append('Generator_Energy [Wh] ' + str(j))
        index.append('Lost_Load [Wh] ' + str(j))
        index.append('Battery_Flow_Out [Wh] ' +str(j))
    Scenarios.index = index
    
    # Creation of an index starting in the 'model.StartDate' value with a frequency step equal to 'model.Delta_Time'
    if instance.Delta_Time() >= 1 and type(instance.Delta_Time()) == type(1.0) : # if the step is in hours and minutes
        foo = str(instance.Delta_Time()) # trasform the number into a string
        hour = foo[0] # Extract the first character
        minutes = str(int(float(foo[1:3])*60)) # Extrac the last two character
        columns = pd.DatetimeIndex(start=instance.StartDate(), 
                                   periods=instance.Periods(), 
                                   freq=(hour + 'h'+ minutes + 'min')) # Creation of an index with a start date and a frequency
    elif instance.Delta_Time() >= 1 and type(instance.Delta_Time()) == type(1): # if the step is in hours
        columns = pd.DatetimeIndex(start=instance.StartDate(), 
                                   periods=instance.Periods(), 
                                   freq=(str(instance.Delta_Time()) + 'h')) # Creation of an index with a start date and a frequency
    else: # if the step is in minutes
        columns = pd.DatetimeIndex(start=instance.StartDate(), 
                                   periods=instance.Periods(), 
                                   freq=(str(int(instance.Delta_Time()*60)) + 'min'))# Creation of an index with a start date and a frequency
    
    Scenarios.columns = columns
    Scenarios = Scenarios.transpose()
    
    Scenarios.to_excel('Results_multi/Time_Series_Electric.xls') # Creating an excel file with the values of the variables that are in function of the periods
    
    S = instance.PlotScenario.value
    Time_Series_Electric = pd.DataFrame(index=range(0,35040))
    Time_Series_Electric.index = Scenarios.index
    
    Time_Series_Electric['Electric energy Demand [Wh]']    = Scenarios ['El_Demand [Wh] ' +str(S)]
    Time_Series_Electric['Resistance Demand [Wh]']         = Scenarios ['Res_Demand [Wh] ' +str(S)]
    Time_Series_Electric['PV Energy production [Wh]']      = Scenarios ['PV_Energy [Wh] ' +str(S)]
    Time_Series_Electric['Generator Energy (el+th) [Wh]']  = Scenarios ['Generator_Energy [Wh] ' +str(S)]
    Time_Series_Electric['Lost Load [Wh]']                 = Scenarios ['Lost_Load [Wh] ' +str(S)]
    Time_Series_Electric['Battery Flow Out [Wh]']         = Scenarios ['Battery_Flow_Out [Wh] ' +str(S)]
    
    
    return Time_Series_Electric, Scenarios


def Load_Results_Thermal(instance):
    
    Number_Scenarios = int(instance.Scenarios.extract_values()[None])
    Number_Classes = int(instance.Classes.extract_values()[None])
    Number_Periods = int(instance.Periods.extract_values()[None])

    colonne=[]
    
    for k in range (1,Number_Scenarios+1):
        colonne.append('Scenarios_'+str(k))

    columns= []

    for i in range (1,Number_Classes+1):
        columns.append('Classes_'+str(i))

    Scenarios_Classes=pd.DataFrame()
    
    NG_Consumption    = instance.NG_Consume.get_values()
    Resistance_Energy = instance.Resistance_Thermal_Energy.get_values()
    Lost_Load_Th      = instance.Lost_Load_Th.get_values()
    Tank_SOC          = instance.SOC_Tank.get_values()
    Scenarios_Classes_Periods = [[] for i in range (Number_Classes*Number_Scenarios)]

    for k in range (0,Number_Scenarios):
        for i in range(0,Number_Classes):
            for j in range(1, Number_Periods+1):
                Scenarios_Classes_Periods[Number_Classes*k+i].append((k+1,i+1,j))

    foo=0     
    for k in colonne:
        for i in columns:
            Information = [[] for i in range(4)]
            for j in  Scenarios_Classes_Periods[foo]:
                Information[0].append(NG_Consumption[j])
                Information[1].append(Resistance_Energy[j])
                Information[2].append(Lost_Load_Th[j])
                Information[3].append(Tank_SOC[j])
                
            Scenarios_Classes=Scenarios_Classes.append(Information)
            foo+=1
                
        index=[]  
        for i in range (1,Number_Scenarios+1):
            for j in range(1,Number_Classes+1):   
                index.append('NG_Consumption [kg] '+str(i)+','+str(j))
                index.append('Resistance_Energy [Wh] '+str(i)+','+str(j))
                index.append('Thermal_Demand [Wh] '+str(i)+','+str(j))
                index.append('Lost_Load_Th [Wh] '+str(i)+','+str(j))
                
        Scenarios_Classes.index= index
                        

     # Creation of an index starting in the 'model.StartDate' value with a frequency step equal to 'model.Delta_Time'
    if instance.Delta_Time() >= 1 and type(instance.Delta_Time()) == type(1.0) : # if the step is in hours and minutes
        foo = str(instance.Delta_Time()) # trasform the number into a string
        hour = foo[0] # Extract the first character
        minutes = str(int(float(foo[1:3])*60)) # Extrac the last two character
        columns = pd.DatetimeIndex(start=instance.StartDate(), 
                                   periods=instance.Periods(), 
                                   freq=(hour + 'h'+ minutes + 'min')) # Creation of an index with a start date and a frequency
    elif instance.Delta_Time() >= 1 and type(instance.Delta_Time()) == type(1): # if the step is in hours
        columns = pd.DatetimeIndex(start=instance.StartDate(), 
                                   periods=instance.Periods(), 
                                   freq=(str(instance.Delta_Time()) + 'h')) # Creation of an index with a start date and a frequency
    else: # if the step is in minutes
        columns = pd.DatetimeIndex(start=instance.StartDate(), 
                                   periods=instance.Periods(), 
                                   freq=(str(int(instance.Delta_Time()*60)) + 'min'))# Creation of an index with a start date and a frequency
        
    Scenarios_Classes.columns=columns
    Scenarios_Classes=Scenarios_Classes.transpose()
        
    Scenarios_Classes.to_excel('Results_multi/Time_Series_Thermal.xlsx') # Creating an excel file with the values of the variables that are in function of the periods
    
#    S = instance.PlotScenario.value
    Time_Series_Thermal = pd.DataFrame(index=range(0,35040))
    Time_Series_Thermal.index = Scenarios_Classes.index
#    
#    Time_Series_Thermal['Natural Gas Consumption [kg]']      = Scenarios_Classes ['NG_Consumption [kg] ' +str(S)]
#    Time_Series_Thermal['Energy to thermal resistance [Wh]'] = Scenarios_Classes ['Resistance_Energy [Wh] ' +str(S)]
#    Time_Series_Thermal['Thermal Demand [Wh]']               = Scenarios_Classes ['Thermal_Demand [Wh] ' +str(S)]
#    Time_Series_Thermal['Lost Load th [W]']                  = Scenarios_Classes ['Lost_Load_Th [Wh] ' +str(S)]
#    Time_Series_Thermal['Tank_SOC [Wh]']                     = Scenarios_Classes ['Tank_SOC [Wh] ' +str(S)]
#    

    return Scenarios_Classes


def Load_Results_Cooking(instance):
    '''
    Fourth excel output file with time-dependant cooking-related 
    data
    '''
    Number_Scenarios = int(instance.Scenarios.extract_values()[None])
    Number_Periods   = int(instance.Periods.extract_values()[None])
    
    columns = []
    for i in range(1, Number_Scenarios+1):
        columns.append('Scenario_'+str(i))
    
    Scenarios = pd.DataFrame()
    
    
    Cooking_Demand             = instance.Energy_Demand_Cooking.extract_values()
    Generator_Cooking          = instance.Generator_Energy_Cooking.get_values()
    NG_Energy_Cooking          = instance.NG_Energy_Cooking.get_values()
    El_Energy_Cooking          = instance.El_Energy_Cooking.get_values()
    Battery_Flow_Cooking       = instance.Energy_Battery_Flow_Out_Cooking.get_values()
    Diesel_Consumption_Cooking = instance.Diesel_Consumption_Cooking.get_values()
    NG_Consumption_Cooking     = instance.NG_Consume_Cooking.get_values()
    Energy_PV_Cooking          = instance.Energy_PV_Cooking.get_values()
#    Renewable_Penetration      = instance.Renewable_Penetration_Cooking_Period.get_values()

    
    Scenarios_Periods = [[] for i in range(Number_Scenarios)]
    
    for i in range(0,Number_Scenarios):
        for j in range(1,Number_Periods+1):
            Scenarios_Periods[i].append((i+1,j))
    foo=0
    for i in columns:
        Information = [[] for i in range(8)]
        for j in Scenarios_Periods[foo]:
            Information[0].append(Cooking_Demand[j])
            Information[1].append(Generator_Cooking[j])
            Information[2].append(NG_Energy_Cooking[j])
            Information[3].append(El_Energy_Cooking[j])
            Information[4].append(Battery_Flow_Cooking[j])
            Information[5].append(Diesel_Consumption_Cooking[j])
            Information[6].append(NG_Consumption_Cooking[j])
            Information[7].append(Energy_PV_Cooking[j])
            
        Scenarios = Scenarios.append(Information)
        foo+=1
    
    index=[]
    for j in range(1,Number_Scenarios+1):
        index.append('Cooking_Demand [Wh] ' + str(j))
        index.append('Generator_Cooking [Wh] ' + str(j))
        index.append('NG_Energy_Cooking [Wh] ' + str(j))
        index.append('El_Energy_Cooking [Wh] ' + str(j))
        index.append('Battery_Flow_Cooking [Wh] ' + str(j))
        index.append('Diesel_Consumption_Cooking [l] ' + str(j))
        index.append('NG_Consumption_Cooking [kg] ' + str(j))
        index.append('Energy_PV_Cooking [Wh] ' + str(j))
#        index.append('Renewable_Penetration [%]' + str(j))
    Scenarios.index = index
    
    # Creation of an index starting in the 'model.StartDate' value with a frequency step equal to 'model.Delta_Time'
    if instance.Delta_Time() >= 1 and type(instance.Delta_Time()) == type(1.0) : # if the step is in hours and minutes
        foo = str(instance.Delta_Time()) # trasform the number into a string
        hour = foo[0] # Extract the first character
        minutes = str(int(float(foo[1:3])*60)) # Extrac the last two character
        columns = pd.DatetimeIndex(start=instance.StartDate(), 
                                   periods=instance.Periods(), 
                                   freq=(hour + 'h'+ minutes + 'min')) # Creation of an index with a start date and a frequency
    elif instance.Delta_Time() >= 1 and type(instance.Delta_Time()) == type(1): # if the step is in hours
        columns = pd.DatetimeIndex(start=instance.StartDate(), 
                                   periods=instance.Periods(), 
                                   freq=(str(instance.Delta_Time()) + 'h')) # Creation of an index with a start date and a frequency
    else: # if the step is in minutes
        columns = pd.DatetimeIndex(start=instance.StartDate(), 
                                   periods=instance.Periods(), 
                                   freq=(str(int(instance.Delta_Time()*60)) + 'min'))# Creation of an index with a start date and a frequency
    
    Scenarios.columns = columns
    Scenarios = Scenarios.transpose()
    
    Scenarios.to_excel('Results_multi/Time_Series_Cooking.xls') # Creating an excel file with the values of the variables that are in function of the periods
    
    S = instance.PlotScenario.value
    Time_Series_Cooking = pd.DataFrame(index=range(0,35040))
    Time_Series_Cooking.index = Scenarios.index
    
#    Time_Series_Cooking['Cooking Demand [W]']            = Scenarios ['Cooking_Demand [Wh]' +str(S)]
#    Time_Series_Cooking['Generator use for cooking [W]'] = Scenarios ['Generator_Cooking [Wh] ' +str(S)]
#    Time_Series_Cooking['NG energy for cooking [W]']     = Scenarios ['NG_Energy_Cooking [Wh] ' +str(S)]
#    Time_Series_Cooking['Battery use for cooking [W]']   = Scenarios ['Battery_Flow_Cooking [Wh] ' +str(S)]
#    Time_Series_Cooking['Diesel Consumption [l]']        = Scenarios ['Diesel_Consumption_Cooking [l] ' +str(S)]
#    Time_Series_Cooking['NG Consumption [kg]']           = Scenarios ['NG_Consumption_Cooking [kg] ' +str(S)]
#    Time_Series_Cooking['Energy PV Cooking [Wh]']        = Scenarios ['Energy_PV_Cooking [Wh] ' +str(S)]
#    Time_Series_Cooking['Renewable Penetration [%]']     = Scenarios ['Renewable_Penetration' + str(S)]
    
    return Time_Series_Cooking

def Load_Results(instance):
    '''
    This last file is a collection of all non-time-dependant
    output data and of some important input data as a recap for the 
    user
    '''
    #METTEREI PRIMA I DATI DEI VARI PEZZI POI I PARAMETRI CHE DECIDE IL CODICE!
    #ES: PRIMA LA POTENZA DEI PANNELLI E POI QUANTI NE INSTALLA
    PV_Size = instance.PV_Nominal_Capacity.extract_values()
    SC_Size = instance.SC_Nominal_Capacity.extract_values()
    El_Stove_Nominal_Power = instance.El_Stove_Nominal_Power.extract_values()
    NG_Stove_Nominal_Power = instance.NG_Stove_Nominal_Power.extract_values()
#    NPC = instance.ObjectiveFuntion.expr()
    Number_PV = instance.PV_Units.extract_values()
    Number_SC = instance.SC_Units.extract_values()
    PV_Installed_Power = instance.Installed_Power_PV.extract_values()
    Number_El_Stove = instance.El_Stove_Units.extract_values()
    Number_NG_Stove =instance.NG_Stove_Units.get_values()
    Lost_Load_Probability = instance.Lost_Load_Probability.extract_values()
    OM_Cost_Total = instance.Operation_Maintenance_Cost.get_values() 
    Investment_Cost_Initial = instance.Initial_Inversion.get_values()
    NPC = instance.Final_NPC.get_values()
    Total_Financial_Cost = instance.Total_Finalcial_Cost.get_values()
    Total_Fuel_Cost = instance.Total_Fuel_Cost.extract_values()
#    Installed_El_Renewable_Penetration = instance.Renewable_Penetration_Installed.get_values()
#    Stress_Renewable_Penetration = instance.Stress_Renewable_Penetration.get_values
    
    data = [PV_Size, SC_Size, El_Stove_Nominal_Power, NG_Stove_Nominal_Power, Number_PV, Number_SC,
            PV_Installed_Power, Number_El_Stove, Number_NG_Stove, Lost_Load_Probability,
            OM_Cost_Total, Investment_Cost_Initial, NPC, Total_Financial_Cost, Total_Fuel_Cost,]
    index=['PV Capacity [W]' , 'SC Capacity [W]' , 'El Stove Capacity [W]' ,
           'NG Stove Capacity [W]' , 'PV units [-]' , 'SC units[-]' ,
           'PV Installed PWR [W]' , 'El Stove units[-]', 'NG Stove units [-]' ,
           'Lost Load prob. [0.x]' , 'O&M TOTAL [$]' , 
           'Investment Cost [$]' , 'Net Present Cost [$]' , 'Financial Cost [$]' ,
           'Total Fuel COst [$]'  ]
    Size_variables = pd.DataFrame(data,index)
    Size_variables.to_excel('Results_multi/Size.xls')
    return Size_variables
    
    

'''***************************************************************'''
'''***************************************************************'''
'''***************************************************************'''
'''***************************************************************'''
''' ULTIMA VERSIONE!'''
#    PV_Size = instance.PV_Nominal_Capacity.extract_values()
#    SC_Size = instance.SC_Nominal_Capacity.extract_values()[None]
#    El_Stove_Nominal_Power = instance.El_Stove_Nominal_Power.extract_values()[None]
#    NG_Stove_Nominal_Power = instance.NG_Stove_Nominal_Power.extract_values()[None]
#    Number_PV = instance.PV_Units.extract_values()[None]
#    Number_SC = instance.SC_Units.extract_values()
#    PV_Installed_Power = instance.Installed_Power_PV.extract_values()[1]
#    Number_El_Stove = instance.El_Stove_Units.extract_values()[None]
#    Number_NG_Stove =instance.NG_Stove_Units.get_values()[None]
#    Lost_Load_Probability = instance.Lost_Load_Probability.extract_values()[None]
#    OM_Cost_Total = instance.Operation_Maintenance_Cost.get_values()[None]
#    Investment_Cost_Initial = instance.Initial_Inversion.get_values()[None]
#    NPC = instance.ObjectiveFuntion.expr()
#    Total_Financial_Cost = instance.Total_Finalcial_Cost.get_values()[None]
#    Total_Fuel_Cost = instance.Total_Fuel_Cost.extract_values()[None]
##    Installed_El_Renewable_Penetration = instance.Renewable_Penetration_Installed.get_values()
##    Stress_Renewable_Penetration = instance.Stress_Renewable_Penetration.get_values
#    
#    data = [PV_Size[None], SC_Size, El_Stove_Nominal_Power, NG_Stove_Nominal_Power, Number_PV, Number_SC,
#            PV_Installed_Power, Number_El_Stove, Number_NG_Stove, Lost_Load_Probability,
#            OM_Cost_Total, Investment_Cost_Initial, NPC, Total_Financial_Cost, Total_Fuel_Cost]
#    Size_variables = pd.DataFrame(data, index=['PV Capacity [W]' , 'SC Capacity [W]' , 'El Stove Capacity [W]' ,
#                                               'NG Stove Capacity [W]' , 'PV units [-]' , 'SC units[-]' ,
#                                               'PV Installed PWR [W]' , 'El Stove units[-]', 'NG Stove units [-]' ,
#                                                'Lost Load prob. [0.x]' , 'O&M TOTAL [$]' , 
#                                               'Investment Cost [$]' ,'Net Present Cost [$]',  'Financial Cost [$]' ,
#                                               'Total Fuel Cost [$]'])
#    Size_variables.to_excel('Results_multi/Size.xls')
# 
'''***************************************************************'''
'''***************************************************************'''
'''***************************************************************'''
   

def Plot_Energy_Total(instance, Time_Series_Electric):
    ''' PLOTTING OF ENERGY DISPATCH IN A GIVEN DAY (24-HOUR PERIOD)
    '''
    Periods_day = 24/instance.Delta_Time()
    for x in range(0,instance.Periods()):
        foo = pd.DatetimeIndex(start=instance.PlotDay(),periods=1,freq='1h')
        if foo == Time_Series_Electric.index[x]: 
           Start_Plot = x # asign the value of x to the position where the plot will start 
    End_Plot = Start_Plot + instance.PlotTime()*Periods_day # Create the end of the plot position inside the time_series
    Time_Series_Electric.index=range(1,35041)
    Plot_Data = Time_Series_Electric[Start_Plot:int(End_Plot)] # Extract the data between the start and end position from the Time_Series
    columns = pd.DatetimeIndex(start=instance.PlotDay(), periods=instance.PlotTime()*Periods_day, freq=('1h'))    
    Plot_Data.index=columns
    
    Vect1 = pd.Series(Plot_Data['Battery Flow Out (total) [Wh]'].values + Plot_Data['Generator Energy (el+th) [W]'].values + Plot_Data['Generator use for cooking [W]'].values) #values of total energy to satisfy demand in each moment
    Vect2 = pd.Series(Plot_Data['SOC'])
    Vect3 = pd.Series(Plot_Data['Battery Flow In [Wh]'].values - Plot_Data['Battery Flow Out (total) [Wh]'].values) #Net battery input/output
    Vect4 = pd.Series(Plot_Data['Lost Load [W]'].values)
    Vect5 = pd.Series(Plot_Data['Generator Energy(el+th) [W]'].values + Plot_Data['Generator use for cooking [W]'].values + Plot_Data['NG energy for cooking [W]'].values) #total energy produced by fossil fuels in every period (need also NG for hot water? )
#    Vect6 = pd.Series(Plot_Data[''])
   
    # Plot the line of Energy to satisfy demand in each period
    ax1= Vect1.plot(style='b-', linewidth=0.0) 
#    pylab.ylim([-2000000,10000000])
    ax1.fill_between(Plot_Data.index, 0, Plot_Data['Battery Flow Out (total) [Wh]'].values,   alpha=0.3, color = 'b') # Fill the are of the energy demand satisfied by battery output
    
    # Plot the line of the diesel energy for el and thermal use
    ax2= Plot_Data['Generator Energy (el+th) [W]'].plot(style='r', linewidth=0.5) 
    ax2.fill_between(Plot_Data.index, 0, Plot_Data['Generator Energy (el+th) [W]'].values, alpha=0.2, color='r') # Fill the area of the energy produce by the diesel generator
    
    # Plot the line of the Energy_Demand
    ax3= Vect5.plot(style='k-',linewidth=1) 
    ax3.fill_between(Plot_Data.index, Plot_Data['Generator Energy(el+th) W'].values, Vect5.values, alpha=0.3, color='g') # Fill the area of the fossil fuel produced energy for cooking
    
    # Plot the line of the NET energy flowing into the battery
    ax5= Vect3.plot(style='m', linewidth=0.5) 
    ax5.fill_between(Plot_Data.index, 0, Plot_Data['Lost Load [W]'].values, alpha=0.3, color='m') # Fill the area of the Lost Load to highlight battery trends wrt lost load
    
    # Plot the line of the State of charge of the battery
#    ax6= Vect2.plot(style='k--', secondary_y=True, linewidth=2, alpha=0.7 )
#    pylab.ylim([0,10000000])
    ax7= Vect4.plot(style='b-', linewidth=0.0) # Plot the line of Lost Load
    ax7.fill_between(Plot_Data.index, 0, Vect4.values,  alpha=0.3, color = 'b') # Fill the area between the demand and the curtailment energy
    
    # Plot line with total energy demand then fill total battery output to satisfy it
    ax3.fill_between(Plot_Data.index, Plot_Data , Plot_Data['Energy_Demand'].values, alpha=0.3, color='y') 


#    PV_Nominal_Power
#    Generator_Nominal_Power
#    Battery_Nominal_Capacity 
#    el_Stove_Nominal_Power 
#    NG_Stove_Nominal_Power
#    Max_Total_Power_Output_Demand? (somma dei power output cooking+thermal+el simultanea?)
#
#
#    Number_PV #number of pv installed
#    Number_Generator #number of installed generator
#    Number_SC # number of installed SC
#    PV_Installed_Power # installed total power of PV
#    Generator_Installed_Power # isntalled power of gen - PERCHE LA POTENZA NOMINALE E MESSA COME VARIBAILE?
#    SC_Installed_Power # installed power of SC
#    Number_El_Stove
#    Number_NG_Stove
#    Number batteries?
#    Installed_Cooking_Power
#    Max_Lost_Load
#    Max_Lost_Load_th
#    O&M_Cost_Total
#    Investment_Cost_Total
#    NPC
#    Fuel_Cost_Total
#    Diesel_Cost
#    NG_Cost
#    PV_Cost
#    Battery_Cost
#    Stove_Costs
#    El_Stove_Cost
#    NG_Stove_Cost
#    Renewable_penetration (computed on installed powers)
#    Renewable_Penetration (mean?)
#    Renwable_Penetration (on the max total demand period! -stress condition operation)
#    PLOT dell'andamento domanda vs andamento costi per i combustibili!
#    Plot dell'andamento del renewable penetration period in un giorno qualsiasi



# PROBLEMI CON UDM DEL BATTERY OUT E GENERATORE! BATTERY OUT E DATO IN WH, GENERATOR OUT IN W! CONTROLLA!!!!! (mi sa che è scritta male l'unita di misura nel model creation)

#def Load_Results_Thermal(instance):
#    '''
#    Third excel output file containing relevant time-dependent 
#    thermal-part-related data such as:
#    -Natural gas consumption (th)
#    -Thermal resistance energy
#    -Thermal demand
#    -Lost Load (thermal)
#    -Tank SOC
#    '''
#    
#    Number_Scenarios = int(instance.Scenarios.extract_values()[None])
#    Number_Periods   = int(instance.Periods.extract_values()[None])
#    
#    columns = []
#    for i in range(1, Number_Scenarios+1):
#        columns.append('Scenario_'+str(i))
#    
#    Scenarios = pd.DataFrame()
#    
#    NG_Consumption    = instance.NG_Consume.get_values()
#    Resistance_Energy = instance.Resistance_Thermal_Energy.get_values()
#    Lost_Load_Th      = instance.Lost_Load_Th.get_values()
#    Tank_SOC          = instance.SOC_Tank.get_values()
#    
#    Scenarios_Periods = [[] for i in range(Number_Scenarios)]
#    
#    for i in range(0,Number_Scenarios):
#        for j in range(1,Number_Periods+1):
#            Scenarios_Periods[i].append((i+1,j))
#    foo=0
#    for i in columns:
#        Information = [[] for i in range(0,4)]
#        for j in Scenarios_Periods[foo]:
#            Information[0].append(NG_Consumption[j])
#            Information[1].append(Resistance_Energy[j])
#            Information[2].append(Lost_Load_Th[j])
#            Information[3].append(Tank_SOC[j])
#                       
#        Scenarios = Scenarios.append(Information)
#        foo+=1
#    
#    index=[]
#    for j in range(1,Number_Scenarios+1):
#        index.append('NG_Consumption [kg] ' + str(j))
#        index.append('Resistance_Energy [Wh] ' + str(j))
#        index.append('Thermal_Demand [Wh] ' + str(j))
#        index.append('Lost_Load_Th [Wh] ' + str(j))
#        index.append('Tank_SOC [Wh] ' +str(j))
#    Scenarios.index = index
#    
#    # Creation of an index starting in the 'model.StartDate' value with a frequency step equal to 'model.Delta_Time'
#    if instance.Delta_Time() >= 1 and type(instance.Delta_Time()) == type(1.0) : # if the step is in hours and minutes
#        foo = str(instance.Delta_Time()) # trasform the number into a string
#        hour = foo[0] # Extract the first character
#        minutes = str(int(float(foo[1:3])*60)) # Extrac the last two character
#        columns = pd.DatetimeIndex(start=instance.StartDate(), 
#                                   periods=instance.Periods(), 
#                                   freq=(hour + 'h'+ minutes + 'min')) # Creation of an index with a start date and a frequency
#    elif instance.Delta_Time() >= 1 and type(instance.Delta_Time()) == type(1): # if the step is in hours
#        columns = pd.DatetimeIndex(start=instance.StartDate(), 
#                                   periods=instance.Periods(), 
#                                   freq=(str(instance.Delta_Time()) + 'h')) # Creation of an index with a start date and a frequency
#    else: # if the step is in minutes
#        columns = pd.DatetimeIndex(start=instance.StartDate(), 
#                                   periods=instance.Periods(), 
#                                   freq=(str(int(instance.Delta_Time()*60)) + 'min'))# Creation of an index with a start date and a frequency
#    
#    Scenarios.columns = columns
#    Scenarios = Scenarios.transpose()
#    
#    Scenarios.to_excel('Results_multi/Time_Series_Thermal.xls') # Creating an excel file with the values of the variables that are in function of the periods
#    
#    S = instance.PlotScenario.value
#    Time_Series_Thermal = pd.DataFrame(index=range(0,35040))
#    Time_Series_Thermal.index = Scenarios.index
#    
#    Time_Series_Thermal['Natural Gas Consumption [kg]']     = Scenarios ['NG_Consumption [kg] ' +str(S)]
#    Time_Series_Thermal['Energy to thermal resistance [Wh]'] = Scenarios ['Resistance_Energy [Wh] ' +str(S)]
#    Time_Series_Thermal['Thermal Demand [Wh]']     = Scenarios ['Thermal_Demand [Wh] ' +str(S)]
#    Time_Series_Thermal['Lost Load th [W]']                    = Scenarios ['Lost_Load_Th [Wh] ' +str(S)]
#    Time_Series_Thermal['Tank_SOC [Wh]']            = Scenarios ['Tank_SOC [Wh] ' +str(S)]
#    
#    
#    return Time_Series_Thermal
