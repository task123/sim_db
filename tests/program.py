# -*- coding: utf-8 -*-
""" Testing 'sim_db' for python, that is 'sim_db.py'.

Read in parameters from database, write parameters to database, make unique 
subdirectory for results and save 'results.txt' in this directory.

Finally add empty simulation, write to it and read from it and then delete it.
"""
# Copyright (C) 2017, 2018 Håkon Austlid Taskén <hakon.tasken@gmail.com>
# Licenced under the MIT License.

import add_root_dir_to_path
import src.sim_db as sim_db
import argparse
import os.path
import sys
import numpy as np

if 'no_metadata' in sys.argv:
    store_metadata = False
else:
    store_metadata = True

sim_database = sim_db.SimDB(store_metadata=store_metadata)

param1 = sim_database.read("test_param1")
print(param1)
sim_database.write("new_test_param1", param1, type_of_value="int")
print(sim_database.read("new_test_param1"))

param2 = sim_database.read("test_param2")
print(param2)
sim_database.write("new_test_param2", param2, type_of_value="float")
print(sim_database.read("new_test_param2"))

param3 = sim_database.read("test_param3")
print(param3)
sim_database.write("new_test_param3", param3, type_of_value="string")
print(sim_database.read("new_test_param3"))

param4 = sim_database.read("test_param4")
print(param4)
sim_database.write("new_test_param4", param4, type_of_value="bool")
print(sim_database.read("new_test_param4"))

param5 = sim_database.read("test_param5")
print(param5)
sim_database.write("new_test_param5", param5, type_of_value="int array")
print(sim_database.read("new_test_param5"))

param6 = sim_database.read("test_param6")
print(param6)
sim_database.write("new_test_param6", param6, type_of_value="float array")
print(sim_database.read("new_test_param6"))

param7 = sim_database.read("test_param7")
print(param7)
sim_database.write("new_test_param7", param7, type_of_value="string array")
print(sim_database.read("new_test_param7"))

param8 = sim_database.read("test_param8")
print(param8)
sim_database.write("new_test_param8", param8, type_of_value="bool array")
print(sim_database.read("new_test_param8"))

param9 = sim_database.read("test_param9")
print(param9)
sim_database.write("new_test_param9", param9, type_of_value="int")
print(sim_database.read("new_test_param9"))

param10 = sim_database.read("test_param10")
print(param10)
sim_database.write("new_test_param10", param10, type_of_value="int")
print(sim_database.read("new_test_param10"))

param11 = sim_database.read("test_param11")
print(param11)

param12 = sim_database.read("test_param12")
print(param12)

if store_metadata:
    large_test_res = np.array(param6)
    res_dir = sim_database.make_unique_subdir("root/tests/results")
    np.savetxt("{0}/results.txt".format(res_dir), large_test_res)

sim_database.end()

db_id = sim_db.add_empty_sim()
print(db_id)

sim_database = sim_db.SimDB(db_id = db_id, store_metadata=False)

sim_database.write("test_param1", 7, type_of_value="int")
param1 = sim_database.read("test_param1")
print(param1)

sim_database.end()

sim_db.delete_sim(db_id)
