===
Use
===

Include in your project
=======================
It is recommended to add **sim_db** as a git submodule in your project by running::

    $ git submodule add https://github.com/klasdj

(Otherwise it can taken from `github<https://github.com/alsfj>` and just copied into your project in a directory called '`sim_db`'.)

Go into the sim_db directory and run make::

    $ cd sim_db
    $ make

Answer yes when asked to add `sim_db/commands` to your PATH in `~/.bashrc` or `~/.bash_profile` and remember to source it. (Or if you already have projects using **sim_db**, let it add the path to this **sim_db** directory to the settings.txt of the other local **sim_db** copies.)

All **sim_db** commands should now be available and the C and C++ libraries should be compiled. Test the following command::

    $ list_sim_db_commands

It should list all the **sim_db** commands. How to use any of them can be found either by running the with the `--help` or `-h` flag or reading the documentation of the :ref:`commands <Commands>`. Most of the commands need to have some sets of simulation parameters added to the database to work, so read the examples below to see how to do that.

(All the commands are just calls to python scripts, so they can all be called as :code:`$ python path_to_sim_db_dir/src/commands/'name_command'`.)

How it is used - an brief overview
==================================
**sim_db** is used as follows:
 
* All simulation parameters is placed in a text file with formatting described in :ref:`here<Parameter files>`.

* The parameters are added to **sim_db's** database and the simulation is run with the :code:`$ add_and_run` command.

* In the simulation code the parameters are read from the database with the functions/methods documented :ref:`here for Python <sim_db for Python>`, :ref:`here for C++ <sim_db for C++>` and :ref:`here for C<sim_db for C>`.

That is the brief overview. Reading the examples below and the links above will fill in the details. 

Minimal example using Python
============================
A parameter file called `params_mininal_python_example.txt` is located in the `sim_db/test/` directory in the `source code<https://github.com/jalsjf>`. The file contains the following:

.. literalinclude:: ../../example/params_minimal_python_example.txt
   :language: none

A python script called `minimal_example.py` and is found in the same directory:

.. literalinclude:: ../../example/minimal_example.py
   :language: python
   :lines: 15-28

Add the those simulations parameters to the **sim_db** database and run the simulation with::

    $ add_and_run --filename sim_db/test/params_minimal_python_example.py

Which can also be done from within the `test/` directory with::

    $ add_and_run -f params_minimal_python_example.py

Minimal examples for C++ and C can also be found in the same directory.

Extensive example using C++
==============================
This example is as the name suggerst much more extensive. It is not as straightforward as the minimal example, but it will demostrate a lot more and will also include explainations of more details.

A parameter file called params_extensive_cpp_example.txt is found in the `sim_db/test/` directory in the `source code<https://github.com/jalsjf>`. This parameter file contains all the possible types available in addition to some comments:

.. literalinclude:: ../../example/params_extensive_cpp_example.txt
   :language: none

Notice that the parameters names are different from the :ref:`minimal example<Minimal example using Python>`. This is because `param1` and `param2` are differnt types in this example and the type of a parameter can not change in the database. (In practice this is a very good thing. However, if one add the wrong type to the database the first time, `delete_sim` and `delete_empty_columns` must be used before making a new column with correct type.)

In the same directory `extensive_example.cpp` is also found:

.. literalinclude:: ../../example/extensive_example.cpp
   :language: c++
   :lines: 16-57

Adding the simulation parameters to the **sim_db** database and running the simulation can be just as in the minimal example::

    $ add_and_run -f sim_db/test/params_extensive_cpp_example.txt

Notice that when it is run, it first call `make` to compile the code if needed. What `make` does is equvalient to the following command called from `sim_db/test/` (given that the static C++ library are compiled)::

    $ c++ -o extensive_cpp_example extensive_example.cpp -lsimdbcpp -I../include -L../lib -std=c++11

The :code:`add_and_run` command is usually divided into adding the simulations parameters to the database with::

    $ add_sim

