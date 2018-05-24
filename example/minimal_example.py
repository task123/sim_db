# -*- coding: utf-8 -*-
""" Minimal example showing how to use the python version of 'sim_db'.

Usage: 'add_and_run --filename sim_params_minimal_python_example.txt'
    or with parameter with id, ID, in database:
       'python minimal_example.py --id ID --path_sim_db ".."'
"""
# Copyright (C) 2017 Håkon Austlid Taskén <hakon.tasken@gmail.com>
# Licenced under the MIT License.

# Include the 'sim_db/src/' directory to path.
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "../src"))

import sim_db # 'sim_db/src/' have been include in the path.

# Open database and write some initial metadata to database.
sim_database = sim_db.SimDB()

# Read parameters from database.
param_1 = sim_database.read("param_1") # String
param_2 = sim_database.read("param_2") # List of integers

# Print param_1 just to show that the example is running.
print(param_1)

# Write final metadata to database.
sim_database.end()
