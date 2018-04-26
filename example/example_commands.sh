#! /usr/bin/env bash
#
# Example of how to use the 'add_and_run' command and then how to use the the 
# 'add_sim' and 'run_sim' individually while using 'print_sim' to print from 
# the database at each stage. Both set of simulation are deleted in the end of 
# the example.
# 
# The last of these two examples shows how to run a set of commands to add the 
# parameters in 'example_sim_params.txt' to the database, print some of the 
# parameters, run this "simulation", print the status, update the status, print 
# the status again and delete the simulation parameters from the database .

echo -e "Add example parameters to database and run the simulation."
add_and_run --filename ${BASH_SOURCE%/*}/example_sim_params.txt

# Get hold of the ID of the exampel parameters.
id_from_add_and_run=`print_sim -n 1 --columns id --no_headers`

echo -e "\nAdd example parameters to database.\n"
add_sim --filename ${BASH_SOURCE%/*}/example_sim_params.txt

echo -e "Print the 3 last entries in the database to view the added example parameters.\n"
print_sim -n 3 --max_width 7 --columns id "status" name param1 param2 param3 param4 param5 param6 param7 param8

# Get hold of the ID of the exampel parameters.
id_from_add_sim=`print_sim -n 1 --columns id --no_headers`

echo -e "\nRun example program that prints out the paramters."
run_sim --id ${id_from_add_sim}

echo -e "\nPrint the last entry in the database to view the updated status.\n"
print_sim -n 1 --max_width 7 --columns id "status" name param1 param2 param3 param4 param5 param6 param7 param8


echo -e "\nDelete the example parameters that where added to the database.\n"
delete_sim --id ${id_from_add_and_run}
delete_sim --id ${id_from_add_sim}

echo -e "Print the last entry in the database to check that the example parameters where deleted.\n"
print_sim -n 1 --max_width 7 --columns id "status" name param1 param2 param3 param4 param5 param6 param7 param8


