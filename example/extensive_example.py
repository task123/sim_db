# -*- coding: utf-8 -*-
""" Example program showing how to use the python version of 'sim_db'.

Usage: 'add_and_run --filename sim_params_example_python_program.txt'
    or with parameter with id, ID, in database:
       'python example_program --id ID --path_sim_db ".."'
"""
# Copyright (C) 2017 Håkon Austlid Taskén <hakon.tasken@gmail.com>
# Licenced under the MIT License.

import numpy as np
import sys, os
# Include the 'sim_db/src/' directory to path.
sys.path.append(os.path.join(os.path.dirname(__file__), "../src"))

import sim_db # 'sim_db/src/' have been include in the path.

# Open database and write some initial metadata to database.
sim_database = sim_db.SimDB()

# Read parameters from database.
param1 = sim_database.read("param1_extensive") # Integer
param2 = sim_database.read("param2_extensive") # Float
param3 = sim_database.read("param3_extensive") # String 
param4 = sim_database.read("param4_extensive") # Bool 
param5 = sim_database.read("param5_extensive") # List of integers 
param6 = sim_database.read("param6_extensive") # List of floats 
param7 = sim_database.read("param7_extensive") # List of strings 
param8 = sim_database.read("param8_extensive") # List of bools 

# Demonstrate that the simulation is running.
print(param3)

# Write to database.
sim_database.write("example_result_1", param1, type_of_value="int")
sim_database.write("example_result_2", param2, type_of_value="float")
sim_database.write("example_result_3", param3, type_of_value="string")
sim_database.write("example_result_4", param4, type_of_value="bool")
sim_database.write("example_result_5", param5, type_of_value="int array")
sim_database.write("example_result_6", param6, type_of_value="float array")
sim_database.write("example_result_7", param7, type_of_value="string array")
sim_database.write("example_result_8", param8, type_of_value="bool array")

# Make unique subdirectory for storing results and write its name to database.
results = np.array(param6)
name_results_dir = sim_database.make_unique_subdir("example/results")
np.savetxt(name_results_dir + "/results.txt", results)

# Write final metadata to database.
sim_database.end()
