# -*- coding: utf-8 -*-
""" Used by a bash function to change directory to the 'result_dir' of a simulation."""

# Copyright (C) 2018 Håkon Austlid Taskén <hakon.tasken@gmail.com>
# Licenced under the MIT License.

import helpers
import sim_db
import argparse
import os

def get_arguments(argv):
    parser = argparse.ArgumentParser(description="Return full path to 'result_dir' of simulation with provided id, '-i ID'. Used by a bash function, 'cd_results', to change directory to this 'result_dir'.")
    parser.add_argument('--id', '-i', type=int, required=True, help="<Required> 'ID' of the 'result_dir' in the 'sim.db' database.")
    return parser.parse_args(argv)

def cd_results(argv=None):
    args = get_arguments(argv)
    
    simdb = sim_db.SimDB(db_id=args.id)
    return simdb.read('result_dir')

if __name__ == '__main__':
    print(cd_results())
    

