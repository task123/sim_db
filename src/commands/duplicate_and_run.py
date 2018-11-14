# -*- coding: utf-8 -*-
""" Duplicate a set of parameters from database and run simulation with it.

If the 'ID' of a set of simulation parameters is passed to 
'duplicate_and_run.py', a new set of almost identically simulation parameters 
will be created. The only parameters that are NOT identical is the 'id', which 
will be unique, and 'status', which will be set to 'new'.

The new set of parameters will then be used to run a simulation.

Usage: 'python duplicate_and_run.py --id ID'
"""
# Copyright (C) 2018 Håkon Austlid Taskén <hakon.tasken@gmail.com>
# Licenced under the MIT License.

if __name__ == '__main__':
    import add_root_dir_to_path

import src.commands.duplicate_sim as duplicate_sim
import src.commands.run_sim as run_sim
import argparse


def command_line_arguments_parser():
    # yapf: disable
    parser = argparse.ArgumentParser(description="Duplicate simulation in database and run it. All parameters (including possible results) of specified simulation is duplicated with the exception of 'id' and 'status', which is kept unique and set to 'new' respectfully.")
    parser.add_argument('--id', '-i', type=int, required=True, help="<Required> 'ID' of the simulation parameters in the 'sim.db' database that should be duplicated.")
    parser.add_argument('-n', type=int, default=None, help="Number of threads/core to run the simulation on.")
    # yapf: enable

    return parser


def duplicate_and_run(argv=None):
    args = command_line_arguments_parser().parse_args(argv)

    new_id = duplicate_sim.duplicate_sim(['--id', str(args.id)])

    if args.n == None:
        run_sim.run_sim(['--id', str(new_id)])
    else:
        run_sim.run_sim(['--id', str(new_id), '-n', str(args.n)])

    return new_id


if __name__ == '__main__':
    duplicate_and_run()
