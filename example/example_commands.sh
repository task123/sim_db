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

############################# Run python example ############################## 

# Add example parameters to database for python example.
add_sim --filename sim_params_example_python_program.txt

# Get hold of the ID of the exampel parameters for python example.
id_for_python_example=`print_sim -n 1 --columns id --no_headers`

# Run program.py.
run_sim --id ${id_for_python_example}

############################### Run C example ################################# 

# Add example parameters to database for C example.
add_sim --filename sim_params_example_c_program.txt

# Get hold of the ID of the exampel parameters for C example.
id_for_c_example=`print_sim -n 1 --columns id --no_headers`

# Run program.c (after compiling it with make command).
run_sim --id ${id_for_c_example}

############################## Run C++ example ################################ 

# Add example parameters to database for C example.
add_sim --filename sim_params_example_cpp_program.txt

# Get hold of the ID of the exampel parameters for C example.
id_for_cpp_example=`print_sim -n 1 --columns id --no_headers`

# Run program.c (after compiling it with make command).
run_sim --id ${id_for_cpp_example}

################## Delete example simulations from database ################### 

delete_sim --id ${id_for_python_example}
delete_sim --id ${id_for_c_example}
delete_sim --id ${id_for_cpp_example}

################################## Clean up ################################### 

make clean
