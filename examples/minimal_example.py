# -*- coding: utf-8 -*-
""" Minimal example showing how to use the python version of 'sim_db'.

Usage: 'add_and_run --filename sim_params_minimal_python_example.txt'
    or with parameter with id, ID, in database:
       'python minimal_example.py --id ID --path_sim_db ".."'
"""
# Copyright (C) 2017 Håkon Austlid Taskén <hakon.tasken@gmail.com>
# Licenced under the MIT License.

# Include the 'sim_db/' directory to path.
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import sim_db # 'sim_db/src/' have been include in the path.

# Open database and write some initial metadata to database.
sim_database = sim_db.SimDB()

# Read parameters from database.
param1 = sim_database.read("param1") # String
param2 = sim_database.read("param2") # Integer

# Print param1 just to show that the example is running.
print(param1)

# Write final metadata to database.
sim_database.end()
