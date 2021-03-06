==============
sim_db for C++
==============

.. toctree::
   :maxdepth: 1
   :caption: sim_db for C++

Minimal Example using C++
=========================
A parameter file called `params_mininal_cpp_example.txt` is located in the *sim_db/examples/* directory in the `source code <https://github.com/task123/sim_db/tree/master/examples>`_. The file contains the following:

.. literalinclude:: ../../examples/params_minimal_cpp_example.txt
   :language: none

A C++ file called `minimal_example.cpp` and is found in the same directory:

.. literalinclude:: ../../examples/minimal_example.cpp
   :language: C++
   :lines: 15-27

Add the those simulations parameters to the **sim_db** database and run the simulation from within the `sim_db/examples` directory with:

.. code-block:: console

    $ sim_db add_and_run -f params_minimal_cpp_example.txt

Notice that when it is run, it first call two ``cmake`` commands to compile the code if needed. What ``cmake`` does is equvalient to the following command called from *sim_db/examples/* (given that the static C library are compiled and located in *sim_db/build*):

.. code-block:: console

    $ c++ -o build/minimal_cpp_example minimal_example.cpp -I../include -L../build -lsimdbcpp -lpthread -ldl -m

The example is not really a minimal one. If you already have compiled your program into a executable called ``program`` located in the current directory, the lines starting with ``{...} (alias):`` can be removed and the ``run_command`` can be replaced with simpy ``run_command (string): ./program``.

Extensive Example using C++
===========================
A parameter file called params_extensive_cpp_example.txt is found in the *sim_db/examples/* directory in the `source code <https://github.com/task123/sim_db/tree/master/examples>`_. This parameter file contains all the possible types available in addition to some comments:

.. literalinclude:: ../../examples/params_extensive_cpp_example.txt
   :language: none

The line in the parameter file starting with *include_parameter_file:* will be substituted with the contain of the specified *extra_params_example.txt* file, found in the same directory:

.. literalinclude:: ../../examples/extra_params_example.txt
   :language: none

`extensive_example.py` is also found in the same directory:

.. literalinclude:: ../../examples/extensive_example.cpp
   :language: C++
   :lines: 16-76

Add the those simulations parameters to the **sim_db** database and run the simulation from within the `sim_db/examples` directory with:

.. code-block:: console

    $ sdb add_and_run -f params_extensive_cpp_example.txt

Notice that when it is run, it first call ``cmake`` to compile the code if needed. What ``cmake`` does is equvalient to the following command called from *sim_db/examples/* (given that the static C library are compiled and located in *sim_db/build/*):

.. code-block:: console

    $ cc -o build/extensive_cpp_example extensive_example.cpp -I../include -L../build -lsimdbcpp -lpthread -ldl -m

C++ API Referance
====================

.. doxygenclass:: sim_db::Connection
   :project: sim_db

.. doxygenfunction:: sim_db::Connection::Connection(int, char**, bool)
.. doxygenfunction:: sim_db::Connection::Connection(std::string, int, bool)
.. doxygenfunction:: sim_db::Connection::read
.. doxygenfunction:: sim_db::Connection::write
.. doxygenfunction:: sim_db::Connection::unique_results_dir
.. doxygenfunction:: sim_db::Connection::column_exists
.. doxygenfunction:: sim_db::Connection::get_id
.. doxygenfunction:: sim_db::Connection::get_path_proj_root
.. doxygenfunction:: sim_db::Connection::update_sha1_executables
.. doxygenfunction:: sim_db::Connection::delete_from_database
.. doxygenfunction:: sim_db::add_empty_sim(bool)
.. doxygenfunction:: sim_db::add_empty_sim(std::string, bool)
