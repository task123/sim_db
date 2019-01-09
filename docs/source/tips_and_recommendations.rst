========================
Tips and Recommendations
========================

A number of tips, recommendations and explainations that might be useful is listed here:

* ``sdb`` is a shorter way of calling the ``sim_db`` command line tool and does not differ in any other way.

* If the *sim_db/* directory is empty after having cloned a projet that uses **sim_db**, go into the *sim_db/* directory and run these two commands; ``$ git submodule init`` and ``$ git submodule update``.

* For C++ the instance of ``SimDB`` must be initialized at the beginning of the simulation and kept to the end. This is because its initializer and destructor take the time of the simulation as well as writing a number of thing to the database, including the simulations status. The same is true for Python, but in addition the ``close()`` method need to be called. For C ``sim_db_ctor()`` and ``sim_db_dtor()`` must for the same reason, be called at the beginning and end of the simulation. ``sim_db_dtor()`` also does clean up and must be called to avoid memory leaks.

* It is recommended to add a '*name* (string): *name of simulation run*' and a '*describtion* (string): *describtion of simulation*' to explain which simulation it is and the intent of the simulation. This makes it much easier to navigate all the simulations that accumulates at a later time.

* The ``run`` and ``add_and_run`` commands will print the output from the *run_command* to the terminal while the program runs, but it may take some time before start printing the output.

* It is recommended to use '*root/*' in the *run_command* to give the path to the *executable_program* relative to the project's root directory. This is because the '*root/*' will be replaced with the full path to the file when running the simulation, which may be necessary when running on a cluster or supercomputer.

* Any stand alone hashtages, ``#``, that occure in the *run_command* will be replaced with the number passed after the ``-n`` flag in the ``run`` command. Ex. : ``mpirun -n # python program.py``.

* Small results can be written to the database, but large results are recommended to be saved in a subdirectory in a result made by ``unique_results_dir`` inside a result directory.

* For all commands that end with *_sim*, this ending can be omitted. ``add`` can for instance be used instead of ``add_sim``.

* The ``cd_results`` command call a bash script to change the directory to the '*result_dir*' and then replace the currect shell process with this new one.

* The command line tool can be called with ``python sim_db/__main__.py'`` instead of just ``'sim_db'`` or ``'sdb'``, if it is perferable.

* Multiple default names for the parameter files can be added in prioritized order in *settings.txt* to replace or in addition to *sim_params.txt*.

* If add error message occur during the simulation, consider adding the error message as a comment, ``add_comment --id 'ID' --filename 'standard_error.out'``. An explaination may be appended in addition.
