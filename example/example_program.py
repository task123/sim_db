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
example_dir = os.path.dirname(os.path.abspath(__file__))
sim_db_src_dir = os.path.abspath(os.path.join(example_dir, "../src"))
sys.path.append(sim_db_src_dir)
import sim_db

# Open database and write some initial metadata to database.
sim_database = sim_db.SimDB()

# Read parameters from database.
example_param1 = sim_database.read("example_param1") # String
example_param2 = sim_database.read("example_param2") # List of integers

# Write to database.
small_result = 42.0
sim_database.write("example_small_result", small_result, type_of_value=float)

# Make unique subdirectory for storing results and write its name to database.
results = np.array([1, 3, 7])
name_results_dir = sim_database.make_unique_subdir("example/results")
np.savetxt(name_results_dir + "/results.txt", results)

# Write final metadata to database. 
sim_database.end()