and running the simulation::

    $ run_sim --id 'ID'

where '`ID`' is the a unique number given to each set of simulation parameters added to the database. The '`ID`' is printed when using `add_sim`, but to check the '`ID`' of the latest set of paramters added one can run::

    $ print_sim -n 1 -c id

`print_sim` have lots of flags to control and limit what is printed. The ``-n 1`` flag prints the last entry. ``-c id`` limit the output to just the column named `id`. ``-v -i 'ID'`` are two other useful flags that prints the columns in the database as rows for the set of parameters that have id 'ID'. To avoid typing out lots of flags and column names/parameter names for each time one would like to print something, one can set `Personlized print configurations` in `settings.txt`. `Personlized print configurations` are a set of print_sim flags that are given a name and can be set as default or called as::

    $ print_sim -p 'name_of_personalized_config' 

When running ``$ run_sim --id 'ID'``, the flags ``--id 'ID' -p 'path_to_sim_db`` is added to the `run_command` before it is run, so that the program know where the database is and which 'ID' to read from. So, the the executable prodused by `make` or the compile command stated above. Can be run directoy as::

    $ ./extensive_cpp_example --id 'ID' -p ".."

The example stored some results in a unique subdirectory, which is the recommended way to store large results. To change the directory to that subdirectory, so one can check out the results, just run::

    $ cd_results --id 'ID' 

To run this example or any other simulation on a cluster or a super computer with a job scheduler, just fill out the `Settings for job scheduler` in `settings.txt` and run::

    $ submit_sim --id 'ID' --max_walltime 00:00:10 --n_tasks 1 

The command will create a job script and submit it to the job scheduler. **sim_db** supports job scheduler SLURM and PBS, but it should be quite easy to add more. `n_tasks` is here the number of logical CPUs you want to run on, and can together with `max_walltime` also be set in the parameter file.

It does not make any sense to run such a small single threaded example on a super computer. If one uses a super computer, one are much more likely to want to run a large simulation on two entire nodes::

    $ submit_sim --id 'ID' --max_walltime 10:30:00 --n_nodes 2

If a number of simulations are added all including the paramters `max_walltime` and `n_tasks`, one can simply run::

    $ submit_sim

, which will run all simulations that have not been run yet after a confimation question.

Extensive examples for Python and C can also be found in the same directory, `sim_db/examples/`, on `github<https://github.com/lkajsdlf>`.

Dependencies
============
The dependencies for **sim_db** is tried to keep at a minimum and it is overwhelming likely that everything is available if on a Linux machine or a Mac. The reason for the minimal minimal dependencies and the detailed list of actual dependencies, is that the it is expected to use in project using clusers and super computers. On these clusters and super computers one typically don't have root access and only limited ability to install the dependencies.

* **SQLite** - Uses a SQLite database, so it need to be installed on the system. Almost all the flavours of Linux OS are being shipped with SQLite and MacOS comes pre-installed with SQLite. The SQLite Amalgamation (source code of SQLite in C) is even included to provide a painfree compilation of the C and C++ libraries.

* **Python 2.6 or greater** - A Python interpreter of version 2.6 or greater (that means that is also does work with Python 3) is needed as all the commands are written in Python. Pre-installed on almost all Linux distros and on MacOS.

* **C and C++ compiler** - C99 and C++98 compilers are need for using **sim_db** with C or C++ code, but in that case these compilers are of couse needed anyways. Only the examples need a C++11 compiler.

Recommended:

* **Git** - Your project must use Git to get the full range of metadata. If Git is not used, metadata from Git (and the executable's SHA1 hash) is not collected. (So, nothing dramatic. It might, however, be useful.)

* **Make** - Makes the build process much easier.

Windows:
++++++++
* **Cygwin/MinGW** - The commands relie on Unix (POSIX) style paths, which Cygwin/MinGW/powershell mimicks.

(Not tested on windows yet.)

License
=======
The project is licensed under the MIT license. A copy of the license is provided `here <https://github.com/asjfka>`_.
