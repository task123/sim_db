#! /usr/bin/env bash
#
# Example of how to use sim_db's 'add' and 'run' commands to run the examples 
# for python, C and C++.
#
# The 'print' command is run silenty to get the id of added parameters and 
# 'delete' is used to delete the added parameters.
#
# Copyright (C) 2017, 2018 Håkon Austlid Taskén <hakon.tasken@gmail.com>
# Licenced under the MIT License.

######################### Run minimal python example ########################### 

# Add example parameters to database for minimal python example.
sim_db add --filename root/examples/params_minimal_python_example.txt

# Get hold of the ID of the exampel parameters for minimal python example.
id_for_minimal_python_example=`sim_db print -n 1 --columns id --no_headers`

# Run minimal_example.py.
sim_db run --id ${id_for_minimal_python_example}

# Delete example simulation from database.
sim_db delete --id ${id_for_minimal_python_example} --no_checks

########################### Run minimal C++ example ############################ 

# Add example parameters to database for minimal C++ example.
sim_db add --filename root/examples/params_minimal_cpp_example.txt

# Get hold of the ID of the exampel parameters for minimal C++ example.
id_for_minimal_cpp_example=`sim_db print -n 1 --columns id --no_headers`

# Run minima_example.cpp (after compiling it with make command).
sim_db run --id ${id_for_minimal_cpp_example}

# Delete example simulation from database.
sim_db delete --id ${id_for_minimal_cpp_example} --no_checks

########################### Run minimal C example ############################## 

# Add example parameters to database for minimal C example.
sim_db add --filename root/examples/params_minimal_c_example.txt

# Get hold of the ID of the exampel parameters for minimal C example.
id_for_minimal_c_example=`sim_db print -n 1 --columns id --no_headers`

# Run minimal_example.c (after compiling it with make command).
sim_db run --id ${id_for_minimal_c_example}

# Delete example simulation from database.
sim_db delete --id ${id_for_minimal_c_example} --no_checks

######################## Run extensive python example ########################## 

# Add example parameters to database for extensive python example.
sim_db add --filename root/examples/params_extensive_python_example.txt

# Get hold of the ID of the exampel parameters for extensive python example.
id_for_extensive_python_example=`sim_db print -n 1 --columns id --no_headers`

# Run extensive_example.py.
sim_db run --id ${id_for_extensive_python_example}

# Delete example simulation from database.
sim_db delete --id ${id_for_extensive_python_example} --no_checks

########################## Run extensive C++ example ########################### 

# Add example parameters to database for extensive C++ example.
sim_db add --filename root/examples/params_extensive_cpp_example.txt

# Get hold of the ID of the exampel parameters for extensive C++ example.
id_for_extensive_cpp_example=`sim_db print -n 1 --columns id --no_headers`

# Run minima_example.cpp (after compiling it with make command).
sim_db run --id ${id_for_extensive_cpp_example}

# Delete example simulation from database.
sim_db delete --id ${id_for_extensive_cpp_example} --no_checks

########################## Run extensive C example ############################# 

# Add example parameters to database for extensive C example.
sim_db add --filename root/examples/params_extensive_c_example.txt

# Get hold of the ID of the exampel parameters for extensive C example.
id_for_extensive_c_example=`sim_db print -n 1 --columns id --no_headers`

# Run extensive_example.c (after compiling it with make command).
sim_db run --id ${id_for_extensive_c_example}

# Delete example simulation from database.
sim_db delete --id ${id_for_extensive_c_example} --no_checks
