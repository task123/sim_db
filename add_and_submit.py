# -*- coding: utf-8 -*-
""" Add simulation parameters to the database and submit simulation.

Name of the parameter file can be passed to the program, otherwise first match
with parameter file from 'settings.txt' is used.

The format of the parameter file is for each parameter as following:
parameter_name (type): parameter_value
'type' can be int, float, string, bool or int/float/string/bool array.
Lines without any semicolon is ignored.

The database used is the one which path given in 'settings.txt', closest 
matches the currect directory.

The submit program used to submit is taken from default submit program in 
'settings.txt' if no other program is specified.

Usage: 'python add_and_submit.py' 
    or 'python add_and_submit.py -filename name_param_file.txt
                                 -submit_program submit_vilje.py"
"""
# Copyright (C) 2017 Håkon Austlid Taskén <hakon.tasken@gmail.com>
# Licenced under the MIT License.

import add_sim
import sqlite3
import argparse
import sys
import os

def get_arguments(argv):
    parser = argparse.ArgumentParser(description='Add simulation and submit it.')
    parser.add_argument('-filename', '-f', type=str, default=None, help="Name of parameter file added and submitted.")
    parser.add_argument('-submit_program', type=str, default=None, help="Program called to submit the simulation. (Called with arguments '-id ID'.)")
    return parser.parse_args(argv)

def get_submit_program_from_settings():
    sim_db_dir = os.path.dirname(os.path.abspath(__file__))
    settings_file = open(sim_db_dir + '/settings.txt', 'r')
    next_is_submit_program = False
    for line in settings_file:
        if next_is_submit_program and len(line.strip()) > 0:
            settings_file.close()
            return line.strip()
        if len(line) > 23 and line[:24] == "# Default submit program":
            next_is_submit_program = True
    settings_file.close()
    return None

def main(argv=None):
    args = get_arguments(argv)
    
    if args.filename == None:
        added_id = add_sim.main()
    else:
        added_id = add_sim.main("-filename {}".format(args.filename).split())

    submit_program = args.submit_program
    if submit_program == None:
        submit_program = get_submit_program_from_settings()
        if submit_program == None:
            raise ValueError("No default submit program is found in " \
                           + "'settings.txt'.") 

    os.system("python {0} -id {1}".format(submit_program, added_id)) 

if __name__ == '__main__':
    main()
