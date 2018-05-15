# -*- coding: utf-8 -*-
""" Add simulation parameters to the database and submit it to job scheduler.

Name of the parameter file can be passed to the program, otherwise first match
with parameter file from 'settings.txt' is used.

The format of the parameter file is for each parameter as following:
parameter_name (type): parameter_value
'type' can be int, float, string, bool or int/float/string/bool array.
Lines without any colon is ignored.

The database used is the one which path given in 'settings.txt', closest 
matches the currect directory.

Usage: 'python add_and_submit.py' 
    or 'python add_and_submit.py -filename name_param_file.txt
"""
# Copyright (C) 2017, 2018 Håkon Austlid Taskén <hakon.tasken@gmail.com>
# Licenced under the MIT License.

import add_sim
import run_sim
import submit_sim
import argparse

def get_arguments(argv):
    parser = argparse.ArgumentParser(description='Add simulation and submit it.')
    parser.add_argument('--filename', '-f', type=str, default=None, help="Name of parameter file added and submitted.")
    parser.add_argument('-n', type=int, default=None, help="Number of threads/core to run the simulation on.")
    return parser.parse_args(argv)

def add_and_submit(argv=None):
    args = get_arguments(argv)
    
    if args.filename == None:
        added_id = add_sim.add_sim()
    else:
        added_id = add_sim.add_sim(['--filename', args.filename])
    
    if args.n == None:
        submit_sim.submit_sim(['--id', str(added_id)])
    else:
        submit_sim.submit_sim(['--id', str(added_id), '-n', str(args.n)])

if __name__ == '__main__':
    add_and_submit()