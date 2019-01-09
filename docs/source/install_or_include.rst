.. _install_or_include:

==================
Install or Include
==================

Install
=======

(If you wish to include **sim_db** instead of installing it, jump to the next subsection.)

Command line tool and python package
------------------------------------

**sim_db** can be can most easily be installed with ``pip``:

.. code-block:: console

    $ pip install sim_db

The command line tool and the python package should now be available. If one are only going to use the python version of **sim_db**, it should now be ready for use. For listing all the available command of the command line tool run:

.. code-block:: console

    $ sim_db list_commands

(This should also work on Windows as long as your Python directory and its *Scripts/* subdirectory is added to the *%PATH%*.)

How to use any of them can be found either by running the with the ``--help`` or ``-h`` flag or reading the documentation of the :ref:`commands <Commands>`. Most of the commands need to have some sets of simulation parameters added to the database to work, so read the examples below to see how to do that. (The command line tool can also be invoked by running ``$ python -m sim_db``.)

Testing the import of the python package can be done with:

.. code-block:: console

    $ python -c "import sim_db"

And should just return without producing any errors.

Change directory to your projects root directory and initiate **sim_db** with the command:

.. code-block:: console

    $ sim_db init

The command will add a *.sim_db/* directory.

C and C++ versions
------------------

If one are going to use in the C or C++ version of **sim_db**, one also have to download the source code from `github <https://github.com/task123/sim_db>`_. It is recommended to add **sim_db** as a git submodule of your project by (inside your project) running:

.. code-block:: console

    $ git submodule add https://github.com/task123/sim_db

The C and C++ libraries now needs to by complied and this can be done either with CMake or just with Make. To compile and install the libraries with CMake run these commands:

.. code-block:: console

    $ cd sim_db
    $ mkdir build
    $ cd build
    $ cmake ..
    $ cmake --build . --target install

To compile the libraries using just Make run these commands:

.. code-block:: console

    $ cd sim_db
    $ make

(If **sim_db** haven't already been install with ``pip`` and you are running just make, it will be installed now.) 

The libraries should now be available in *sim_db/build/* as *libsimdb.a* and *libsimdbcpp.a* with headers *sim_db/include/sim_db.h* and *sim_db/include/sim_db.hpp* respectfully.

Include in Your Project
=======================
(Skip to this section of one have choosen to install **sim_db**.)

**sim_db** is designed to not add any additional dependencies for your project, except a absolute minimum. It therefore does not itself **need** to be installed, just included. (The command_line_tool is just python scripts (except the ``cd_results`` command), so it can be called with :code:`$ python path_to_sim_db_dir/sim_db/__main__.py`. It is however much more convenient to just add the command line tool to your *PATH*.)

It is recommended to add **sim_db** as a git submodule in your project by (inside your project) running:

.. code-block:: console

    $ git submodule add https://github.com/task123/sim_db

(Otherwise it can taken from `github <https://github.com/task123/sim_db>`_ and just copied into your project in a directory called '`sim_db`'.)

If Make is available run the following commands:

.. code-block:: console

    $ cd sim_db
    $ make include

Answer yes when asked to add *sim_db/sim_db* to your *PATH* in *~/.bashrc* or *~/.bash_profile* and remember to source it.

If Make is not available, include *sim_db/sim_db* to your *PATH* and if the C and C++ libraries are needed compile them with CMake by running these commands:

.. code-block:: console

    $ cd sim_db
    $ mkdir build
    $ cd build
    $ cmake ..
    $ cmake --build .

All **sim_db** commands should now be available and the C and C++ libraries should be compiled and found in the *build/* directory with the headers in *include/*. Test the following command:

.. code-block:: console

    $ sim_db list_commands

It should list all the **sim_db** commands. How to use any of them can be found either by running the with the ``--help`` or ``-h`` flag or reading the documentation of the :ref:`commands <Commands>`. Most of the commands need to have some sets of simulation parameters added to the database to work, so read the examples below to see how to do that.

(The full set of tests can be run with ``$ pytest`` or ``$ python -m pytest`` provided `pytest` is installed.)

Change directory to your projects root directory and initiate **sim_db** with the command:

.. code-block:: console

    $ sim_db init

The command will add a *.sim_db/* directory.

Since **sim_db** is just included, it will manually need to be added to the *PYTHONPATH* before using the python package. This can be done in your *~/.bashrc* or *~/.bash_profile*, but it can also be done from within your python code. For a python script in the same directory as *sim_db/* it can be done like this:

.. code-block:: python

    import sys, os.path
    sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "sim_db"))
    import sim_db

The python package should now behave as if it was installed. For files in subdirectories, just add more ``os.path.dirname`` calls round the path.

Dependencies
============
The dependencies for **sim_db** is tried to keep at a minimum and it is overwhelming likely that everything is available if on a Linux machine or a Mac. The reason for the minimal dependencies and the detailed list of actual dependencies, is that the it is expected to use in project using clusers and super computers. On these clusters and super computers one typically don't have root access and only limited ability to install the dependencies.

* **SQLite** - **sim_db** uses a SQLite database, so it need to be installed on the system. Almost all the flavours of Linux OS are being shipped with SQLite and MacOS comes pre-installed with SQLite. The SQLite Amalgamation (source code of SQLite in C) is even included to provide a painfree compilation of the C and C++ libraries.

* **Python 2.6 or greater** - A Python interpreter of version 2.6 or greater (that means that is also does work with Python 3) is needed as all the commands are written in Python. Pre-installed on almost all Linux distros and on MacOS.

* **C and C++ compiler** - C99 and C++98 compilers are need for using **sim_db** with C or C++ code, but in that case these compilers are of couse needed anyways. Only the examples need a C++11 compiler.

Recommended:

* **Git** - Your project must use Git to get the full range of metadata. If Git is not used, metadata from Git (and the executable's SHA1 hash) is not collected. (So, there is no dramatic difference if it not used. It might, however, be useful.)

* **CMake** or just **Make** - Makes the build process much easier.

* **pytest** - `Python framework <https://docs.pytest.org/en/latest/index.html>`_ used to run the tests and nothing else. Installed with :code:`$ pip install -U pytest`.

For Windows:

* **Cygwin/MinGW** - The the C and C++ libraries relie on Unix (POSIX) style paths, which Cygwin/MinGW/powershell mimicks.

(Not propery tested on windows yet.)

License
=======
The project is licensed under the MIT license. A copy of the license is provided `here <https://github.com/task123/sim_db/blob/master/LICENSE>`_.
