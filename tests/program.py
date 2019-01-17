# -*- coding: utf-8 -*-
""" Testing 'sim_db' for python, that is 'sim_db.py'.

Read in parameters from database, write parameters to database, make unique 
subdirectory for results and save 'results.txt' in this directory.

Finally add empty simulation, write to it and read from it and then delete it.
"""
# Copyright (C) 2017, 2018 Håkon Austlid Taskén <hakon.tasken@gmail.com>
# Licenced under the MIT License.

import add_package_root_to_path
import sim_db.sim_db_lib as sim_db_lib
import sim_db.__init__ 
import argparse
import os.path
import sys
import numpy as np

if 'no_metadata' in sys.argv:
    store_metadata = False
else:
    store_metadata = True

if 'running_in_parallel' in sys.argv:
    running_in_parallel = True
else:
    running_in_parallel = False

print(sim_db.__init__.__version__)

sim_database = sim_db_lib.SimDB(store_metadata=store_metadata)

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
sim_database.write("new_test_param5", np.array(param5), type_of_value="int array")
print(sim_database.read("new_test_param5"))

param6 = sim_database.read("test_param6")
print(param6)
sim_database.write("new_test_param6", param6, type_of_value="float array")
sim_database.write("new_test_param6", np.array(param6), type_of_value="float array")
print(sim_database.read("new_test_param6"))

param7 = sim_database.read("test_param7")
print(param7)
sim_database.write("new_test_param7", param7, type_of_value="string array")
sim_database.write("new_test_param7", np.array(param7), type_of_value="string array")
print(sim_database.read("new_test_param7"))

param8 = sim_database.read("test_param8")
print(param8)
sim_database.write("new_test_param8", param8, type_of_value="bool array")
sim_database.write("new_test_param8", np.array(param8), type_of_value="bool array")
print(sim_database.read("new_test_param8"))

param9 = sim_database.read("test_param9")
print(param9)
sim_database.write("new_test_param9", param9, type_of_value="int")
print(sim_database.read("new_test_param9"))

param10 = sim_database.read("test_param10")
print(param10)
sim_database.write("new_test_param10", param10, type_of_value="int")
print(sim_database.read("new_test_param10"))

param12 = sim_database.read("test_param12")
print(param12)

param13 = sim_database.read("test_param13")
print(param13)
sim_database.write("test_param13", [1, 2, 3])
print(sim_database.read("test_param13"))

print(sim_database.is_empty("test_param11"))
sim_database.set_empty("test_param11")
print(sim_database.is_empty("test_param11"))

if store_metadata:
    large_test_res = np.array(param6)
    res_dir = sim_database.unique_results_dir("root/tests/results")
    np.savetxt("{0}/results.txt".format(res_dir), large_test_res)

print(sim_database.column_exists("test_param1"))
print(sim_database.column_exists("test_column_does_not_exists"))

try:
    sim_database.read("test_column_does_not_exists")
except sim_db_lib.ColumnError:
    print("raised ColumnError")

sim_database.close()

if not running_in_parallel:
    sim_database = sim_db_lib.add_empty_sim(False)
    print(sim_database.get_id())

    sim_database.write("test_param1", 7, type_of_value="int", 
                       only_if_empty=True)
    param1 = sim_database.read("test_param1")
    print(param1)

    sim_database.delete_from_database()
    sim_database.close()
