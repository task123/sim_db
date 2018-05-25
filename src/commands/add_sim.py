# -*- coding: utf-8 -*-
""" Add simulation parameters to a sqlite3 database from a text file.

Name of the parameter file can be passed to the program, otherwise first match
with parameter file from 'settings.txt' is used.

The format of the parameter file is for each parameter as following:
parameter_name (type): parameter_value
'type' can be int, float, string, bool or int/float/string/bool array.
Lines without any colon is ignored.

The database used is the one which path given in 'settings.txt', closest 
matches the currect directory.

Usage: 'python add_sim.py' or 'python add_sim.py -filename name_param_file.txt'
"""
# Copyright (C) 2017, 2018 Håkon Austlid Taskén <hakon.tasken@gmail.com>
# Licenced under the MIT License.

import helpers
import sqlite3
import argparse
import sys
import os
import subprocess


def command_line_arguments_parser():
    # yapf: disable
    parser = argparse.ArgumentParser(description='Add simulation to database.')
    parser.add_argument('--filename', '-f', type=str, default=None, help="Name of parameter file added and submitted.")
    # yapf: enable

    return parser


def split_parameter_line(line, i):
    line_split = line.split(':', 1)
    try:
        value = line_split[1].strip()
        param_name, param_type = line_split[0].split('(')
        param_name = param_name.strip()
        param_type = param_type.split(')')[0].strip()
    except ValueError:
        raise ValueError("Parameter on line no. {0} in the parameter ".format(i) \
                       + "file has INCORRECT format of type and parentheses.")
    return param_name, param_type, value


def add_new_column(db_cursor, i, param_type, param_name, value):
    if param_type == 'int':
        db_cursor.execute("ALTER TABLE runs ADD COLUMN \
                          {0} INTEGER"                                                                                                                  .format(param_name))
    elif param_type == 'float':
        db_cursor.execute("ALTER TABLE runs ADD COLUMN \
                           {0} REAL"                                                                                                            .format(param_name))
    elif param_type == 'string':
        db_cursor.execute("ALTER TABLE runs ADD COLUMN \
                           {0} TEXT"                                                                                                            .format(param_name))
    elif param_type == 'bool':
        db_cursor.execute("ALTER TABLE runs ADD COLUMN \
                           {0} TEXT"                                                                                                            .format(param_name))
    elif len(param_type) > 5 and param_type[-5:] == 'array':
        db_cursor.execute("ALTER TABLE runs ADD COLUMN \
                           {0} TEXT"                                                                                                            .format(param_name))
        array_type = param_type[:-5].strip()
        if array_type != 'int' and array_type != 'float' \
                and array_type != 'string' and array_type != 'bool':
            raise ValueError("Parameter on line no. {0} in ".format(i) \
                           + "parameter file has INVALID type of array.")
        if len(value) > 0 and (value[0] != '[' or value[-1] != ']'):
            raise ValueError("Parameter on line no. {0} in the ".format(i) \
                           + "parameter file has INCORRECT format for " \
                           + "arrays. Square bracets missing.")
    else:
        raise ValueError("Parameter on line no. {0} in the parameter".format(i) \
                       + "file has an INVALID type.")


def check_type_matches(param_type, column_type, value, i):
    correct_type = False
    if column_type == 'INTEGER' and (param_type == 'int'
                                     or param_type == 'bool'):
        correct_type = True
    elif column_type == 'REAL' and param_type == 'float':
        correct_type = True
    elif column_type == 'TEXT':
        if param_type == 'string':
            correct_type = True
        elif param_type == 'bool':
            correct_type = True
        elif len(param_type) > 5 and param_type[-5:] == 'array':
            array_type = param_type[:-5].strip()
            if array_type == 'int' or array_type == 'float' \
                    or array_type == 'string' or array_type == 'bool':
                correct_type = True
            if len(value) > 0 and (value[0] != '[' or value[-1] != ']'):
                raise ValueError("Parameter on line no. {0} in the ".format(i) \
                               + "parameter file has INCORRECT format for " \
                               + "arrays. Square bracets missing.")
    if not correct_type:
        raise ValueError("Parameter on line no. {0} in the parameter".format(i) \
                       + "file has an INVALID type.")


