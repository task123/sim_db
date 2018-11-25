#! /usr/bin/env bash
#
# Example of how to use 'sdb add' and 'sdb run' to run the extensive examples
# for Python, C and C++.
#
# 'sdb print' is run silenty to get the id of added parameters and 'sdb delete'
# is used to delete the added parameters.
#
# Copyright (C) 2018 Håkon Austlid Taskén <hakon.tasken@gmail.com>
# Licenced under the MIT License.

######################## Run extensive Python example ######################### 

# Add example parameters to database for miniaml Python example.
sdb add --filename params_extensive_python_example.txt

# Get hold of the ID of the exampel parameters for extensive Python example.
id_for_extensive_python_example=`sdb print -n 1 --columns id --no_headers`

# Run extensive_example.py.
sdb run --id ${id_for_extensive_python_example}

################## Delete example simulation from database #################### 

# Remove the example parameters, that was previously added, from the database
sdb delete --id ${id_for_extensive_python_example} --no_checks

########################## Run extensive C example ############################ 

# Add example parameters to database for miniaml C example.
sdb add --filename params_extensive_c_example.txt

# Get hold of the ID of the exampel parameters for extensive C example.
id_for_extensive_c_example=`sdb print -n 1 --columns id --no_headers`

# Run extensive_example.py.
sdb run --id ${id_for_extensive_c_example}

################## Delete example simulation from database #################### 

# Remove the example parameters, that was previously added, from the database
sdb delete --id ${id_for_extensive_c_example} --no_checks

######################### Run extensive C++ example ########################### 

# Add example parameters to database for miniaml C++ example.
sdb add --filename params_extensive_cpp_example.txt

# Get hold of the ID of the exampel parameters for extensive C++ example.
id_for_extensive_cpp_example=`sdb print -n 1 --columns id --no_headers`

# Run extensive_example.py.
sdb run --id ${id_for_extensive_cpp_example}

################## Delete example simulation from database #################### 

# Remove the example parameters, that was previously added, from the database
sdb delete --id ${id_for_extensive_cpp_example} --no_checks
