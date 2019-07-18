# -*- coding: utf-8 -*-
"""
Created on Wed Mar  7 16:49:26 2018

@author: pisto
"""

from pyomo.opt import SolverFactory
from pyomo.environ import Objective, minimize, Constraint


def Model_Resolution(model,datapath="Example/data.dat"):   
    '''
    This function creates the model and call Pyomo to solve the instance of the proyect 
    
    :param model: Pyomo model as defined in the Model_creation library
    :param datapath: path to the input data file
    
    :return: The solution inside an object call instance.
    '''
    
    from Constraints_Thermal import  (Net_Present_Cost, Solar_Energy, State_of_Charge, \
    Maximun_Charge, Minimun_Charge, Max_Power_Battery_Charge, Max_Power_Battery_Discharge, Max_Bat_in, Max_Bat_out, \
    Financial_Cost, Energy_balance, Maximun_Lost_Load, Maximun_Lost_Load_Th, Scenario_Net_Present_Cost, Scenario_Lost_Load_Cost, Scenario_Lost_Load_Cost_Th, \
    Initial_Inversion, Operation_Maintenance_Cost, Total_Finalcial_Cost, Battery_Reposition_Cost, Maximun_Diesel_Energy, Diesel_Comsuption,Diesel_Cost_Total, \
    Solar_Thermal_Energy, State_Of_Charge_Tank, Maximun_Tank_Charge, Maximum_Boiler_Energy, \
    NG_Consumption, Maximum_Resistance_Thermal_Energy, Total_Thermal_Energy_Demand, Thermal_Energy_Balance, Total_Electrical_Resistance_Demand, SC_Financial_Cost, \
    Tank_Financial_Cost, Boiler_Financial_Cost, NPC_Final, Resistance_Financial_Cost, NG_Cost_Total , Minimun_Tank_Charge, Max_Power_Tank_Discharge, \
    Max_Tank_out, Maximum_Energy_El_Stove, Total_Cost_Fuel, \
    #NG_Consumption_Cooking, 
#     
    Energy_Cooking_Balance, \
    #Minimum_Installed_Stove, \
    El_Energy_Cooking_Balance, NG_Energy_Cooking_Balance, \
    Installed_Power_Balance_Cooking, \
#    Total_Demand_Cooking, \
    PV_Division, PV_Installed, Limit_NG_Cooking_Demand, NG_Consumption_Thermal, \
    Limit_El_Cooking_Demand, NG_Total_Consumption )
#    Cooking_Renewable_Penetration_Period,  Stress_Condition_Renewable_Penetration, Renewable_Penetration)
    
    
    
    # OBJETIVE FUNTION:
    model.ObjectiveFuntion = Objective(rule=Net_Present_Cost, sense=minimize)  
    
    # CONSTRAINTS
    #Energy constraints
    model.EnergyBalance = Constraint(model.scenario,model.periods, rule=Energy_balance)
    model.MaximunLostLoad = Constraint(model.scenario, rule=Maximun_Lost_Load) # Maximum permissible lost load
    model.MaximunLostLoadTh = Constraint(model.scenario, model.classes, rule=Maximun_Lost_Load_Th) # Maximum permissible lost load
    model.ScenarioLostLoadCost = Constraint(model.scenario, rule=Scenario_Lost_Load_Cost)
    model.ScenarioLostLoadCostTh = Constraint(model.scenario, rule=Scenario_Lost_Load_Cost_Th)
    model.TotalThermalEnergyDemand = Constraint(model.scenario, model.classes, model.periods, rule=Total_Thermal_Energy_Demand)
    model.ThermalEnergyBalance = Constraint(model.scenario, model.classes, model.periods, rule=Thermal_Energy_Balance)
    model.TotalElectricalResistanceDemand = Constraint(model.scenario, model.periods, rule=Total_Electrical_Resistance_Demand)

    # Solar Collectors Constraints    
    model.SolarThermalEnergy = Constraint(model.scenario, model.classes, model.periods, rule=Solar_Thermal_Energy)

    # PV constraints
    model.SolarEnergy = Constraint(model.scenario, model.periods, rule=Solar_Energy)  # Energy output of the solar panels
    
    # Battery constraints
    model.StateOfCharge = Constraint(model.scenario, model.periods, rule=State_of_Charge) # State of Charge of the battery
    model.MaximunCharge = Constraint(model.scenario, model.periods, rule=Maximun_Charge) # Maximun state of charge of the Battery
    model.MinimunCharge = Constraint(model.scenario, model.periods, rule=Minimun_Charge) # Minimun state of charge
    model.MaxPowerBatteryCharge = Constraint(rule=Max_Power_Battery_Charge)  # Max power battery charge constraint
    model.MaxPowerBatteryDischarge = Constraint(rule=Max_Power_Battery_Discharge)    # Max power battery discharge constraint
    model.MaxBatIn = Constraint(model.scenario, model.periods, rule=Max_Bat_in) # Minimun flow of energy for the charge fase
    model.Maxbatout = Constraint(model.scenario, model.classes, model.periods, rule=Max_Bat_out) #minimun flow of energy for the discharge fase

    # Tank Constraints     
    model.StateOfChargeTank = Constraint(model.scenario, model.classes, model.periods, rule =State_Of_Charge_Tank)
    model.MaximumTankCharge = Constraint(model.scenario, model.classes, model.periods, rule =Maximun_Tank_Charge)
    model.MinimunTankCharge = Constraint(model.scenario, model.classes, model.periods, rule =Minimun_Tank_Charge)
    model.MaxPowerTankDischarge = Constraint(model.classes, rule =Max_Power_Tank_Discharge)
    model.MaxTankout = Constraint(model.scenario, model.classes, model.periods, rule =Max_Tank_out)
    
    # Boiler Constraints     
    model.MaximumBoilerEnergy = Constraint(model.scenario, model.classes, model.periods, rule =Maximum_Boiler_Energy) 
    model.NGConsumption = Constraint(model.scenario, model.classes, model.periods, rule = NG_Consumption)
    model.NGCostTotal = Constraint(model.scenario, rule = NG_Cost_Total)
    
    # Electrical Resistance Constraint     
    model.MaximumResistanceThermalEnergy = Constraint(model.scenario, model.classes, model.periods, rule = Maximum_Resistance_Thermal_Energy)
    
    # Diesel Generator constraints
    model.MaximunDieselEnergy = Constraint(model.scenario, model.periods, rule=Maximun_Diesel_Energy) # Maximun energy output of the diesel generator
    model.DieselComsuption = Constraint(model.scenario, model.periods, rule=Diesel_Comsuption)    # Diesel comsuption 
    model.DieselCostTotal = Constraint(model.scenario, rule=Diesel_Cost_Total)
    
    # Financial Constraints
    #model.MinRES = Constraint(model.scenario, model.classes, rule = Min_Renewables )
    model.SCFinancialCost = Constraint(rule = SC_Financial_Cost ) 
    model.TankFinancialCost = Constraint(rule = Tank_Financial_Cost ) 
    model.BoilerFinancialCost = Constraint(rule =Boiler_Financial_Cost )
    model.ResistanceFinancialCost = Constraint(rule = Resistance_Financial_Cost )
    model.FinancialCost = Constraint(rule=Financial_Cost) # Financial cost
    model.ScenarioNetPresentCost = Constraint(model.scenario, rule=Scenario_Net_Present_Cost)    
    model.InitialInversion = Constraint(rule=Initial_Inversion)
    model.OperationMaintenanceCost = Constraint(rule=Operation_Maintenance_Cost)
    model.TotalFinalcialCost = Constraint(rule=Total_Finalcial_Cost)
    model.BatteryRepositionCost = Constraint(rule=Battery_Reposition_Cost) 
    model.FinalNPC = Constraint(rule=NPC_Final)
    #New Constraints
