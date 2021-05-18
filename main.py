'''
author:         Philipp Kittler
version:        1.1
license:        MIT license
date:           2021-05-18

description:                                This code creates the needed values for experiment M6 (internal friction / Innere Reibung) by the
                                            measured sinking times, diameters of globules and cylinders including their error ranges. Also the
                                            density of the globules and the oil has to be provided. The code is suitable for experiment M6 at the
                                            physics faculty at Humboldt University to Berlin.

How to create the CSV files:                The values have to be comma separated. Rows represent the series of measurements, columns represent
                                            the different globule diameters. Please consider, that your CSV should not have a header.

How to use this code:                       Put your file paths and values in the marked section below. The code produces output in the console
                                            and in the given output directory in separated CSV files. All values have to be in SI units.

Important note:                             This version doesn't consider to round values.

path_input                                  Path to the directory, which contains your input files
path_output                                 Path to the directory, where the output CSV files will be stored

filename_input_sinkingtimes                 Name of the file, which contains your measured sinking times
filename_input_globules_diameters           Name of the file, which contains your measured or provided diameters of the globules
filename_input_globules_density             Name of the file, which contains the provided values for the density of the globules
filename_input_globules_density_errorranges Name of the file, which contains the provided error range for the density of the globules

cylinder_length                             length of the chosen section of your measuring cylinder
cylinder_length_errorrange                  error range of the measuring cylinder
cylinder_diameter                           diameter of the measuring cylinder
cylinder_diameter_errorrange                error range of the diameter of the measuring cylinder

globules_diameter_errorrange                error range of the diameter of the globules

g                                           acceleration during free fall in vacuum on earth
g_errorrange                                error range for the acceleration

fluid_density                               density of the oil
fluid_density_errorrange                    error range of the oil density
'''

import pandas as pd
import sys
import numpy as np
from pathlib import Path

'''
CHANGE THE FOLLOWING VALUES TO YOUR SYSTEM AND MODALITIES
'''

path_input = Path("C:/Users/phili/PycharmProjects/M6/input/")
path_output = Path("C:/Users/phili/PycharmProjects/M6/output/")

filename_input_sinkingtimes                 = "sinkingtimes.csv"
filename_input_globules_diameters           = "globules_diameters.csv"
filename_input_globules_density             = "globules_density.csv"
filename_input_globules_density_errorranges = "globules_density_errorranges.csv"

cylinder_length                 = 0.20              # in m
cylinder_length_errorrange      = 0.0005            # in m
cylinder_diameter               = 0.0635            # in m
cylinder_diameter_errorrange    = 0.000005          # in m

globules_diameter_errorrange    = 0.000005          # in m

g                               = 9.81235           # in m/s^2
g_errorrange                    = 0.0001            # in m/s^2

fluid_density                   = 965               # in kg/m^3
fluid_density_errorrange        = 0.5               # in kg/m^3

'''
DON'T TOUCH THE CODE BELOW IF YOU DON'T KNOW WHAT YOU ARE DOING
'''

# Print versions of used packages
def package_versions():
    print("Python version: " + sys.version)
    print("Pandas version: " + pd.__version__)

package_versions()

# Print headline
def headline(headline):
    print(" ")
    print("---------------------------------------------")
    print(headline)
    print("---------------------------------------------")

# Prints the results
def result(col, row, value):
    print("Col", col, "| Row", row, ":", value)

# Reading Input Files

location = Path(path_input / filename_input_sinkingtimes)
df_sinkingtimes = pd.read_csv(location, header=None)

location = Path(path_input / filename_input_globules_diameters)
df_globules_diameters = pd.read_csv(location, header=None)

location = Path(path_input / filename_input_globules_density)
df_globules_density = pd.read_csv(location, header=None)

location = Path(path_input / filename_input_globules_density_errorranges)
df_globules_density_errorranges = pd.read_csv(location, header=None)

# create empty lists

velocities                              = []
mean_velocities                         = []
mean_velocities_errorranges             = []

sinkingtimes_errorranges                = []
mean_sinkingtimes                       = []
mean_sinkingtimes_errorranges           = []

dynamic_viscosity                       = []
dynamic_viscosity_errorranges           = []
mean_dynamic_viscosity                  = []

ladenburg_dynamic_viscosity             = []
ladenburg_dynamic_viscosity_errorranges = []
mean_ladenburg_dynamic_viscosity        = []

kinematic_viscosity                     = []
kinematic_viscosity_errorrange          = []

reynolds_number                         = []
reynolds_number_errorrange              = []

