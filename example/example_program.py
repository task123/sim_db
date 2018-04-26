# -*- coding: utf-8 -*-
""" Add simulation parameters to a sqlite3 database from a text file.
Usage: 'python example_program --id ID'
"""
# Copyright (C) 2017 Håkon Austlid Taskén <hakon.tasken@gmail.com>
# Licenced under the MIT License.

import __init__
import sim_db
import argparse


parser = argparse.ArgumentParser(description='Example program that prints example parameters from database.')
parser.add_argument('--id', '-i', required=True, type=int, help="<Required> ID of example paramters in sim.db database.")
args = parser.parse_args()

sim_db = sim_db.SimDB()

print("\nSimulation is printing out all input parameters:")
for i in range(1, 9):
    parameter = sim_db.read(column='param{}'.format(i))
    print("param{0}: {1}".format(i, parameter))

sim_db.end()
