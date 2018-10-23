#! /usr/bin/env bash
#
# Example of how to use 'add_sim' and 'run_sim' to run the extensive examples
# for Python, C and C++.
#
# 'print_sim' is run silenty to get the id of added parameters and 'delete_sim'
# is used to delete the added parameters.
#
# Copyright (C) 2018 Håkon Austlid Taskén <hakon.tasken@gmail.com>
# Licenced under the MIT License.

######################## Run extensive Python example ######################### 

# Add example parameters to database for miniaml Python example.
add_sim --filename params_extensive_python_example.txt

# Get hold of the ID of the exampel parameters for extensive Python example.
id_for_extensive_python_example=`print_sim -n 1 --columns id --no_headers`

# Run extensive_example.py.
run_sim --id ${id_for_extensive_python_example}

################## Delete example simulation from database #################### 

# Remove the example parameters, that was previously added, from the database
delete_sim --id ${id_for_extensive_python_example} --no_checks

########################## Run extensive C example ############################ 

# Add example parameters to database for miniaml C example.
add_sim --filename params_extensive_c_example.txt

# Get hold of the ID of the exampel parameters for extensive C example.
id_for_extensive_c_example=`print_sim -n 1 --columns id --no_headers`

# Run extensive_example.py.
run_sim --id ${id_for_extensive_c_example}

################## Delete example simulation from database #################### 

# Remove the example parameters, that was previously added, from the database
delete_sim --id ${id_for_extensive_c_example} --no_checks

######################### Run extensive C++ example ########################### 

# Add example parameters to database for miniaml C++ example.
add_sim --filename params_extensive_cpp_example.txt

# Get hold of the ID of the exampel parameters for extensive C++ example.
id_for_extensive_cpp_example=`print_sim -n 1 --columns id --no_headers`

# Run extensive_example.py.
run_sim --id ${id_for_extensive_cpp_example}

################## Delete example simulation from database #################### 

# Remove the example parameters, that was previously added, from the database
delete_sim --id ${id_for_extensive_cpp_example} --no_checks
