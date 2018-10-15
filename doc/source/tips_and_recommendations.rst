========================
Tips and Recommendations
========================

* For Python and C++ the instance of ```SimDB``` must be kept initialized at the beginning of the simulation and kept to the end. This is because its initializer and destructor take the time of the simulation as well as writing a number of thing to the database, including the simulations status. For C ```sim_db_start()``` and ```sim_db_end()``` must for the same reason be called at the beginning and end of the simulation.

* It is recommended to add a ```name (string): name of simulation run``` and a ```describtion (string): describtion of simulation``` to explain which simulation it is and the intent of the simulation. This makes it much easier to navigate all the simulations that accumulates at a later time.

* It is recommended to use ```.``` and ```..``` in the run_command to give the path in ```executable_program``` relative to the directory of ```sim_params.txt```. This is because the ```.``` and ```..``` will be replaced with the full path to the file when running the simulation, which often is necessary when running on a cluster or supercomputer.

* All the command can be called with ```python 'path_to_sim_db_dir/command.py'``` instead of just ```'command'``` if it is perferable or windows without Cygwin or MinGW.

* Multiple default names for the parameter files can be added in prioritized order in ```settings.txt``` to replace or in addition to ```sim_params.txt```.

* The text file with the parameters can be named anything, but if it is not named ```sim_params.txt``` (or any of the parameter filenames in the settings), the name of the file needs to be passed to any commands.

* When one have multiple projects using ```sim_db```, the commands will use the closest copy of ```sim_db```. (Provided ```python generate_commands.py``` have been run in that directory.)

* If the ```sim_db``` directory is moved, the ``` python generate_commands.py ``` should be run again to add the new location and remove the old one.

* The reason that any paths in the ```run_command``` must start with ```./``` or ```sim_db/``` is to ensure that the simulations can be run even when the project is copied to another place and/or the commands are submittedt to a job scheduler.

* Remember that if the ```print_sim``` commands does not print anything, it might be because the database is empty. That it don't have any simulation parameters added.

* Small results can be written to the database, but large results are recommended to be saved in a subdirectory in a result made by ```make_subdir_result``` inside a result directory.

* If add error message occur during the simulation, consider adding the error message as a comment, ```add_comment --id 'ID' --filename 'standard_error.out'```. An explaination may be appended in addition.

* The 'cd_results' command is a bash function that call the 'cd_results.py' to get the path to the 'result_dir'. The reason it is a bash funciton is that when 'cd' is called from a shell or python script only the directory of the subshell, in which the script is running, is changed.

* Remember to compile any C code with the flag '-l sqlite3'.
