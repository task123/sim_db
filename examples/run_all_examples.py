#! /usr/bin/env python
#
# Example of how to use sim_db's 'add' and 'run' commands to run the examples 
# for python, C and C++.
#
# The 'print' command is run silenty to get the id of added parameters and 
# 'delete' is used to delete the added parameters.
#
# Copyright (C) 2017, 2018 Håkon Austlid Taskén <hakon.tasken@gmail.com>
# Licenced under the MIT License.

import subprocess
import sys

def run(explanation, command):
    print(explanation)
    print("$", command)
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, 
                               universal_newlines=True)
    output = ""
    for line in iter(process.stdout.readline, ''):
        sys.stdout.write(line)
        sys.stdout.flush()
        output = output + line
    print("")
    return output.strip()

print("""
######################### Run minimal python example ###########################
""")

run(
"# Add example parameters to database for minimal python example.",
"sim_db add --filename root/examples/params_minimal_python_example.txt")

id_for_minimal_python_example = run(
"# Get hold of the ID of the example parameters for minimal python example.",
"sim_db print -n 1 --columns id --no_headers")

run(
"# Run minimal_example.py.",
"sim_db run --id {0}".format(id_for_minimal_python_example))

run(
"# Delete example simulation from database.",
"sim_db delete --id {0} --no_checks".format(id_for_minimal_python_example))

print("""
########################### Run minimal C++ example ############################ 
""")

run(
"# Add example parameters to database for minimal C++ example.",
"sim_db add --filename root/examples/params_minimal_cpp_example.txt")

id_for_minimal_cpp_example = run(
"# Get hold of the ID of the exampel parameters for minimal C++ example.",
"sim_db print -n 1 --columns id --no_headers")

run(
"# Run minima_example.cpp (after compiling it with make command).",
"sim_db run --id {0}".format(id_for_minimal_cpp_example))

run(
"# Delete example simulation from database.",
"sim_db delete --id {0} --no_checks".format(id_for_minimal_cpp_example))

print("""
########################### Run minimal C example ############################## 
""")

run(
"# Add example parameters to database for minimal C example.",
"sim_db add --filename root/examples/params_minimal_c_example.txt")

id_for_minimal_c_example = run(
"# Get hold of the ID of the exampel parameters for minimal C example.",
"sim_db print -n 1 --columns id --no_headers")

run(
"# Run minimal_example.c (after compiling it with make command).",
"sim_db run --id {0}".format(id_for_minimal_c_example))

run(
"# Delete example simulation from database.",
"sim_db delete --id {0} --no_checks".format(id_for_minimal_c_example))

print("""
######################## Run extensive python example ########################## 
""")

run(
"# Add example parameters to database for extensive python example.",
"sim_db add --filename root/examples/params_extensive_python_example.txt")

id_for_extensive_python_example = run(
"# Get hold of the ID of the exampel parameters for extensive python example.",
"sim_db print -n 1 --columns id --no_headers")

run(
"# Run extensive_example.py.",
"sim_db run --id {0}".format(id_for_extensive_python_example))

run(
"# Delete example simulation from database.",
"sim_db delete --id {0} --no_checks".format(id_for_extensive_python_example))

print("""
########################## Run extensive C++ example ########################### 
""")

run(
"# Add example parameters to database for extensive C++ example.",
"sim_db add --filename root/examples/params_extensive_cpp_example.txt")

id_for_extensive_cpp_example = run(
"# Get hold of the ID of the exampel parameters for extensive C++ example.",
"sim_db print -n 1 --columns id --no_headers")

run(
"# Run minima_example.cpp (after compiling it with make command).",
"sim_db run --id {0}".format(id_for_extensive_cpp_example))

run(
"# Delete example simulation from database.",
"sim_db delete --id {0} --no_checks".format(id_for_extensive_cpp_example))

print("""
########################## Run extensive C example ############################# 
""")

run(
"# Add example parameters to database for extensive C example.",
"sim_db add --filename root/examples/params_extensive_c_example.txt")

id_for_extensive_c_example = run(
"# Get hold of the ID of the exampel parameters for extensive C example.",
"sim_db print -n 1 --columns id --no_headers")

run(
"# Run extensive_example.c (after compiling it with make command).",
"sim_db run --id {0}".format(id_for_extensive_c_example))

run(
"# Delete example simulation from database.",
"sim_db delete --id {0} --no_checks".format(id_for_extensive_c_example))
