# -*- coding: utf-8 -*-
""" Example program showing how to use the python version of 'sim_db'.

Usage: 'add_and_run --filename sim_params_example_python_program.txt'
    or with parameter with id, ID, in database:
       'python example_program --id ID --path_sim_db ".."'
"""
# Copyright (C) 2017-2019 Håkon Austlid Taskén <hakon.tasken@gmail.com>
# Licenced under the MIT License.

import numpy as np
import sys, os
# Include the 'sim_db/' directory to path.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import sim_db # 'sim_db/' have been included in the path.

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
name_results_dir = sim_database.unique_results_dir("root/examples/results")
np.savetxt(name_results_dir + "/results.txt", results)

# Check if column exists in database.
is_column_in_database = sim_database.column_exists("column_not_in_database")

# Check is column is empty and then set it to empty.
sim_database.is_empty("example_result_1")
sim_database.set_empty("example_result_1")

# Get the 'ID' of the connected simulation and the path to the root directory.
db_id = sim_database.get_id()
path_proj_root = sim_database.get_path_proj_root()

# Write final metadata to the database and close the connection.
sim_database.close()

# Add an empty simulation to database, open connection and write to it.
sim_database_2 = sim_db.add_empty_sim(False)
sim_database_2.write("param1_extensive", 7, type_of_value="int")

# Delete simulation from the database.
sim_database_2.delete_from_database()

# Close connection to the database.
sim_database_2.close()