# Calculating error range for single measured time
def sinkingtime_errorrange(time):
    return 0.01 + 5 * pow(10, -4) * time

# Calculating error range for all measured times
def calculate_sinkingtimes_errorranges():
    headline("sinking times error ranges")
    for i in range(0, df_sinkingtimes.shape[0]):
        tmp_list = []

        for j in range(0, df_sinkingtimes.shape[1]):
            tmp_list.extend([sinkingtime_errorrange(df_sinkingtimes.iloc[i][j])])
            result(i, j, tmp_list[j])

        sinkingtimes_errorranges.extend([tmp_list])

calculate_sinkingtimes_errorranges()

# Write time error ranges to CSV
location = Path(path_output / "sinkingtimes_errorranges.csv")
df_sinkingtimes_errorranges = pd.DataFrame(data=sinkingtimes_errorranges)
df_sinkingtimes_errorranges.to_csv(location, index=False, header=False)

# Calculate general mean values:
def calculate_mean_values(values):
    total = 0
    items = values.shape[0]

    for i in range(0, items):
        total += values.iloc[i]

    return total / items

def calculate_mean_sinkingtimes():
    tmp_list = []

    headline("mean sinking times")

    for i in range(0, df_sinkingtimes.shape[1]):
        tmp_list.extend([calculate_mean_values(df_sinkingtimes[i])])
        result(i, 0, tmp_list[i])

    mean_sinkingtimes.extend([tmp_list])

calculate_mean_sinkingtimes()

# Write mean times to CSV
location = Path(path_output / "mean_times.csv")
df_mean_sinkingtimes = pd.DataFrame(data = mean_sinkingtimes)
df_mean_sinkingtimes.to_csv(location, index=False, header=False)

# Calculate mean error ranges:
def calculate_mean_sinkingtime_errorranges():
    tmp_list = []

    headline("mean sinking times error ranges")

    for i in range(0, df_sinkingtimes_errorranges.shape[1]):
        mean = calculate_mean_values(df_sinkingtimes_errorranges[i])
        binomicParts = 0
        for j in range(0, df_sinkingtimes_errorranges.shape[0]):
            binomicParts += pow((df_sinkingtimes_errorranges[i][j] - mean),2)

        total = np.sqrt((binomicParts / (df_sinkingtimes_errorranges.shape[0] - 1))/df_sinkingtimes_errorranges.shape[0])
        tmp_list.extend([total])
        result(i, 0, tmp_list[i])

    mean_sinkingtimes_errorranges.extend([tmp_list])

calculate_mean_sinkingtime_errorranges()

# Write mean error ranges of sinking time to CSV
location = Path(path_output / "mean_sinkingtimes_errorranges.csv")
df_mean_sinkingtimes_errorranges = pd.DataFrame(data = mean_sinkingtimes_errorranges)
df_mean_sinkingtimes_errorranges.to_csv(location, index=False, header=False)

# Calculate velocity for single value pair:
def calculate_velocity(l, t):
    return l / t

# Calculate velocity for all value pairs:
def calculate_velocities():
    headline("Velocities")
    for i in range(0, df_sinkingtimes.shape[1]):
        tmp_list = []
        for j in range(0, df_sinkingtimes.shape[0]):
            velocity = calculate_velocity(cylinder_length, df_sinkingtimes[i][j])
            tmp_list.append(velocity)
            result(i, j, velocity)

        velocities.append(tmp_list)

calculate_velocities()

# Write velocities to CSV
location = Path(path_output / "velocities.csv")
df_velocities = pd.DataFrame(data = velocities)
df_velocities.to_csv(location, index=False, header=False)

# Calculate mean velocities
def calculate_mean_velocities():
    tmp_list = []
    headline("mean velocities")
    for i in range(0, df_mean_sinkingtimes.shape[1]):
        tmp_list.append(cylinder_length / df_mean_sinkingtimes[i][0])
        result(i, 0, tmp_list[i])

    mean_velocities.append(tmp_list)

calculate_mean_velocities()

# Write mean velocities to CSV
location = Path(path_output / "mean_velocities.csv")
df_mean_velocities = pd.DataFrame(data = mean_velocities)
df_mean_velocities.to_csv(location, index=False, header=False)

# Calculate error range of mean velocities
def calculate_mean_velocities_errorrange():
    tmp_list = []

    headline("mean velocities error range")

    for i in range(0, df_mean_sinkingtimes.shape[1]):
        tmp_list.append(float(np.sqrt(pow(cylinder_length_errorrange/df_mean_sinkingtimes[i],2) + pow(df_mean_sinkingtimes_errorranges[i]/pow(df_mean_sinkingtimes[i],2),2))))
        result(i, 0, tmp_list[i])

    mean_velocities_errorranges.append(tmp_list)

