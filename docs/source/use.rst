.. _use:

===
Use
===

An Brief Overview
==================================
**sim_db** is used as follows:

* Run ``$ sim_db init`` in project's root directoy.
 
* All simulation parameters is placed in a text file with formatting described in :ref:`here<Parameter files>`.

* The parameters are added to **sim_db's** database and the simulation is run with the :code:`$ sim_db add_and_run` command, or with some of the other :ref:`commands <Commands>`.

* In the simulation code the parameters are read from the database with the functions/methods documented :ref:`here for Python <sim_db for Python>`, :ref:`here for C++ <sim_db for C++>` and :ref:`here for C<sim_db for C>`.

That is the brief overview. Reading the examples below and the links above will fill in the details. 

Minimal Example using Python
============================
A parameter file called `params_mininal_python_example.txt` is located in the *sim_db/examples/* directory in the `source code <https://github.com/task123/sim_db/tree/master/examples>`_. The file contains the following:

.. literalinclude:: ../../examples/params_minimal_python_example.txt
   :language: none

A python script called `minimal_example.py` and is found in the same directory:

.. literalinclude:: ../../examples/minimal_example.py
   :language: python
   :lines: 15-28

Add the those simulations parameters to the **sim_db** database and run the simulation with:

.. code-block:: console

    $ sim_db add_and_run --filename sim_db/examples/params_minimal_python_example.txt

Which can also be done from within the *sim_db/examples/* directory with:

.. code-block:: console

    $ sdb add_and_run -f params_minimal_python_example.txt

where ``sdb`` is just a shorter name for ``sim_db`` and ``-f`` a shorter version of the ``--filename`` flag.

Minimal examples for C++ and C can also be found in the same directory.

Extensive Example using C++
==============================
This example is as the name suggerst much more extensive. It is not as straightforward as the minimal example, but it will demostrate a lot more and will also include explainations of more details.

A parameter file called params_extensive_cpp_example.txt is found in the *sim_db/examples/* directory in the `source code <https://github.com/task123/sim_db/tree/master/examples>`_. This parameter file contains all the possible types available in addition to some comments:

.. literalinclude:: ../../examples/params_extensive_cpp_example.txt
   :language: none

Notice that the parameters names are different from the :ref:`minimal example<Minimal example using Python>`. This is because `param1` and `param2` are differnt types in this example and the type of a parameter can not change in the database. (In practice this is a very good thing. However, if one add the wrong type to the database the first time, the ``delete_sim`` and ``delete_empty_columns`` commands must be used before making a new column with correct type.)

The line in the parameter file starting with *include_parameter_file:* will be substituted with the contain of the specified *extra_params_example.txt* file, found in the same directory:

.. literalinclude:: ../../examples/extra_params_example.txt
   :language: none

This syntax for can be used to simplify the parameter files for projects with many parameters. One can for instance have different parameter files for different kindes of parameters, such as printing parameters. The same parameter name, with the same type, can be added to multiple lines in the parameter files, but all the previous parameter values will be overwritting by the last one. This way one can have a default paramter file, include that in any other parameter file and just change the necesarry parameters. Consider including the other parameter file before the parameters to the sure that they are not modified in the other parameter files, and be careful with the order of included parameter files.

`extensive_example.cpp` is also found in the same directory:

.. literalinclude:: ../../examples/extensive_example.cpp
   :language: c++
   :lines: 16-75

Adding the simulation parameters to the **sim_db** database and running the simulation can be just as in the minimal example:

.. code-block:: console

    $ sim_db add_and_run -f sim_db/examples/params_extensive_cpp_example.txt

If the filename passed to either the ``add_sim`` or ``add_and_run`` commands starts with  *root/* that part will be substituted with the full path to the projects root directory (where *.sim_db/* is located). This way the same path to a parameter file can be passed from anywhere within the project.

It is, as the name suggest, the *run_command* parameter that is used to run the simulation. And it need to included in the parameter file for the ``run_sim``, ``add_and_run`` and ``submit_sim`` commands to work. (The *name* parameter is needed for the *make_unique_subdir* function to work, but is always recommended to included reguardless of whether that function is used or not.)

Notice that when it is run, it first call ``make`` to compile the code if needed. What ``make`` does is equvalient to the following command called from *sim_db/examples/* (given that the static C++ library are compiled):

.. code-block:: console

    $ c++ -o extensive_cpp_example extensive_example.cpp -lsimdbcpp -I../include -L../lib -std=c++11 -lm -lpthread -ldl

If the :code:`add_and_run` command is run without any flags, it will look for any files in the current directory matching the ones `Parameter filenames` in *.sim_db/settings.txt* and add and run the first match. The command is often divided into adding the simulations parameters to the database with:

.. code-block:: console

    $ sdb add

and running the simulation:

.. code-block:: console

    $ sdb run

When passed without any flags ``run`` will run the last simulation added, that have not yet been started. To run a spesific simulation different from the last one, add the ``--id`` flag: 

.. code-block:: console

    $ sdb run --id 'ID'

where '`ID`' is the a unique number given to each set of simulation parameters added to the database. The '`ID`' is printed when using ``add``, but to check the '`ID`' of the last couple of siulations added one can run:

.. code-block:: console

    $ sdb print -n 2 -c id name

`print` have lots of flags to control and limit what is printed. The ``-n 2`` flag prints the last two entries. ``-c id name`` limit the output to just the column named `id` and `name`. ``-v -i 'ID'`` are two other useful flags that prints the columns in the database as rows for the set of parameters that have id 'ID'. To avoid typing out lots of flags and column names/parameter names for each time one would like to print something, one can set `Personlized print configurations` in `settings.txt`. `Personlized print configurations` are a set of print_sim flags that are given a name and can be set as default or called as:

.. code-block:: console

    $ sdb print -p 'name_of_personalized_config' 

When running ``$ sdb run --id 'ID'``, the flags ``--id 'ID' --path_proj_root 'PATH_TO_PROJECT_ROOT_DIR`` is added to the `run_command` before it is run, so that the program know where the database is and which 'ID' to read from. So, the executable prodused by ``make`` or the compile command stated above can be run in the *sim_db/examples/* directoy as:

.. code-block:: console

    $ ./extensive_cpp_example --id 'ID' --path_proj_root ".."

The *sim_db/* directory is there the project root directory, and where *.sim_db/* is located.

The example stored some results in a unique subdirectory, which is the recommended way to store large results. To change the directory to that subdirectory, so one can check out the results, just run:

.. code-block:: console

    $ sdb cd_results --id 'ID' 

To run this example or any other simulation on a cluster or a super computer with a job scheduler, just fill out the `Settings for job scheduler` in `settings.txt` and run:

.. code-block:: console

    $ sdb submit --id 'ID' --max_walltime 00:00:10 --n_tasks 1 

The command will create a job script and submit it to the job scheduler. **sim_db** supports job scheduler SLURM and PBS, but it should be quite easy to add more. `n_tasks` is here the number of logical CPUs you want to run on, and can together with `max_walltime` also be set in the parameter file.

It does not make any sense to run such a small single threaded example on a super computer. If one uses a super computer, one are much more likely to want to run a large simulation on two entire nodes:

.. code-block:: console

    $ sdb submit --id 'ID' --max_walltime 10:30:00 --n_nodes 2

If a number of simulations are added all including the parameters `max_walltime` and `n_tasks`, one can simply run:

.. code-block:: console

    $ sdb submit

, which will run all simulations that have not been run yet after a confimation question.

Extensive examples for Python and C can also be found in the same directory, *sim_db/examples/*, on `github <https://github.com/task123/sim_db/tree/master/example>`.

.. _dependencies:

Multithreading
==============
**sim_db** is thread safe with the notable exception of the ``make_unique_subdir`` functions that should only be called from a single thread.

Dependencies
============
The dependencies for **sim_db** is tried to keep at a minimum and it is overwhelming likely that everything is available if on a Linux machine or a Mac. The reason for the minimal dependencies and the detailed list of actual dependencies, is that the it is expected to use in project using clusers and super computers. On these clusters and super computers one typically don't have root access and only limited ability to install the dependencies.

* **SQLite** - Uses a SQLite database, so it need to be installed on the system. Almost all the flavours of Linux OS are being shipped with SQLite and MacOS comes pre-installed with SQLite. The SQLite Amalgamation (source code of SQLite in C) is even included to provide a painfree compilation of the C and C++ libraries.

* **Python 2.6 or greater** - A Python interpreter of version 2.6 or greater (that means that is also does work with Python 3) is needed as all the commands are written in Python. Pre-installed on almost all Linux distros and on MacOS.

* **C and C++ compiler** - C99 and C++98 compilers are need for using **sim_db** with C or C++ code, but in that case these compilers are of couse needed anyways. Only the examples need a C++11 compiler.

Recommended:

* **Git** - Your project must use Git to get the full range of metadata. If Git is not used, metadata from Git (and the executable's SHA1 hash) is not collected. (So, nothing dramatic. It might, however, be useful.)

* **Make** - Makes the build process much easier.

* **pytest** - `Python framework <https://docs.pytest.org/en/latest/index.html>`_ used to run the tests and nothing else. Installed with :code:`$ pip install -U pytest`.

Windows:
++++++++
* **Cygwin/MinGW** - The commands relie on Unix (POSIX) style paths, which Cygwin/MinGW/powershell mimicks.

(Not tested on windows yet.)

License
=======
The project is licensed under the MIT license. A copy of the license is provided `here <https://github.com/task123/sim_db/blob/master/LICENSE>`_.
