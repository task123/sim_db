===
Use
===

Include in your project
=======================
It is recommended to add **sim_db** as a git submodule in your project by running::

    $ git submodule add https://github.com/klasdj

(Otherwise it can just be copied into your project in a directory called '`sim_db`'.)

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
The parameter file is called `params_mininal_python_example.txt` and is located in the `sim_db/test/` directory. The file contains the following:

.. literalinclude:: ../../example/params_minimal_python_example.txt

The python script is called `minimal_example.py` and is found in the same directory:

.. literalinclude:: ../../example/minimal_example.py
   :language: python
   :lines: 15-25

Add the those simulations parameters to the **sim_db** database and run the simulation with::

    $ add_and_run --filename sim_db/test/params_minimal_python_example.py

Which can also be done from within the `test/` directory with::

    $ add_and_run -f params_minimal_python_example.py

Extensive example using C++
==============================

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