calculate_mean_velocities_errorrange()

# Write mean error spans velocities to CSV
location = Path(path_output / "mean_velocities_errorranges.csv")
df_mean_velocities_errorranges = pd.DataFrame(data = mean_velocities_errorranges)
df_mean_velocities_errorranges.to_csv(location, index=False, header=False)

# Calculate dynamic viscosity in Pa * s
def calculate_dynamic_viscosity():
    tmp_list = []

    headline("Dynamic Viscosity")

    for i in range(0, df_mean_velocities.shape[1]):
        tmp_list.append(float(((2 * pow(df_globules_diameters[i]/2, 2))/9) * g * ((df_globules_density[i][0] - fluid_density)/(df_mean_velocities[i][0]))))
        result(i, 0, tmp_list[i])

    dynamic_viscosity.append(tmp_list)

calculate_dynamic_viscosity()

# Write dynamic viscosity to CSV
location = Path(path_output / "dynamic_viscosity.csv")
df_dynamic_viscosity = pd.DataFrame(data = dynamic_viscosity)
df_dynamic_viscosity.to_csv(location, index=False, header=False)


# Calculate Ladenburg dynamic viscosity in Pa * s
def calculate_ladenburg_dynamic_viscosity():
    tmp_list = []
    headline("Ladenburg dynamic viscosity")
    for i in range(0, df_mean_velocities.shape[1]):
        tmp_list.append(float(((2 * pow(df_globules_diameters[i]/2, 2))/9) * g * ((df_globules_density[i][0] - fluid_density)/(df_mean_velocities[i][0] * (1 + 2.1 * ((df_globules_diameters[i][0])/(cylinder_diameter)))))))
        result(i,0, tmp_list[i])

    ladenburg_dynamic_viscosity.append(tmp_list)

calculate_ladenburg_dynamic_viscosity()

# Write ladenburg dynamic viscosity to CSV
location = Path(path_output / "ladenburg_dynamic_viscosity.csv")
df_ladenburg_dynamic_viscosity = pd.DataFrame(data = ladenburg_dynamic_viscosity)
df_ladenburg_dynamic_viscosity.to_csv(location, index=False, header=False)

# Calculate error ranges for dynamic viscosity in Pa * s:
def calculate_dynamic_viscosity_errorranges():
    tmp_list = []

    headline("dynamic viscosity error ranges")

    for i in range(0, df_dynamic_viscosity.shape[1]):
        max_level = (2/9) * (g+g_errorrange) * pow((float(df_globules_diameters[i][0]) + cylinder_diameter_errorrange)/2, 2) * (((float(df_globules_density[i][0]) + float(df_globules_density_errorranges[i][0])) - (fluid_density + fluid_density_errorrange)) / (float(df_mean_velocities[i][0]) + float(df_mean_velocities_errorranges[i][0])))
        min_level = (2/9) * (g-g_errorrange) * pow((float(df_globules_diameters[i][0]) - cylinder_diameter_errorrange)/2, 2) * (((float(df_globules_density[i][0]) - float(df_globules_density_errorranges[i][0])) - (fluid_density - fluid_density_errorrange)) / (float(df_mean_velocities[i][0]) - float(df_mean_velocities_errorranges[i][0])))
        level_difference = max_level - min_level
        vrange = level_difference / 2
        result(i,0,vrange)

        tmp_list.append(vrange)

    dynamic_viscosity_errorranges.extend([tmp_list])

calculate_dynamic_viscosity_errorranges()

# Write error spans dynamic viscosity to CSV
location = Path(path_output / "dynamic_viscosity_errorranges.csv")
df_dynamic_viscosity_errorranges = pd.DataFrame(data = dynamic_viscosity_errorranges)
df_dynamic_viscosity_errorranges.to_csv(location, index=False, header=False)

