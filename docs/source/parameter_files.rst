===============
Parameter Files
===============

A text file with a particular format is used to pass parameters to the simulations. The parameters are easily edited in the text files, and added to the database and used to run the simulation with the command:

.. code-block:: console

    $ sim_db add_and_run -f sim_param_file.txt

The Format
==========

The format of the parameter file is for each parameter as following:

*parameter_name* (*type*): *parameter_value*

*type* can be *int*, *float*, *string*, *bool* or *int*/*float*/*string*/*bool array*. Lines without any colon is ignored. This means that the parameter name, type, colon and value MUST all be on the same line and colons can ONLY be used on lines with parameters (except when including other parameter files).

The '*run_command* (*string*): *command*' parameter need to be one of the parameters in the parameter file for the ``run_sim``, ``add_and_run`` and ``submit_sim`` commands to work. The '*name* (*string*): *name_of_simulation*' stricly only needed if the *unique_results_dir* function is used, but it is always recommeneded to include.

The parameters from other parameter files can be included with a line like this:

include_parameter_file: *name_parameter_file*

The line is simply substituted with the contain of the file, and the included files are also allowed to include other parameter files. (Including any files in which the file is itself included, will cause an infinite loop). ``include parameter file:`` can also be used instead of ``include parameter file:``.

It is perfectly fine to have the same parameter name, with the same type, in multiple plasses in the parameter file. The previous parameter values will just be overwritten by the last one.

It is also possible create an alias taking the follow format:

*{string_to_replace}* (alias): *replacement_string*

Any occurrence of *{string_to_replace}* on any line after a colon and below this alias definition, will be replaced by *replacement_string*. This also includes any parameter files included after the alias. It is required that the alias name starts and ends with curly brackets as in the above example. Aliases is powerful and can be very useful if a parameter or part of a parameter appear in multiple parameters. It also allows for a layer of abstraction. But be careful as this can cause unintended replacements and can easily make the parameter file harder to read. Avoid excessive use and use unique alias names.

The format is very flexible, as the parameters can be in any order and lines without colons can be used freely to comment, describe and organise (with blank lines and indents) the parameters. This makes it easy to make the parameters of the simulation well understood. It is also very fast to change any number of parameters as it is only a text file that need to be edited. The parameters can also be organised in different files using ``include_parameter_file:``. 

run_command
===========
A couple words about how the 'run_command' is treated by **sim_db** can be helpful. The ``run_sim``, ``add_and_run`` and ``submit_sim`` commands uses the 'run_command' parameter (given as ``run_command (string): command``) to run the simultion. Before the 'run_command' is run a couple things are done to it. It is split at all semicolons into multiple commands, all occurrences of 'root/' will be replaced with the path to the root directory of the project and ' # ' will be replaced with the ' *n_tasks* ', where *n_tasks* is a parameter passed to one of the commands that uses the run_command. As an example let's say a project with root directory, ``/path/root/dir``, have a run_command defined as: 

``run_command (string): make -C root/example; mpirun # root/example/program``

in ``sim_params.txt``. Running ``$ sim_db add_and_run -f sim_params.txt -n 4`` will then in turn run the commands:

.. code-block:: console

    $ make -C /path/root/dir/example
    $ mpirun 4 /path/root/dir/example/program

(If your run_command contain a 'root/' that your don't want to be replaced, you should substitute it with an alias.) 


Example
=======

Example of a parameter file that uses all the different parameter types:

.. literalinclude:: ../../examples/params_extensive_c_example.txt
   :language: none

The line in the parameter file starting with *include_parameter_file:* will be substituted with the contain of the specified *extra_params_example.txt* file:

.. literalinclude:: ../../examples/extra_params_example.txt
   :language: none

Filename
========

The filename of the text file with the parameters can be anything (to describe what simulation it is used for) and just passed to the ``add_sim`` and ``add_and_run`` commands with the ``--filename`` or ``-f`` option. That option can however be omitted be naming the parameter file *sim_params.txt* or any other name added under the *Parameter filenames* header in the *settings.txt* file in the *.sim_db/* directory.

Commands Realated to Parameters
===============================

The parameters in a parameter file can be added to the database with the ``add`` command or added and run with ``add_and_run``. The file can then be edited to add new simulations, but a parameter can also be edited or added to an already added simulation with the ``update`` command. One can also generate a new parameter file from a simulation in the database with the ``extract_params`` commands, which can be a quick way of running simulations similar to that one. Finally it is very useful to get familiar with the ``print`` command to print the parameters and other things from simulations in the database.
