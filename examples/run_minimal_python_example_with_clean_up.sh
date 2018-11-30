#! /usr/bin/env bash
#
# Example of how to use 'sim_db add' and 'sim_db run' to run the minimal 
# example for Python.
#
# 'sim_db print' is run silenty to get the id of added parameters and 
# 'sim_db delete' is used to delete the added parameters.
#
# Copyright (C) 2018 Håkon Austlid Taskén <hakon.tasken@gmail.com>
# Licenced under the MIT License.

######################### Run minimal Python example ########################## 

# Add example parameters to database for miniaml Python example.
sim_db add --filename root/examples/params_minimal_python_example.txt

# Get hold of the ID of the exampel parameters for minimal Python example.
id_for_minimal_python_example=`sdb print -n 1 --columns id --no_headers`

# Run minimal_example.py.
sim_db run --id ${id_for_minimal_python_example}

################## Delete example simulation from database #################### 

# Remove the example parameters, that was previously added, from the database
sim_db delete --id ${id_for_minimal_python_example} --no_checks