def standardize_value(value, param_type):
    if param_type == 'bool':
        if value == "False" or value == "false" or value == "FALSE" or value == 0:
            value = "False"
        else:
            value = "True"
    type_split = param_type.split()
    if len(type_split
           ) > 1 and type_split[0] == 'bool' and type_split[1] == 'array':
        array = value[1:-1].split(',')
        new_array = "["
        for i in array:
            i = i.strip()
            if i == "False" or i == "false" or i == "FALSE" or i == "0":
                new_array += "False, "
            else:
                new_array += "True, "
        new_array = new_array[:-2]
        new_array += ']'
        value = new_array
    if (param_type == 'string array'):
        strings = value[1:-1].split(',')
        value = "["
        for i in range(len(strings)):
            string = strings[i]
            while (string.strip()[0] == '"' and string.strip()[-1] != '"'):
                i += 1
                string += string[i]
            while (string.strip()[0] == "'" and string.strip()[-1] != "'"):
                i += 1
                string += string[i]
            string = string.strip()
            if ((string[0] == '"' and string[-1] == '"') \
                or (string[0] == "'" and string[-1] == "'")):
                string = string[1:-1]
            value += string + ', '
        if len(strings) > 0:
            value = value[:-2] + ']'
    if len(type_split) > 1 and type_split[1] == 'array' and len(value) > 0:
        value = type_split[0] + value
    if (param_type == 'string' or param_type == 'bool' \
            or (len(param_type) > 5 and param_type[-5:] == 'array')):
        if len(value) > 0:
            if not ((value[0] == "'" and value[-1] == "'") or
                    (value[0] == '"' and value[-1] == '"')):
                value = "'" + value + "'"

    return value


def insert_value(db_cursor, param_name, last_row_id, value):
    if last_row_id:
        db_cursor.execute("UPDATE runs SET {0} = {1} WHERE id = {2};" \
                          .format(param_name, value, last_row_id))
    else:
        db_cursor.execute("INSERT INTO runs (status, {0}) VALUES ('new', {1});" \
                          .format(param_name, value))
        last_row_id = db_cursor.lastrowid
    return last_row_id


def make_path_relative_to_sim_db(run_command, sim_params_filename):
    """Make all paths starting with './' relative to 'sim_db'."""
    sim_params_filename = os.getcwd() + '/' + sim_params_filename
    sim_params_dir = sim_params_filename.split('/')[:-1]
    sim_db_dir = helpers.get_closest_sim_db_dir_path().split('/')
    i = 0
    while (i < len(sim_params_dir) and i < len(sim_db_dir)
           and sim_params_dir[i] == sim_db_dir[i]):
        i += 1
    rel_path = ""
    for j in range(len(sim_db_dir) - i - 1):
        rel_path += "../"
    for dir_name in sim_params_dir[i:]:
        rel_path += dir_name + "/"

    run_command = run_command.replace(' ./', ' sim_db/' + rel_path)
    return run_command


def add_sim(argv=None):
    db = helpers.connect_sim_db()

    args = command_line_arguments_parser().parse_args(argv)
    sim_params_filename = args.filename
    if (sim_params_filename != None and len(sim_params_filename.split('/')) > 1
                and sim_params_filename.split('/')[0] == 'sim_db'):
        sim_params_filename = ( helpers.get_closest_sim_db_dir_path() + '/' +
                               sim_params_filename.split('/', 1)[1])
    if sim_params_filename == None:
        sim_params_filename = (
                helpers.search_for_parameter_file_matching_settings())

    try:
        sim_params_file = open(sim_params_filename, 'r')
    except:
        print("Could NOT open {0}.".format(sim_params_filename))
        exit(1)

    db_cursor = db.cursor()
    default_db_columns = ""
    for key in helpers.default_db_columns:
        default_db_columns += key + " " + str(
                helpers.default_db_columns[key]) + ", "
    default_db_columns = default_db_columns[:-2]
    db_cursor.execute("CREATE TABLE IF NOT EXISTS runs ({0});".format(
            default_db_columns))

    column_names, column_types = helpers.get_db_column_names_and_types(
            db_cursor)

    last_row_id = None
    for i, line in enumerate(sim_params_file.readlines()):
        if len(line.split(':')) > 1:
            param_name, param_type, value = split_parameter_line(line, i)

            if param_name == 'run_command':
                value = make_path_relative_to_sim_db(value,
                                                     sim_params_filename)

            try:
                row_index = column_names.index(param_name)
            except ValueError:
                row_index = None

            if row_index is None:
                add_new_column(db_cursor, i, param_type, param_name, value)
            else:
                check_type_matches(param_type, column_types[row_index], value,
                                   i)

            value = standardize_value(value, param_type)
            if len(value) > 0:
                last_row_id = insert_value(db_cursor, param_name, last_row_id,
                                           value)

    db.commit()
    db_cursor.close()
    db.close()

    return last_row_id


if __name__ == '__main__':
    last_id = add_sim()
    print("ID of last added: {0}".format(last_id))