# Calculate error spans for ladenburg dynamic viscosity in Pa * s:
def calculate_ladenburg_dynamic_viscosity_errorranges():
    tmp_list = []

    headline("Ladenburg dynamic viscosity error ranges")

    for i in range(0, df_dynamic_viscosity.shape[1]):
        max_level = (2/9) * (g+g_errorrange) * pow((float(df_globules_diameters[i][0]) + cylinder_diameter_errorrange)/2, 2) * (((float(df_globules_density[i][0]) + float(df_globules_density_errorranges[i][0])) - (fluid_density + fluid_density_errorrange)) / ((float(df_mean_velocities[i][0]) + float(df_mean_velocities_errorranges[i][0])) * (1 + 2.1 * ((df_globules_diameters[i][0] + globules_diameter_errorrange)/(cylinder_diameter + cylinder_diameter_errorrange)))))
        min_level = (2/9) * (g-g_errorrange) * pow((float(df_globules_diameters[i][0]) - cylinder_diameter_errorrange)/2, 2) * (((float(df_globules_density[i][0]) - float(df_globules_density_errorranges[i][0])) - (fluid_density - fluid_density_errorrange)) / ((float(df_mean_velocities[i][0]) - float(df_mean_velocities_errorranges[i][0])) * (1 + 2.1 * ((df_globules_diameters[i][0] - globules_diameter_errorrange)/(cylinder_diameter - cylinder_diameter_errorrange)))))
        level_difference = max_level - min_level
        vrange = level_difference / 2

        tmp_list.append(vrange)

        result(i,0, vrange)

    ladenburg_dynamic_viscosity_errorranges.extend([tmp_list])

calculate_ladenburg_dynamic_viscosity_errorranges()

# Write error ranges ladenburg dynamic viscosity to CSV
location = Path(path_output / "ladenburg_dynamic_viscosity_errorranges.csv")
df_ladenburg_dynamic_viscosity_errorranges = pd.DataFrame(data = ladenburg_dynamic_viscosity_errorranges)
df_ladenburg_dynamic_viscosity_errorranges.to_csv(location, index=False, header=False)

# Calculate mean dynamic viscosity
def calculate_mean_dynamic_viscosity():
    tmp_list = []
    total = 0

    headline("mean dynamic viscosity")

    for i in range(0, df_dynamic_viscosity.shape[1]):
        total += df_dynamic_viscosity[i][0]

    mean = total / df_dynamic_viscosity.shape[1]
    tmp_list.extend([mean])
    mean_dynamic_viscosity.extend([tmp_list])
    result(0, 0, mean)

calculate_mean_dynamic_viscosity()

# Write mean dynamic viscosity to CSV
location = Path(path_output / "mean_dynamic_viscosity.csv")
df_mean_dynamic_viscosity = pd.DataFrame(data = mean_dynamic_viscosity)
df_mean_dynamic_viscosity.to_csv(location, index=False, header=False)

# Calculate mean ladenburg dynamic viscosity
def calculate_mean_ladenburg_dynamic_viscosity():
    tmp_list = []
    total = 0

    headline("mean ladenburg dynamic viscosity")

    for i in range(0, df_ladenburg_dynamic_viscosity.shape[1]):
        total += df_ladenburg_dynamic_viscosity[i][0]

    mean = total / df_ladenburg_dynamic_viscosity.shape[1]
    tmp_list.extend([mean])
    mean_ladenburg_dynamic_viscosity.extend([tmp_list])
    result(0,0, mean)

calculate_mean_ladenburg_dynamic_viscosity()

# Write mean ladenburg dynamic viscosity to CSV
location = Path(path_output / "mean_ladenburg_dynamic_viscosity.csv")
df_mean_ladenburg_dynamic_viscosity = pd.DataFrame(data = mean_ladenburg_dynamic_viscosity)
df_mean_ladenburg_dynamic_viscosity.to_csv(location, index=False, header=False)

# Calculate SEM
def calculate_SEM(mean_value, values):
    tmp_list = []
    mean = mean_value
    binomicParts = 0

    for i in range(0, values.shape[1]):
        binomicParts += pow((values[i][0] - mean), 2)

    total = np.sqrt((binomicParts / (values.shape[1] - 1))/values.shape[1]) / np.sqrt(values.shape[1])
    tmp_list.extend(total)

    return tmp_list

# Calculate error range for mean dynamic viscosity by SEM
mean_dynamic_viscosity_errorrange = calculate_SEM(mean_dynamic_viscosity, df_dynamic_viscosity)
headline("mean dynamic viscosity error range")
result(0,0, mean_dynamic_viscosity_errorrange[0][0])

# Write error range mean dynamic viscosity to CSV
location = Path(path_output / "mean_dynamic_viscosity_errorrange.csv")
df_mean_dynamic_viscosity_errorrange = pd.DataFrame(data = mean_dynamic_viscosity_errorrange)
df_mean_dynamic_viscosity_errorrange.to_csv(location, index=False, header=False)

