#! /usr/bin/env bash
#
# Example of how to use 'add_sim' and 'run_sim' to run the minimal example for 
# Python.
#
# 'print_sim' is run silenty to get the id of added parameters and 'delete_sim'
# is used to delete the added parameters.
#
# Copyright (C) 2018 Håkon Austlid Taskén <hakon.tasken@gmail.com>
# Licenced under the MIT License.

######################### Run minimal python example ########################## 

# Add example parameters to database for miniaml python example.
add_sim --filename params_minimal_python_example.txt

# Get hold of the ID of the exampel parameters for minimal python example.
id_for_minimal_python_example=`print_sim -n 1 --columns id --no_headers`

# Run minimal_example.py.
run_sim --id ${id_for_minimal_python_example}

################## Delete example simulation from database #################### 

# Remove the example parameters, that was previously added, from the database
delete_sim --id ${id_for_minimal_python_example}
