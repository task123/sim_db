```sim_db``` - A Simulation Database
====================================
**sim_db** is a set of commands and functions for conveniently running a large number of simulations with different parameter values, while keeping track of these all simulation parameters and results along with metadata in a database for you. 

Documentation of the project is found [here]<link>.







A set of programs/commands to keep track of the parameters used to run different simulations. The parameters is stored in a SQLite3 database, and the programs/commands does the direct interaction with the database for you. There is currently only a version for python, but any more languages can easily be added.

## Purpose
When doing simulations, one will usually run a great number of simulations with different parameters. (This is especially true when developing the simulations.) After a while it will often become a bit difficult to keep track of all the simulations; the parameters used to run them, the results and metadate such at the time used to perform the simulation. sim_db aim towards providing a flexible and convenient way of keeping track of all the simulation and does this by storing the parameters in a SQLite3 database.



## Use
The are quite of few commands and options, so first the minimum that have to be done is presented and then more advanced options are added.


### All Commands

What any of the commands do, how they are used and all possible arguments for the command are displayed by added ```-h``` to after the commands.

* ``` list_sim_db_commands ``` - Print all the commands.

* ``` print_sim ``` - Print parameters of the simulations, i.e. the content of the database. One should definitly use the command with some options arguments to limit the output. A personalized print configuration is often useful - see settings.

* ``` add_sim ```  -  Add a new set of simulation parameters to the database from ```sim_params.txt```. Other parameters files can be used by adding ```-filename 'FILENAME'```.

* ``` run_sim ``` - Run all simulations with status 'new' unless anything else is specified.

* ``` submit_sim ``` - Submit all simulation with status 'new' to the job scheduler in settings.

* ``` add_and_run ``` - Same as running ```add_sim``` and then ```run_sim -db_id 'ID'``` with the same ```'ID'```.

* ``` add_and_submit ```  - Same as running ```add_sim``` and then ```submit_sim -db_id 'ID'``` with the same ```'ID'```.

* ``` update_sim ``` - Change the value of a single or multiple entires in the database.

* ``` add_comment ``` - Add a comment or error message to a simulation.

* ``` delete_sim ``` - Delete a set of simulations parameters from the database.

* ``` extract_params ``` - Extract the parameters from the database to a parameter file.

* ``` cd_results --id 'ID' ``` - Change directory to where the results of a simulation with id ```'ID'``` is localed.

* ``` add_column ``` - Add a new column to the database.

* ``` combine_dbs  'sim_database_1.db' 'sim_database_2.db' 'new_name.db'``` - Combine two SQLite3 simulation databases after simulation have been run differnt places. 

* ``` delete_empty_columns ``` - Delete all empty columns, execpt the default ones. 

### Recommendations, tips and explainations

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

### Available functions

The functions and classes that are available to be used in a simulation are given for the different languages below.

**Python:**
```
class SimDB(db_in=None)
    read(name_column, db_id=None, check_type_id='')
    write(name_column, value, db_id=None, type_value='')
    make_subdir_result(name_result_directory) # Return full path
    update_sha1_executables(paths_executables) # Not done automatically
    end()
```

**C:**
```
SimDB sim_db_init(int argc, char** argv)
SimDB sim_db_init_with_id(int parameter_id)

int sim_db_read_int(SimDB self, char name_column[])
double sim_db_read_double(SimDB self, char name_column[])
char* sim_db_read_string(SimDB self, char name_column[])
int sim_db_read_bool(SimDB self, char name_column[])
void sim_db_read_int_array(SimDB self, char name_column[], int* arr, size_t len)
void sim_db_read_double_array(SimDB self, char name_column[], double* arr, size_t len),
void sim_db_read_string_array(SimDB self, char name_column[], char** arr, size_t len)
void sim_db_read_bool_array(SimDB self, char name_column[], int* arr, size_t len)

void sim_db_write_int(SimDB self, char name_column[], int value)
void sim_db_write_double(SimDB self, char name_column[], double value)
void sim_db_write_string(SimDB self, char name_column[], char value[])
void sim_db_write_bool(SimDB self, char name_column[], int value)
void sim_db_write_int_array(SimDB self, char name_column[], int* arr, size_t len)
void sim_db_write_double_array(SimDB self, char name_column[], double* arr, size_t len_)
void sim_db_write_string_array(SimDB self, char name_column[], char** arr, size_t len)
void sim_db_write_bool_array(SimDB self, char name_column[], int* arr, size_t len_)

char* sim_db_make_subdir_result(char name_result_directory[])

void sim_db_update_sha1_executables(SimDB self, char** paths_executables, size_t len) 

void sim_db_del(SimDB self)
```

**C++:**
```
class SimDB
    void SimDB(argc, argv)
    void SimDB(int id)
    template T read<T>(std::string name_of_parameter)
    template void write<T>(std::string column, T value)
    std::string make_subdir_result(std::string name_result_directory)
    void update_sha1_executables(std::vector<std::string> paths_executables)
```

### Settings
Setting can be changed by modifing the ```settings.txt``` file.

### Example and Tests

## Database
Many possible useful columns of metadata are added to the SQLite3 database in addition to all the simulation parameters. They take little space to store and can easily be omitted when printing the parameters if not used.

These columns columns and some more are added reguardless of how the simulation is used as a number of commands rely on them being in the database. Some of these reflect that using git and a job scheduler (on a cluster or super computer) is common and convinient for developing and running simulations, but if this is not used one can just avoid to print these columns.

Default columns:

* ```id``` - To uniquely refer to a set of simulation parameters.

* ```status``` - Status of simulation: 'submitted', 'running' or 'finished'.

* ```name``` - To easily distinguage the different simulations.

* ```describtion``` - To further explain the intent of the simulation.

* ```run_command``` - Command to run the simulation.

* ```comment``` - Comment about the simulation and how it ran. Standard error may be included.

* ```add_to_job_script``` - Additional flags, import or load statement added to the job script for the job scheduler.

* ```result_dir``` - The path to where the results are stored. 

* ```time_submitted``` - To tell how long a submition have been in queque.

* ```time_started``` - To tell how long a simulation used in queque and how long it have been running. 

* ```used_walltime``` - To tell the total run time of the simulation.

* ```max_walltime``` - Useful if the simulation is stopped for exceeding this limit. (Also in the context of understanding the time between ```time_submitted``` and ```time_started```.)

* ```job_id``` - To check the simulation when submitted to a job scheduler.

* ```n_tasks``` - Number of threads/cores. Needed to understand 'used_walltime'.

* ```cpu_info``` - Needed to compare ```used_walltime``` across different machines.

* ```git_hash``` - To be sure of which commit the simulation is run from.

* ```commit_message``` - A easier way to distinguage the commits than the hash. 

* ```git_diff_stat``` - Show summary of difference between the working directory and the current commit (HEAD) at the time the simulation is run.

* ```git_diff``` - Show the explicit difference between the working directory and the current commit at the time when the simulation is run.

* ```sha1_executables``` - To tell exacetly which executable that was used to run the simulation. Useful to check that it have been compiled after any changes. Is the sha1 of any files in the ```run_command```.

Any new parameter that are added give an additional column automatically.
