#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Add simulation parameters to the database and run the simulation.

Name of the parameter file can be passed to the program, otherwise first match
with parameter file from 'settings.txt' is used.

The format of the parameter file is for each parameter as following:
parameter_name (type): parameter_value
'type' can be int, float, string, bool or int/float/string/bool array.
Lines without any colon is ignored.

The database used is the one which path given in 'settings.txt', closest 
matches the currect directory.

Usage: 'python add_and_run.py' 
    or 'python add_and_run.py -filename name_param_file.txt
"""
# Copyright (C) 2017-2019 Håkon Austlid Taskén <hakon.tasken@gmail.com>
# Licenced under the MIT License.

if __name__ == '__main__':
    import add_package_root_to_path

import sim_db.src_command_line_tool.commands.add_sim as add_sim
import sim_db.src_command_line_tool.commands.run_sim as run_sim
import argparse
import sys


def command_line_arguments_parser(name_command_line_tool="sim_db",
                                  name_command="add_and_run"):
    parser = argparse.ArgumentParser(
            description='Add simulation and submit it.',
            prog="{0} {1}".format(name_command_line_tool, name_command))
    parser.add_argument(
            '--filename',
            '-f',
            type=str,
            default=None,
            help="Name of parameter file to add and run.")
    parser.add_argument(
            '-n',
            type=int,
            default=None,
            help="Number of threads/core to run the simulation on.")
    parser.add_argument(
            '--add_unique_results_dir',
            '-u',
            action="store_true",
            help="Add a unique subdirectory for the simulation in the "
                 "'superdir_for_results' directory in the settings and write " 
                 "it to 'results_dir' in the database.")

    return parser


def add_and_run(name_command_line_tool="sim_db",
                name_command="add_and_run",
                argv=None):
    args = command_line_arguments_parser(name_command_line_tool,
                                         name_command).parse_args(argv)

    if args.filename == None:
        added_id = add_sim.add_sim()
    else:
        added_id = add_sim.add_sim(argv=['--filename', args.filename])

    run_parameters = ['--id', str(added_id)]
    if args.n != None:
        run_parameters += ['-n', str(args.n)]
    if args.add_unique_results_dir:
        run_parameters += ['--add_unique_results_dir']
    run_sim.run_sim(argv=run_parameters)

    return added_id


if __name__ == '__main__':
    add_and_run("", sys.argv[0], sys.argv[1:])
