==================
sim_db for Fortran
==================

.. toctree::
   :maxdepth: 1
   :caption: sim_db for Fortran

Minimal Example using Fortran
=============================
A parameter file called `params_mininal_fortran_example.txt` is located in the *sim_db/examples/* directory in the `source code <https://github.com/task123/sim_db/tree/master/examples>`_. The file contains the following:

.. literalinclude:: ../../examples/params_minimal_fortran_example.txt
   :language: none

A Fortran file called `minimal_example.f90` and is found in the same directory:

.. literalinclude:: ../../examples/minimal_example.f90
   :language: Fortran
   :lines: 11-31

Add the those simulations parameters to the **sim_db** database and run the simulation from within the `sim_db/examples` directory with:

.. code-block:: console

    $ sim_db add_and_run -f params_minimal_cpp_example.txt

Notice that when it is run, it first call two ``cmake`` commands to compile the code if needed. What ``cmake`` does is equvalient to the following command called from *sim_db/examples/* (given that the static Fortran library are compiled and located in *sim_db/build*):

.. code-block:: console

    $ gfortran -o build/minimal_fortran_example minimal_example.f90 -I../build -L../build -lsimdbf -lpthread -ldl -m

The example is not really a minimal one. If you already have compiled your program into a executable called ``program`` located in the current directory, the lines starting with ``{...} (alias):`` can be removed and the ``run_command`` can be replaced with simpy ``run_command (string): ./program``.

Extensive Example using Fortran
===============================
A parameter file called params_extensive_cpp_example.txt is found in the *sim_db/examples/* directory in the `source code <https://github.com/task123/sim_db/tree/master/examples>`_. This parameter file contains all the possible types available in addition to some comments:

.. literalinclude:: ../../examples/params_extensive_fortran_example.txt
   :language: none

The line in the parameter file starting with *include_parameter_file:* will be substituted with the contain of the specified *extra_params_example.txt* file, found in the same directory:

.. literalinclude:: ../../examples/extra_params_example.txt
   :language: none

`extensive_example.py` is also found in the same directory:

.. literalinclude:: ../../examples/extensive_example.f90
   :language: Fortran
   :lines: 11-93

Add the those simulations parameters to the **sim_db** database and run the simulation from within the `sim_db/examples` directory with:

.. code-block:: console

    $ sdb add_and_run -f params_extensive_fortran_example.txt

Notice that when it is run, it first call ``cmake`` to compile the code if needed. What ``cmake`` does is equvalient to the following command called from *sim_db/examples/* (given that the static Fortran library are compiled and located in *sim_db/build/*):

.. code-block:: console

    $ gfortran -o build/extensive_fortran_example extensive_example.f90 -I../build -L../build -lsimdbf -lpthread -ldl -m

Fortran API Referance
=====================

Doxygen and Breathe that is used to generate the documentation for C, C++ and Fortran, does not work as well for Fortran as it does for C and C++. The Fortran documentation is therefor less than ideal, but hopefully still somewhat useful, espesially in combination with the examples. The parameter types are written in bold at the start of the parameter description.

.. doxygeninterface:: sim_db_mod::sim_db
.. doxygenfunction:: sim_db_mod::sim_db_ctor
.. doxygenfunction:: sim_db_mod::sim_db_ctor_with_id
.. doxygenfunction:: sim_db_mod::sim_db_ctor_without_search

.. doxygenfunction:: sim_db_mod::sim_db::read
.. doxygenfunction:: sim_db_mod::read_int
.. doxygenfunction:: sim_db_mod::read_real_sp
.. doxygenfunction:: sim_db_mod::read_real_dp
.. doxygenfunction:: sim_db_mod::read_string
.. doxygenfunction:: sim_db_mod::read_logical
.. doxygenfunction:: sim_db_mod::read_int_array
.. doxygenfunction:: sim_db_mod::read_real_sp_array
.. doxygenfunction:: sim_db_mod::read_real_dp_array
.. doxygenfunction:: sim_db_mod::read_string_array
.. doxygenfunction:: sim_db_mod::read_logical_array

.. doxygenfunction:: sim_db_mod::sim_db::write
.. doxygenfunction:: sim_db_mod::write_int
.. doxygenfunction:: sim_db_mod::write_int_false
.. doxygenfunction:: sim_db_mod::write_real_sp
.. doxygenfunction:: sim_db_mod::write_real_sp_false
.. doxygenfunction:: sim_db_mod::write_real_dp
.. doxygenfunction:: sim_db_mod::write_real_dp_false
.. doxygenfunction:: sim_db_mod::write_string
.. doxygenfunction:: sim_db_mod::write_string_false
.. doxygenfunction:: sim_db_mod::write_logical
.. doxygenfunction:: sim_db_mod::write_logical_false
.. doxygenfunction:: sim_db_mod::write_int_array
.. doxygenfunction:: sim_db_mod::write_int_array_false
.. doxygenfunction:: sim_db_mod::write_real_sp_array
.. doxygenfunction:: sim_db_mod::write_real_sp_array_false
.. doxygenfunction:: sim_db_mod::write_real_dp_array
.. doxygenfunction:: sim_db_mod::write_real_dp_array_false
.. doxygenfunction:: sim_db_mod::write_string_array
.. doxygenfunction:: sim_db_mod::write_string_array_false
.. doxygenfunction:: sim_db_mod::write_logical_array
.. doxygenfunction:: sim_db_mod::write_logical_array_false

.. doxygenfunction:: sim_db_mod::unique_results_dir
.. doxygenfunction:: sim_db_mod::unique_results_dir
.. doxygenfunction:: sim_db_mod::unique_results_dir_abs_path
.. doxygenfunction:: sim_db_mod::column_exists
.. doxygenfunction:: sim_db_mod::is_empty
.. doxygenfunction:: sim_db_mod::set_empty
.. doxygenfunction:: sim_db_mod::get_id
.. doxygenfunction:: sim_db_mod::get_path_proj_root

.. doxygenfunction:: sim_db_mod::sim_db::update_sha1_executables 
.. doxygenfunction:: sim_db_mod::update_sha1_executables_conditionally
.. doxygenfunction:: sim_db_mod::update_sha1_executables_unconditionally

.. doxygenfunction:: sim_db_mod::allow_timeouts
.. doxygenfunction:: sim_db_mod::have_timed_out
.. doxygenfunction:: sim_db_mod::delete_from_database
.. doxygenfunction:: sim_db_mod::close