#    model.NGConsumptionCooking = Constraint(model.scenario, model.periods, rule=NG_Consumption_Cooking )
    model.MaximumEnergyElStove = Constraint(model.scenario, model.periods, rule=Maximum_Energy_El_Stove )
#    model.MinimumInstalledStove = Constraint(model.scenario, rule=Minimum_Installed_Stove )
    model.EnergyCookingBalance = Constraint(model.scenario, model.periods, rule=Energy_Cooking_Balance )
    model.ElEnergyCookingBalance = Constraint(model.scenario, model.periods, rule=El_Energy_Cooking_Balance )
    model.NGEnergyCookingBalance = Constraint(model.scenario, model.periods, rule=NG_Energy_Cooking_Balance )
    model.InstalledPowerBalanceCooking = Constraint(model.scenario, rule=Installed_Power_Balance_Cooking )
#    model.TotalDemandCooking = Constraint(model.scenario, model.periods, rule=Total_Demand_Cooking )
    model.PVDivision = Constraint(model.scenario, model.periods, rule=PV_Division )
    model.PVInstalled = Constraint(model.scenario, rule=PV_Installed )
    model.LimitNGDemand = Constraint(model.scenario, model.periods, rule=Limit_NG_Cooking_Demand )
    model.LimitElDemand = Constraint(model.scenario, model.periods, rule=Limit_El_Cooking_Demand )
    model.NGTotal = Constraint(model.scenario, model.periods, rule=NG_Total_Consumption )
    model.NGThermal = Constraint(model.scenario, model.periods, rule=NG_Consumption_Thermal)
    model.TotalCostFuel = Constraint(rule=Total_Cost_Fuel)
#    model.RenewablePenetration = Constraint(rule=Renewable_Penetration )
#    model.StressRenewablePenetration = Constraint(rule=Stress_Condition_Renewable_Penetration )
#    model.CookingRenewable = Constraint(model.scenario, model.periods, rule=Cooking_Renewable_Penetration_Period )
#    model.MinElCookingFactor = Constraint(rule=Minimum_El_Cooking_Factor)
#    model.MaxElCookingFactor = Constraint(rule=Maximum_El_Cooking_Factor)
#    model.ElectricEnergyCookingDemand = Constraint(model.scenario, model.periods, rule=Electric_Energy_Cooking_Demand)
 
    print('model resolution executed')    
    
    instance = model.create_instance(datapath) # load parameters 

    print('instance created')
      
    opt = SolverFactory('cplex') # Solver use during the optimization    
    results = opt.solve(instance, tee=True) # Solving a model instance 
    
    print('solver called')
    
    instance.solutions.load_from(results)  # Loading solution into instance
    return instance
    
