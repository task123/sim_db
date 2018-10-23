==============
sim_db for C++
==============

.. toctree::
   :maxdepth: 1
   :caption: sim_db for C++

Minimal example using C++
=========================
A parameter file called `params_mininal_cpp_example.txt` is located in the *sim_db/example/* directory in the `source code<https://github.com/task123/sim_db/tree/master/example>`. The file contains the following:

.. literalinclude:: ../../example/params_minimal_cpp_example.txt
   :language: none

A C++ file called `minimal_example.cpp` and is found in the same directory:

.. literalinclude:: ../../example/minimal_example.cpp
   :language: C++
   :lines: 13-27

Add the those simulations parameters to the **sim_db** database and run the simulation from within the `sim_db/example` directory with:

.. code-block:: console

    $ add_and_run -f params_minimal_cpp_example.txt

Notice that when it is run, it first call `make` to compile the code if needed. What `make` does is equvalient to the following command called from *sim_db/example/* (given that the static C library are compiled):

.. code-block:: console

    $ c++ -o minimal_cpp_example minimal_example.cpp -lsimdbcpp -I../include -L../lib -lm -lpthread -ldl

Extensive example using C++
===========================
A parameter file called params_extensive_cpp_example.txt is found in the *sim_db/example/* directory in the `source code<https://github.com/task123/sim_db/tree/master/example>`. This parameter file contains all the possible types available in addition to some comments:

.. literalinclude:: ../../example/params_extensive_cpp_example.txt
   :language: none

The line in the parameter file starting with *include_parameter_file:* will be substituted with the contain of the specified *extra_params_example.txt* file, found in the same directory:

.. literalinclude:: ../../example/extra_params_example.txt
   :language: none

`extensive_example.py` is also found in the same directory:

.. literalinclude:: ../../example/extensive_example.cpp
   :language: C++
   :lines: 16-56

Add the those simulations parameters to the **sim_db** database and run the simulation from within the `sim_db/example` directory with:

.. code-block:: console

    $ add_and_run -f params_extensive_cpp_example.txt

Notice that when it is run, it first call `make` to compile the code if needed. What `make` does is equvalient to the following command called from *sim_db/example/* (given that the static C library are compiled):

.. code-block:: console

    $ cc -o extensive_cpp_example extensive_example.cpp -lsimdbcpp -I../include -L../lib -lm -lpthread -ldl

C++ API referance
====================

.. doxygenclass:: sim_db::Connection
   :project: sim_db

.. doxygenfunction:: sim_db::Connection::Connection(int, char **, bool)
.. doxygenfunction:: sim_db::Connection::Connection(std::string, int, bool)
.. doxygenfunction:: sim_db::Connection::read
.. doxygenfunction:: sim_db::Connection::write
.. doxygenfunction:: sim_db::Connection::make_unique_subdir
.. doxygenfunction:: sim_db::Connection::update_sha1_executables