# Calculate error range for mean ladenburg dynamic viscosity by SEM
mean_ladenburg_dynamic_viscosity_errorrange = calculate_SEM(mean_ladenburg_dynamic_viscosity, df_ladenburg_dynamic_viscosity)
headline("mean ladenburg dynamic viscosity error range")
result(0,0, mean_ladenburg_dynamic_viscosity_errorrange[0][0])

# Write error range mean ladenburg dynamic viscosity to CSV
location = Path(path_output / "mean_ladenburg_dynamic_viscosity_errorrange.csv")
df_mean_ladenburg_dynamic_viscosity_errorrange = pd.DataFrame(data = mean_ladenburg_dynamic_viscosity_errorrange)
df_mean_ladenburg_dynamic_viscosity_errorrange.to_csv(location, index=False, header=False)

# Calculate kinematic viscosity
def calculate_kinematic_viscosity():
    tmp_list = []
    tmp_list.append(df_mean_dynamic_viscosity[0][0] / fluid_density)
    kinematic_viscosity.append(tmp_list)
    headline("kinematic viscosity")
    result(0,0, kinematic_viscosity[0][0])

calculate_kinematic_viscosity()

# Write kinematic viscosity to CSV
location = Path(path_output / "kinematic_viscosity.csv")
df_kinematic_viscosity = pd.DataFrame(data = kinematic_viscosity)
df_kinematic_viscosity.to_csv(location, index=False, header=False)

# Calculate error range for kinematic viscosity
def calculate_kinematic_viscosity_errorrange():
    max_level = (df_mean_dynamic_viscosity[0][0] + df_mean_dynamic_viscosity_errorrange[0][0]) / (fluid_density + fluid_density_errorrange)
    min_level = (df_mean_dynamic_viscosity[0][0] - df_mean_dynamic_viscosity_errorrange[0][0]) / (fluid_density - fluid_density_errorrange)
    difference = max_level - min_level
    vrange = difference / 2
    kinematic_viscosity_errorrange.append(vrange)
    headline("kinematic viscosity error range")
    result(0,0, vrange)

calculate_kinematic_viscosity_errorrange()

# Write error range kinematic viscosity to CSV
location = Path(path_output / "kinematic_viscosity_errorrange.csv")
df_kinematic_viscosity_errorrange = pd.DataFrame(data = kinematic_viscosity_errorrange)
df_kinematic_viscosity_errorrange.to_csv(location, index=False, header=False)

# Calculate Reynolds value for all spheres
def calculate_reynolds_number():
    tmp_list = []
    headline("Reynolds number")
    for i in range(0, df_dynamic_viscosity.shape[1]):
        Re = (df_kinematic_viscosity[0][0] * (df_globules_diameters[i][0]/2) * fluid_density) / (df_dynamic_viscosity[i][0])
        tmp_list.append(Re)
        result(i,0,Re)

    reynolds_number.extend([tmp_list])

calculate_reynolds_number()

# Write Reynolds number to CSV
location = Path(path_output / "reynolds_number.csv")
df_reynolds_number = pd.DataFrame(data = reynolds_number)
df_reynolds_number.to_csv(location, index=False, header=False)

# Calculate error range for reynolds values
def calculate_reynolds_number_errorrange():
    tmp_list = []

    headline("Reynolds number error range")

    for i in range(0, df_globules_diameters.shape[1]):
        max_level = ((df_kinematic_viscosity[0][0] + df_kinematic_viscosity_errorrange[0][0]) * ((df_globules_diameters[i][0]/2) + globules_diameter_errorrange) * (fluid_density + fluid_density_errorrange)) / ((df_dynamic_viscosity[i][0] + df_dynamic_viscosity_errorranges[i][0]))
        min_level = ((df_kinematic_viscosity[0][0] - df_kinematic_viscosity_errorrange[0][0]) * ((df_globules_diameters[i][0]/2) - globules_diameter_errorrange) * (fluid_density - fluid_density_errorrange)) / ((df_dynamic_viscosity[i][0] - df_dynamic_viscosity_errorranges[i][0]))
        difference = max_level - min_level
        vrange = difference / 2
        tmp_list.append(vrange)
        result(i,0,vrange)

    reynolds_number_errorrange.append(tmp_list)

calculate_reynolds_number_errorrange()

# Write error range reynolds values to CSV
location = Path(path_output / "reynolds_number_errorrange.csv")
df_reynolds_number_errorrange = pd.DataFrame(data = reynolds_number_errorrange)
df_reynolds_number_errorrange.to_csv(location, index=False, header=False)