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
# Copyright (C) 2017, 2018 Håkon Austlid Taskén <hakon.tasken@gmail.com>
# Licenced under the MIT License.

if __name__ == '__main__':
    import add_root_dir_to_path

import src.commands.add_sim as add_sim
import src.commands.run_sim as run_sim
import argparse


def command_line_arguments_parser():
    # yapf: disable
    parser = argparse.ArgumentParser(description='Add simulation and submit it.')
    parser.add_argument('--filename', '-f', type=str, default=None, help="Name of parameter file added and submitted.")
    parser.add_argument('-n', type=int, default=None, help="Number of threads/core to run the simulation on.")
    # yapf: enable

    return parser


def add_and_run(argv=None):
    args = command_line_arguments_parser().parse_args(argv)

    if args.filename == None:
        added_id = add_sim.add_sim()
    else:
        added_id = add_sim.add_sim(['--filename', args.filename])

    if args.n == None:
        run_sim.run_sim(['--id', str(added_id)])
    else:
        run_sim.run_sim(['--id', str(added_id), '-n', str(args.n)])

    return added_id


if __name__ == '__main__':
    add_and_run()
