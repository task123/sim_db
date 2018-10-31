=================
sim_db for Python
=================

.. toctree::
   :maxdepth: 1
   :caption: sim_db for Python

Minimal example using Python
============================
A parameter file called `params_mininal_python_example.txt` is located in the *sim_db/example/* directory in the `source code<https://github.com/task123/sim_db/tree/master/example>`. The file contains the following:

.. literalinclude:: ../../example/params_minimal_python_example.txt
   :language: none

A python script called `minimal_example.py` and is found in the same directory:

.. literalinclude:: ../../example/minimal_example.py
   :language: python
   :lines: 15-28

Add the those simulations parameters to the **sim_db** database and run the simulation from the *sim_db/example/* directory with:

.. code-block:: console

    $ add_and_run -f params_minimal_python_example.txt

Extensive example using Python
==============================
A parameter file called params_extensive_python_example.txt is found in the *sim_db/example/* directory in the `source code<https://github.com/task123/sim_db/tree/master/example>`. This parameter file contains all the possible types available in addition to some comments:

.. literalinclude:: ../../example/params_extensive_python_example.txt
   :language: none

The line in the parameter file starting with *include_parameter_file:* will be substituted with the contain of the specified *extra_params_example.txt* file, found in the same directory:

.. literalinclude:: ../../example/extra_params_example.txt
   :language: none

`extensive_example.py` is also found in the same directory:

.. literalinclude:: ../../example/extensive_example.py
   :language: python
   :lines: 16-65

Add the those simulations parameters to the **sim_db** database and run the simulation from the *sim_db/example/* directory with:

.. code-block:: console

    $ add_and_run -f params_extensive_python_example.txt

Python API referance
====================
.. automodule:: sim_db
.. autoclass:: SimDB
    :members:
    :special-members: __init__
