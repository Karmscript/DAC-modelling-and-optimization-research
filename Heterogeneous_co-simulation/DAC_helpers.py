#import all necessary libraries
import pandas as pd
import numpy as np
import math

def sutherland_air_viscosity(DAC_ambient_temp):
    
    """
    function calculates the viscosity of air based on the conditions in the DAC unit using Sutherland equation

    Paramters
    ---------
    DAC_ambient_temp: This is the operating temperature of the Direct Air Capture unit, input unit is C, converted to Kelvin below

    returns
    ------
    returns delta_p: the pressure drop across the bed (Pa or N/m2)
    """
    #base values
    ref_mu = 1.827 * 10**(-5)  # reference viscosity of air, unit is Pa.S
    ref_temp = 291.15          # reference temperature, unit is Kelvin
    suther_const = 120         # sutherland constant

    #viscosity at the air temperature
    mu  =  ref_mu * ((ref_temp + suther_const) / ((DAC_ambient_temp + 273.15) + suther_const)) * (( DAC_ambient_temp + 273.15) / ref_temp)**1.5

    #return the calculated viscosity
    return mu


def specific_gas_const(DAC_ambient_temp, MW_air):
    """
    function calculates the specific gas constant * gas temperature

    Paramters
    ---------
    DAC_ambient_temp: This is the operating temperature of the Direct Air Capture unit, unit is C, converted to K below
    MW_air is Molecular weight of air, unit is kg/kmol
    returns
    ------
    returns the value of RT/MW_air
    """
    # Constant values
    R = 8.314            # Universal gas constant, unit is J/(mol.K)

    # Calculate the RT/MW_air AT TEMP, converts molar weight to kg/mol from kg/kmol or g/mol
    RT_ratio_MWair = R * (DAC_ambient_temp + 273.15) / (MW_air/1000)

    #return
    return RT_ratio_MWair

def gas_mass_flux(kg_per_hr):
    """
    function calculates the mass flux of gas in kg/ (m^2 s)

    Paramters
    ---------
    kmol_per_hr is the air flow rate

    returns
    ------
    returns the G_flux in kg/(m2 . s)
    """

    cross_area = math.pi * (7/2)**2                # diameter of DAC column fixed as 7 meters
    kg_per_sec = kg_per_hr / 3600                  # converts to kg per second
    G_flux = kg_per_sec / cross_area               # Gas mas flux

    # return the mass flux
    return G_flux


def obtain_ergun_pressure_inlet(L, e_void, dp, DAC_ambient_temp, kg_per_hr, MW_air):
    """
    function calculates the Ergun pressure that is based on the conditions in the DAC unit

    Paramters
    ---------
    
    L is the length of the bed (m)
    e_void is the void fraction (porosity) of the bed (dimensionless)
    dp is the average particle diameter (mm), converted to m in code
    sphericity is the sphericity of the particles.
    DAC_ambient_temp: This is the operating temperature of the Direct Air Capture unit, unit is Kelvin (K)
    kg_per_hr is the flow rate of air into the Direct Air Capture unit, unit is kmol/hr, value is converted to kg/s in code

    returns
    ------
    P_in: the pressure into the the DAC unit (Pa or N/m2), converted to atm in return call
    """
    #sphericity assumed to be 1 for simplicity
    sphericity = 1
    
    #mu is the dynamic viscosity of the fluid (Pa.s)
    mu = sutherland_air_viscosity(DAC_ambient_temp)

    #Calculate mass flux of gas
    G = gas_mass_flux(kg_per_hr)

    #calculate the ratio of RT to MWair
    RT_ratio_MWair = specific_gas_const(DAC_ambient_temp, MW_air)
    
    #laminar term
    laminar_term = (150 * mu * G * (1 - e_void)**2) / (((dp / 1000)**2) * (e_void**3) * (sphericity**2))

    # turbulence term
    turbulence_term = (1.75 * (1 - e_void) * (G**2)) / ((e_void**3) * (dp / 1000) * sphericity)
    
    #The Ergun Equation
    delta_p_squared = 2 * RT_ratio_MWair * L * (laminar_term + turbulence_term)

    #Return pressure into DAC
    P_in = math.sqrt(delta_p_squared + 101325**2)

    return P_in / 101325

