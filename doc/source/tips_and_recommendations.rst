========================
Tips and Recommendations
========================

A number of tips, recommendations and explainations that might be useful is listed here:

* If the *sim_db/* directory is empty after having cloned a projet that uses **sim_db**, go into the *sim_db/* directory and run these two commands; ``$ git submodule init`` and ``$ git submodule update``.

* For Python and C++ the instance of ``SimDB`` must be kept initialized at the beginning of the simulation and kept to the end. This is because its initializer and destructor take the time of the simulation as well as writing a number of thing to the database, including the simulations status. For C ``sim_db_start()`` and ``sim_db_end()`` must for the same reason be called at the beginning and end of the simulation.

* It is recommended to add a '*name* (string): *name of simulation run*' and a '*describtion* (string): *describtion of simulation*' to explain which simulation it is and the intent of the simulation. This makes it much easier to navigate all the simulations that accumulates at a later time.

* The ``run_sim`` and ``add_and_run`` commands will print the output from the *run_command* to the terminal while the program runs, but it may take some time before start printing the output.

* It is recommended to use '*./*' '*root/*' or '*sim_db/*' in the *run_command* to give the path to the *executable_program* relative to the directory of *sim_params.txt* or **sim_db**. This is because the '*./*', '*root/*' or '*sim_db/*' will be replaced with the full path to the file when running the simulation, which may be necessary when running on a cluster or supercomputer.

* Any stand alone hashtages, ``#``, that occure in the *run_command* will be replaced with the number passed after the ``-n`` flag in the ``run_sim`` command. Ex. : ``mpirun -n # python program.py``.

* All the command can be called with ``python 'path_to_sim_db_dir/command.py'`` instead of just ``'command'``, if it is perferable or windows without Cygwin or MinGW.

* Multiple default names for the parameter files can be added in prioritized order in *settings.txt* to replace or in addition to *sim_params.txt*.

* **sim_db** commands can be called from the directory where **sim_db** is included (the top directory of your project) or any of its subdirectories. (Provided that ``$ make`` have been run in 'sim_db/'.)

* If one do not wish to include **sim_db** in the top directory of your project, one can add in in a subdirectory and add a text file named '.sim_db' in the top directory with a path to the locaton of the '*sim_db/*' directory. ('*root/...*' will be replace with '*sim_db/..*' reguardless.)

* If the ``sim_db`` directory is moved, the `` python generate_commands.py `` should be run again to add the new location to the path in the '~/.bash_rc' or '~/.bash_profile' file. One can also remove the old path.

* Remember that if the ``print_sim`` commands does not print anything, it might be because the database is empty. That it don't have any simulation parameters added.

* Small results can be written to the database, but large results are recommended to be saved in a subdirectory in a result made by ``make_subdir_result`` inside a result directory.

* If add error message occur during the simulation, consider adding the error message as a comment, ``add_comment --id 'ID' --filename 'standard_error.out'``. An explaination may be appended in addition.

* The ``cd_results`` command is a bash function that call the 'cd_results.py' to get the path to the '*result_dir*'. The reason it is a bash funciton is that when ``cd`` is called from a shell or python script only the directory of the subshell, in which the script is running, is changed.

* Remember to compile any C code with the flag '-l sqlite3'.
