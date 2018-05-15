# -*- coding: utf-8 -*-
""" Testing 'sim_db' for python, that is 'sim_db.py'.

Read in parameters from database, write parameters to database, make unique 
subdirectory for results and save 'results.txt' in this directory.
"""
# Copyright (C) 2017, 2018 Håkon Austlid Taskén <hakon.tasken@gmail.com>
# Licenced under the MIT License.

import __init__
import sim_db
import argparse
import os.path
import numpy as np

sim_database = sim_db.SimDB()

param1 = sim_database.read("param1")
print(param1) 
sim_database.write("new_param1", param1, type_of_value="int")
print(sim_database.read("new_param1"))

param2 = sim_database.read("param2")
print(param2) 
sim_database.write("new_param2", param2, type_of_value="float")
print(sim_database.read("new_param2"))

param3 = sim_database.read("param3")
print(param3) 
sim_database.write("new_param3", param3, type_of_value="string")
print(sim_database.read("new_param3"))

param4 = sim_database.read("param4")
print(param4) 
sim_database.write("new_param4", param4, type_of_value="bool")
print(sim_database.read("new_param4"))

param5 = sim_database.read("param5")
print(param5) 
sim_database.write("new_param5", param5, type_of_value="int array")
print(sim_database.read("new_param5"))

param6 = sim_database.read("param6")
print(param6) 
sim_database.write("new_param6", param6, type_of_value="float array")
print(sim_database.read("new_param6"))

param7 = sim_database.read("param7")
print(param7) 
sim_database.write("new_param7", param7, type_of_value="string array")
print(sim_database.read("new_param7"))

param8 = sim_database.read("param8")
print(param8) 
sim_database.write("new_param8", param8, type_of_value="bool array")
print(sim_database.read("new_param8"))

param9 = sim_database.read("param9")
print(param9) 

param10 = sim_database.read("param10")
print(param10) 

large_test_res = np.array(param6)
res_dir = sim_database.make_unique_subdir("test/results")
np.savetxt("{}/results.txt".format(res_dir), large_test_res)

sim_database.end()

