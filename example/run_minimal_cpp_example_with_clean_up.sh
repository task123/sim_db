#! /usr/bin/env bash
#
# Example of how to use 'sim_db add' and 'sim_db run' to run the minimal 
# example for C++.
#
# 'sim_db print' is run silenty to get the id of added parameters and 
# 'sim_db delete' is used to delete the added parameters.
#
# Copyright (C) 2018 Håkon Austlid Taskén <hakon.tasken@gmail.com>
# Licenced under the MIT License.

######################### Run minimal python example ########################## 

# Add example parameters to database for miniaml C++ example.
sim_db add --filename params_minimal_cpp_example.txt

# Get hold of the ID of the exampel parameters for minimal C++ example.
id_for_minimal_cpp_example=`sdb print -n 1 --columns id --no_headers`

# Run minimal_example.cpp.
sim_db run --id ${id_for_minimal_cpp_example}

################## Delete example simulation from database #################### 

# Remove the example parameters, that was previously added, from the database
sim_db delete --id ${id_for_minimal_cpp_example} --no_checks
