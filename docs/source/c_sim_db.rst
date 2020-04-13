============
sim_db for C
============

.. toctree::
   :maxdepth: 1
   :caption: sim_db for C

Minimal Example using C
=======================
A parameter file called `params_mininal_c_example.txt` is located in the *sim_db/examples/* directory in the `source code <https://github.com/task123/sim_db/tree/master/examples>`_. The file contains the following:

.. literalinclude:: ../../examples/params_minimal_c_example.txt
   :language: none

A C file called `minimal_example.c` and is found in the same directory:

.. literalinclude:: ../../examples/minimal_example.c
   :language: C
   :lines: 14-29

Add the those simulations parameters to the **sim_db** database and run the simulation from within the `sim_db/examples` directory with:

.. code-block:: console

    $ sim_db add_and_run -f params_minimal_c_example.txt

Notice that when it is run, it first call two ``cmake`` commands to compile the code if needed. What ``cmake`` does is equvalient to the following command called from *sim_db/examples/* (given that the static C library are compiled and located in *sim_db/build/*):

.. code-block:: console

    $ cc -o build/minimal_c_example minimal_example.c -I../include -L../build -lsimdbc -lpthread -ldl -m

The example is not really a minimal one. If you already have compiled your program into a executable called ``program`` located in the current directory, the lines starting with ``{...} (alias):`` can be removed and the ``run_command`` can be replaced with simpy ``run_command (string): ./program``.

Extensive Example using C
=========================
A parameter file called params_extensive_c_example.txt is found in the *sim_db/examples/* directory in the `source code <https://github.com/task123/sim_db/tree/master/examples>`_. This parameter file contains all the possible types available in addition to some comments:

.. literalinclude:: ../../examples/params_extensive_c_example.txt
   :language: none

The line in the parameter file starting with *include_parameter_file:* will be substituted with the contain of the specified *extra_params_example.txt* file, found in the same directory:

.. literalinclude:: ../../examples/extra_params_example.txt
   :language: none

`extensive_example.py` is also found in the same directory:

.. literalinclude:: ../../examples/extensive_example.c
   :language: C
   :lines: 20-98

Add the those simulations parameters to the **sim_db** database and run the simulation from within the `sim_db/examples` directory with:

.. code-block:: console

    $ sdb add_and_run -f params_extensive_c_example.txt

Notice that when it is run, it first call ``cmake`` to compile the code if needed. What ``cmake`` does is equvalient to the following command called from *sim_db/examples/* (given that the static C library are compiled and located in *sim_db/build/*):

.. code-block:: console

    $ cc -o build/extensive_c_example extensive_example.c -I../include -L../build -lsimdbc -lpthread -ldl -m

C API Referance
====================

.. doxygenfunction:: sim_db_ctor(int, char **)
.. doxygenfunction:: sim_db_ctor_no_metadata
.. doxygenfunction:: sim_db_ctor_with_id(int, bool)
.. doxygenfunction:: sim_db_ctor_without_search(const char *, int, bool)
.. doxygenfunction:: sim_db_read_int
.. doxygenfunction:: sim_db_read_double
.. doxygenfunction:: sim_db_read_string
.. doxygenfunction:: sim_db_read_bool
.. doxygenstruct:: SimDBIntVec
   :members:
.. doxygenfunction:: sim_db_read_int_vec
.. doxygenstruct:: SimDBDoubleVec
   :members:
.. doxygenfunction:: sim_db_read_double_vec
.. doxygenstruct:: SimDBStringVec
   :members:
.. doxygenfunction:: sim_db_read_string_vec
.. doxygenstruct:: SimDBBoolVec
   :members:
.. doxygenfunction:: sim_db_read_bool_vec
.. doxygenfunction:: sim_db_write_int
.. doxygenfunction:: sim_db_write_double
.. doxygenfunction:: sim_db_write_string
.. doxygenfunction:: sim_db_write_bool
.. doxygenfunction:: sim_db_write_int_array
.. doxygenfunction:: sim_db_write_double_array
.. doxygenfunction:: sim_db_write_string_array
.. doxygenfunction:: sim_db_write_bool_array
.. doxygenfunction:: sim_db_unique_results_dir
.. doxygenfunction:: sim_db_unique_results_dir_abs_path
.. doxygenfunction:: sim_db_column_exists
.. doxygenfunction:: sim_db_get_id
.. doxygenfunction:: sim_db_get_path_proj_root
.. doxygenfunction:: sim_db_update_sha1_executables
.. doxygenfunction:: sim_db_allow_timeouts
.. doxygenfunction:: sim_db_have_timed_out
.. doxygenfunction:: sim_db_delete_from_database
.. doxygenfunction:: sim_db_dtor
.. doxygenfunction:: sim_db_add_empty_sim
.. doxygenfunction:: sim_db_add_empty_sim_without_search(const char *, bool)
