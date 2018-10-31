============
sim_db for C
============

.. toctree::
   :maxdepth: 1
   :caption: sim_db for C

Minimal example using C
=======================
A parameter file called `params_mininal_c_example.txt` is located in the *sim_db/example/* directory in the `source code<https://github.com/task123/sim_db/tree/master/example>`. The file contains the following:

.. literalinclude:: ../../example/params_minimal_c_example.txt
   :language: none

A C file called `minimal_example.c` and is found in the same directory:

.. literalinclude:: ../../example/minimal_example.c
   :language: C
   :lines: 13-29

Add the those simulations parameters to the **sim_db** database and run the simulation from within the `sim_db/example` directory with:

.. code-block:: console

    $ add_and_run -f params_minimal_c_example.txt

Notice that when it is run, it first call `make` to compile the code if needed. What `make` does is equvalient to the following command called from *sim_db/example/* (given that the static C library are compiled):

.. code-block:: console

    $ cc -o minimal_c_example minimal_example.c -lsimdbc -I../include -L../lib -lm -lpthread -ldl

Extensive example using C
=========================
A parameter file called params_extensive_c_example.txt is found in the *sim_db/example/* directory in the `source code<https://github.com/task123/sim_db/tree/master/example>`. This parameter file contains all the possible types available in addition to some comments:

.. literalinclude:: ../../example/params_extensive_c_example.txt
   :language: none

The line in the parameter file starting with *include_parameter_file:* will be substituted with the contain of the specified *extra_params_example.txt* file, found in the same directory:

.. literalinclude:: ../../example/extra_params_example.txt
   :language: none

`extensive_example.py` is also found in the same directory:

.. literalinclude:: ../../example/extensive_example.c
   :language: C
   :lines: 14-82

Add the those simulations parameters to the **sim_db** database and run the simulation from within the `sim_db/example` directory with:

.. code-block:: console

    $ add_and_run -f params_extensive_c_example.txt

Notice that when it is run, it first call `make` to compile the code if needed. What `make` does is equvalient to the following command called from *sim_db/example/* (given that the static C library are compiled):

.. code-block:: console

    $ cc -o extensive_c_example extensive_example.c -lsimdbc -I../include -L../lib -lm -lpthread -ldl

C API referance
====================

.. doxygenfunction:: sim_db_ctor
.. doxygenfunction:: sim_db_ctor_no_metadata
.. doxygenfunction:: sim_db_ctor_with_id
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
.. doxygenfunction:: sim_db_make_unique_subdir_rel_path
.. doxygenfunction:: sim_db_make_unique_subdir_abs_path
.. doxygenfunction:: sim_db_update_sha1_executables
.. doxygenfunction:: sim_db_get_id
.. doxygenfunction:: sim_db_get_path
.. doxygenfunction:: sim_db_dtor
.. doxygenfunction:: add_empty_sim(const char *)
.. doxygenfunction:: delete_sim(const char *, int)
