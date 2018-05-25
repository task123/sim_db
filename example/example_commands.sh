#! /usr/bin/env bash
#
# Example of how to use 'add_sim' and 'run_sim' to run the examples for 
# python, C and C++.
#
# 'print_sim' is run silenty to get the id of added parameters and 'delete_sim'
# is used to delete the added parameters.
#
# Copyright (C) 2017, 2018 Håkon Austlid Taskén <hakon.tasken@gmail.com>
# Licenced under the MIT License.

######################### Run minimal python example ########################## 

# Add example parameters to database for miniaml python example.
add_sim --filename params_minimal_python_example.txt

# Get hold of the ID of the exampel parameters for minimal python example.
id_for_minimal_python_example=`print_sim -n 1 --columns id --no_headers`

# Run minimal_example.py.
run_sim --id ${id_for_minimal_python_example}

########################### Run minimal C++ example ########################### 

# Add example parameters to database for minimal C++ example.
add_sim --filename params_minimal_cpp_example.txt

# Get hold of the ID of the exampel parameters for minimal C++ example.
id_for_minimal_cpp_example=`print_sim -n 1 --columns id --no_headers`

# Run minima_example.cpp (after compiling it with make command).
run_sim --id ${id_for_minimal_cpp_example}

########################### Run minimal C example ############################# 

# Add example parameters to database for minimal C example.
add_sim --filename params_minimal_c_example.txt

# Get hold of the ID of the exampel parameters for minimal C example.
id_for_minimal_c_example=`print_sim -n 1 --columns id --no_headers`

# Run minimal_example.c (after compiling it with make command).
run_sim --id ${id_for_minimal_c_example}

######################### Run extensive python example ########################## 

# Add example parameters to database for miniaml python example.
add_sim --filename params_extensive_python_example.txt

# Get hold of the ID of the exampel parameters for extensive python example.
id_for_extensive_python_example=`print_sim -n 1 --columns id --no_headers`

# Run extensive_example.py.
run_sim --id ${id_for_extensive_python_example}

########################### Run extensive C++ example ########################### 

# Add example parameters to database for extensive C++ example.
add_sim --filename params_extensive_cpp_example.txt

# Get hold of the ID of the exampel parameters for extensive C++ example.
id_for_extensive_cpp_example=`print_sim -n 1 --columns id --no_headers`

# Run minima_example.cpp (after compiling it with make command).
run_sim --id ${id_for_extensive_cpp_example}

########################### Run extensive C example ############################# 

# Add example parameters to database for extensive C example.
add_sim --filename params_extensive_c_example.txt

# Get hold of the ID of the exampel parameters for extensive C example.
id_for_extensive_c_example=`print_sim -n 1 --columns id --no_headers`

# Run extensive_example.c (after compiling it with make command).
run_sim --id ${id_for_extensive_c_example}

################## Delete example simulations from database ################### 

delete_sim --id ${id_for_minimal_python_example}
delete_sim --id ${id_for_minimal_cpp_example}
delete_sim --id ${id_for_minimal_c_example}
delete_sim --id ${id_for_extensive_python_example}
delete_sim --id ${id_for_extensive_cpp_example}
delete_sim --id ${id_for_extensive_c_example}

################################## Clean up ################################### 

# Remove results created
rm -fr results/*
