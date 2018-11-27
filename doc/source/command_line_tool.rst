=================
Command Line Tool
=================

The command line tool is called ``sim_db``, but can also be called with ``sdb``. It has a syntax simular to ``git``, where commands are passed to ``sim_db`` followed by the arguments to the command: ``$ sim_db <command> [<args>]``. 

All the available commands can be listed with the ``list_commands`` (run as ``$ sim_db list_commands``), and what they do and which arguments they take is found by passing the ``--help`` or ``-h`` option to any of the commands. The same information is found below. 

Commands ending in *_sim* can also be used without this ending, so ``add`` is the same commend as ``add_sim``.

All the commands can be called from anywhere is your project after the ``init`` command is called in your projects root directory. The only exception is inside the ``sim_db/`` directory if that is included.

sim_db
======

.. argparse::
   :ref: src.command_line_tool.command_line_tool.command_line_arguments_parser

Commands
========

add_and_run
-----------
.. argparse::
   :ref: add_and_run.command_line_arguments_parser

add_and_submit
--------------
.. argparse::
   :ref: add_and_submit.command_line_arguments_parser

add_column
----------
.. argparse::
   :ref: add_column.command_line_arguments_parser

add_comment
-----------
.. argparse::
   :ref: add_comment.command_line_arguments_parser

add_range
---------
.. argparse::
   :ref: add_range_sim.command_line_arguments_parser

add_sim
-------
.. argparse::
   :ref: add_sim.command_line_arguments_parser

cd_results
----------
.. argparse::
   :ref: src.command_line_tool.command_line_tool.cd_results_command_line_arguments_parser

combine_dbs
-----------
.. argparse::
   :ref: combine_dbs.command_line_arguments_parser

delete_empty_columns
--------------------
.. argparse::
   :ref: delete_empty_columns.command_line_arguments_parser

delete_results_dir
------------------
.. argparse::
   :ref: delete_results_dir.command_line_arguments_parser

delete_sim
----------
.. argparse::
   :ref: delete_sim.command_line_arguments_parser

duplicate_and_run
-----------------
.. argparse::
   :ref: duplicate_and_run.command_line_arguments_parser

duplicate_sim
-------------
.. argparse::
   :ref: duplicate_sim.command_line_arguments_parser

extract_params
--------------
.. argparse::
   :ref: extract_params.command_line_arguments_parser

get
---
.. argparse::
   :ref: get.command_line_arguments_parser

init
----
.. argparse::
   :ref: init.command_line_arguments_parser

list_commands
-------------
.. argparse::
   :ref: list_commands.command_line_arguments_parser

list_print_configs
------------------
.. argparse::
   :ref: list_print_configs.command_line_arguments_parser

print_sim
---------
.. argparse::
   :ref: print_sim.command_line_arguments_parser

run_seriel_sims
---------------
.. argparse::
   :ref: run_serial_sims.command_line_arguments_parser

run_sim
-------
.. argparse::
   :ref: run_sim.command_line_arguments_parser

settings
--------
.. argparse::
   :ref: settings.command_line_arguments_parser

submit_sim
----------
.. argparse::
   :ref: submit_sim.command_line_arguments_parser

update_sim
----------
.. argparse::
   :ref: update_sim.command_line_arguments_parser
