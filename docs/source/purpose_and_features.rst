====================
Purpose and Features
====================

If you have already decided to use **sim_db**, then skip right ahead to :ref:`install_or_include`.

Purpose
=======
Simulations are usually run with a large number of different sets of parameters. It may not happen at once, it may not even be the intent, but over time it probably will accumulate anyway. It is hard to keep track of all of these simulations including their parameters, without deleting any that one might want to checkout later. Especially, weeks, months or even years after the simulations were run.

When doing simulations, one will usually run a great number of simulations with different parameters. After a while it will often become a difficult to keep track of all the simulations; the parameters used to run them, the results and metadate such at the time used to perform the simulation. sim_db aim towards providing a flexible and convenient way of keeping track of all the simulation and does this by storing the parameters in a SQLite3 database.

**sim_db** aims to fix this problem. It will conveniently let you run a large number of simulations with different parameter values, while keep track of these all simulation parameters and results along with metadata in a database for you. 

Features
========

Easy to Use
+++++++++++
Have a look at a :ref:`minimal example <Minimal example using Python>` and decide for yourself.

Well Documented
+++++++++++++++
Important for use of any code and software and believed to be a modest claim in this case. However, you are currently reading the site documenting **sim_db**, so you can again just decide for yourself.

Keep Track of Your Results
++++++++++++++++++++++++++
It obviously stores all the parameters used to run the simulation, but it also provides two mechanicams to organise your results as well. Results can can easily be written to the database, but for large results and for files that are read by other software for visualization or postprocessing it should be written to file. **sim_db** will create a unique subdirectory for you to store your results in, keep track of this subdirectory and easily jump into it.

Stores a lot of Metadata Automatically
++++++++++++++++++++++++++++++++++++++
**sim_db** stores a lot of metadata that might be useful down the line or even right away. A full list of what is stored is given in the list explaining the :ref:`default columns <Default columns - metadata stored>` in the database. In total what parameters was used, what was the result / where was it stored, what code was used to produce the result (for git projects) including what binary (was it compiled with this code), why this simulation was run, how long did it take to run on how many logical cpus on which hardware should be stored to the database — all while being less work to use that too not use **sim_db** (that is at least the idea).

Few Dependencies
++++++++++++++++
Few dependencies make your project easier to install and to get running, and **sim_db** keeps it to :ref:`a minimum <dependencies>` requiring essentially only a Python interpreter.

Python, C, C++ and Fortran
++++++++++++++++++++++++++
**sim_db** exists for both Python, C, C++ and Fortran, and wrappers for languages that can call C functions are quite easy to add. It is also very useful that multiple programs of different languages can read the same parameters from the database. This does for example allows the plotting, visualization and after work can be seperated in a in a python program and the actual computational intensive simulation in a C++ program.

Thread Safe
+++++++++++
**sim_db** is thread safe and intended to be used in programs running on hundreds of CPUs. Read more about use in multithreading and multiprocessing applications :ref:`here. <Multithreading and Multiprocessing>`

Built to Run on both Local Machine and Super Computers/Clusters
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Can easily both run your simulations on your local machine and on a super computer/cluster with a job scheduler, where it will generate the job script and submit it for you. 

Many Print Options
++++++++++++++++++
With many parameters and lots of simulations it becomes important to be able to view only the simulations and parameters you want to see. **sim_db** has lots of print options to do that. 


Default Columns - Metadata Stored
---------------------------------
The default columns in the database contain the metadata of the simulations run and are the columns not containing the parameters to the simulations or results saved from the simulations. The purpose of each one is explained below and is essentially a full list of the metadata stored.

* ``id`` - To uniquely refer to a set of simulation parameters.

* ``status`` - Status of simulation: 'submitted', 'running' or 'finished'.

* ``name`` - To easily distinguage the different simulations.

* ``describtion`` - To further explain the intent of the simulation.

* ``run_command`` - Command to run the simulation.

* ``comment`` - Comment about the simulation and how it ran. Standard error may be included.

* ``add_to_job_script`` - Additional flags, import or load statement added to the job script for the job scheduler.

* ``result_dir`` - The path to where the results are stored. 

* ``time_submitted`` - To tell how long a submition have been in queque.

* ``time_started`` - To tell how long a simulation used in queque and how long it have been running. 

* ``used_walltime`` - To tell the total run time of the simulation.

* ``max_walltime`` - Useful if the simulation is stopped for exceeding this limit. (Also in the context of understanding the time between ``time_submitted`` and ``time_started``.)

* ``job_id`` - To check the simulation when submitted to a job scheduler.

* ``n_tasks`` - Number of threads/cores. Needed to understand 'used_walltime'.

* ``cpu_info`` - Needed to compare ``used_walltime`` across different machines.

* ``git_hash`` - To be sure of which commit the simulation is run from.

* ``commit_message`` - A easier way to distinguage the commits than the hash. 

* ``git_diff_stat`` - Show summary of difference between the working directory and the current commit (HEAD) at the time the simulation is run.

* ``git_diff`` - Show the explicit difference between the working directory and the current commit at the time when the simulation is run.

* ``sha1_executables`` - To tell exacetly which executable that was used to run the simulation. Useful to check that it have been compiled after any changes. Is the sha1 of any files in the ``run_command``.

* ``initial_parameters`` - To distinguage between parameters used to run the simulation and results produced by the simulation.







