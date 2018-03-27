# -*- coding: utf-8 -*-
""" Extract the parameters from the database to a parameter file.

The parameter file can be used to add a new equal simulation, but more usefully
modified to run a slightly different simulation.
"""
# Copyright (C) 2017 Håkon Austlid Taskén <hakon.tasken@gmail.com>
# Licenced under the MIT License.

import helpers
import sqlite3
import argparse
import os.path

def get_arguments(argv):
    parser = argparse.ArgumentParser(description='Extract parameter file from sim_runs.db.')
    parser.add_argument('-id', type=int, required=True, help="<Required> ID of the simulation which parameter one wish to extract.")
    parser.add_argument('-filename', '-f', type=str, default=None, help="Name of paramter file generated.")
    parser.add_argument('--all', action='store_true', help="Extract all parameters. Default if to only extract non empty parameters to parameter file.")
    return parser.parse_args(argv)

def get_param_type_as_string(col_type, value):
    if col_type == 'INTEGER':
        return 'int'
    elif col_type == 'REAL':
        return 'float'
    elif col_type == 'TEXT':
        if value == 'True' or value == 'False':
            return 'bool' 
        value_split = value.split('[')
        if len(value_split) > 1:
            return value_split[0] + ' array'
        else:
            return 'string'
    else:
        raise ValueError()        

def extract_params(argv=None):
    args = get_arguments(argv)

    if args.filename == None:
        filename = 'sim_params.txt'
    else:
        filename = args.filename
    params_file = open(filename, 'w')

    sim_db_dir = helpers.get_closest_sim_db_path()
    db = sqlite3.connect(sim_db_dir + 'sim.db')
    db_cursor = db.cursor()

    db_cursor.execute("SELECT * FROM runs WHERE id={}".format(args.id))
    extracted_row = db_cursor.fetchall()
    
    column_names, column_types = helpers.get_db_column_names_and_types(db_cursor)

    for col_name, col_type, value in zip(column_names, column_types, 
                                         extracted_row[0]):
        if col_name != 'id' and col_name != 'status' \
                and col_name != 'used_walltime' and col_name != 'job_id':
            skip = True
        else:
            skip = False

        if (args.all or value != None) and skip:
            line = col_name
            param_type = get_param_type_as_string(col_type, value)
            line += " ({}): ".format(param_type)
            if param_type[-3:] == 'ray':
                value = '[' + value.split('[')[1]
            line += str(value) + '\n'
            params_file.write(line)
    
    params_file.close()        

    db.commit()
    db_cursor.close()
    db.close()

if __name__ == '__main__':
    extract_params()
