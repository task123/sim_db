===============
Parameter Files
===============

A text file with a particular format is used to pass parameters to the simulations. The parameters are easily edited in the text files, and added to the database and used to run the simulation with the command:

.. code-block:: console

    $ add_and_run -f sim_param_file.txt

The format
==========

The format of the parameter file is for each parameter as following:

parameter_name (type): parameter_value

*type* can be *int*, *float*, *string*, *bool* or *int*/*float*/*string*/*bool array*. Lines without any colon is ignored. This means that the parameter name, type, colon and value MUST all be on the same line and colons can ONLY be used on lines with parameters.

The format is very flexible, as the parameters can be in any order and lines without colons can be used freely to comment, describe and organise (with blank lines and indents) the parameters. This makes it easy to make the parameters of the simulation well understood. It is also very fast to change any number of parameters as it is only a text file that need to be edited. 

Example
=======

Example of a parameter file with all the different types used to that uses all the different types:

.. literalinclude:: ../../example/params_extensive_c_example.txt
   :language: none

Filename
========

The filename of the parameter file can be any name (to describe what simulation it is used for) and just passed to the ```add_sim``` and ```add_and_run``` commands with the ```--filename``` or ```-f``` option. That option can however be omitted be nameing the parameter file *sim_params.txt* or any other name added under the *Parameter filenames* header in the *settings.txt* file in the *sim_db/* directory.

Commands realated to parameters
===============================

The parameters in a parameter file can be added to the database with the ```add_sim``` command or added and run with ```add_and_run```. The file can then be edited to add new simulations, but a parameter can also be edited or added to an already added simulation with the ```update_sim``` command. One can also generate a new parameter file from a simulation in the database with the ```extract_params``` commands, which can be a quick way of running simulations similar to that one. Finally it is very useful to get familiar with the ```print_sim``` command to print the parameters and other things from simulations in the database.
