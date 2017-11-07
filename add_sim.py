# -*- coding: utf-8 -*-
""" Add simulation parameters to a sqlite3 database from a text file.

Name of the parameter file can be passed to the program, otherwise first match
with parameter file from 'settings.txt' is used.

The format of the parameter file is for each parameter as following:
parameter_name (type): parameter_value
'type' can be int, float, string, bool or int/float/string/bool array.
Lines without any semicolon is ignored.

The database used is the one which path given in 'settings.txt', closest 
matches the currect directory.

Usage: 'python add_sim.py' or 'python add_sim.py name_param_file.txt'
"""
# Copyright (C) 2017 Håkon Austlid Taskén <hakon.tasken@gmail.com>
# Licenced under the MIT License.

import sqlite3
import sys
import os

def search_for_parameter_file_from_settings():
    sim_db_dir = os.path.dirname(os.path.abspath(__file__))
    settings_file = open(sim_db_dir + '/settings.txt', 'r')
    line = ""
    while len(line) < 11 or line[:11] != "# Databases":
        line = settings_file.readline()
        for file_in_current_dir in os.listdir('.'):
            if file_in_current_dir == line.strip():
                return file_in_current_dir
    return None

def get_database_name_from_settings():
    currect_dir = os.getcwd()
    sim_db_dir = os.path.dirname(os.path.abspath(__file__))
    settings_file = open(sim_db_dir + '/settings.txt', 'r')
    longest_match_length = 1
    database_name = None
    for line in settings_file:
        line = line.strip()
        match_length = 0
        for i in range(min(len(line), len(currect_dir))):
            if line[i] == currect_dir[i]:
                match_length += 1
        if match_length > longest_match_length:
            longest_match_length = match_length
            database_name = line
    settings_file.close()
    return database_name

def get_column_names_and_types(db_cursor):
    table_info = db_cursor.execute("PRAGMA table_info('runs')")
    column_names = []
    column_types = []
    for row in table_info:
        column_names.append(row[1])
        column_types.append(row[2])
    return column_names, column_types

def split_parameter_line(line, i):
    line_split = line.split(':', 1)
    try:
        value = line_split[1].strip()
        param_name, param_type = line_split[0].split('(')
        param_name = param_name.strip()
        param_type = param_type.split(')')[0].strip()
    except ValueError:
        raise ValueError("Parameter no. {} in the parameter file ".format(i) \
                       + "has INCORRECT format of type and parentheses.")
    return param_name, param_type, value

def add_new_column(db_cursor, i, param_type, param_name, value):
    print param_type
    if param_type == 'int':
        print 'int'
        db_cursor.execute("ALTER TABLE runs ADD COLUMN \
                          {} INTEGER".format(param_name))
    elif param_type == 'float':
        print 'real'
        db_cursor.execute("ALTER TABLE runs ADD COLUMN \
                           {} REAL".format(param_name))
    elif param_type == 'string':
        db_cursor.execute("ALTER TABLE runs ADD COLUMN \
                           {} TEXT".format(param_name))
    elif param_type == 'bool':
        db_cursor.execute("ALTER TABLE runs ADD COLUMN \
                           {} TEXT".format(param_name))
    elif len(param_type) > 5 and param_type[-5:] == 'array':
        db_cursor.execute("ALTER TABLE runs ADD COLUMN \
                           {} TEXT".format(param_name))
        array_type = param_type[:-5].strip()
        if array_type != 'int' and array_type != 'float' \
                and array_type != 'string' and array_type != 'bool':
            raise ValueError("Parameter no. {} in parameter file ".format(i) \
                           + "has INVALID type of array.")
        if len(value) > 0 and (value[0] != '[' or value[-1] !=']'):
            raise ValueError("Parameter no. {} in the ".format(i) \
                           + "parameter file has INCORRECT format for " \
                           + "arrays. Square bracets missing.")
    else:
        raise ValueError("Parameter no. {} in the parameter".format(i) \
                       + "file has an INVALID type.")
    print get_column_names_and_types(db_cursor)
            
def check_type_matches(param_type, column_type, value, i):
    correct_type = False
    if column_type == 'INTEGER' and (param_type == 'int' or param_type == 'bool'):
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
            if len(value) > 0 and (value[0] != '[' or value[-1] !=']'):
                raise ValueError("Parameter no. {} in the ".format(i) \
                               + "parameter file has INCORRECT format for " \
                               + "arrays. Square bracets missing.")
    if not correct_type:
        raise ValueError("Parameter no. {} in the parameter".format(i) \
                       + "file has an INVALID type.")

def normalize_value(value, param_type):
    if param_type == 'bool':
        if value == "False" or value == "false" or value == "FALSE" or value == 0:
            value = "False"
        else:
            value = "True"
    type_split = param_type.split()
    if len(type_split) > 1 and type_split[0] == 'bool' and type_split[1] == 'array':
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
    if len(type_split) > 1 and type_split[1] == 'array':
        value = type_split[0] + value     
    if (param_type == 'string' or param_type == 'bool' \
            or (len(param_type) > 5 and param_type[-5:] == 'array')):
        if len(value) > 0:
            if not ((value[0] == "'" and value[-1] == "'") 
                    or (value[0] == '"' and value[-1] == '"')):
                value = "'" + value + "'"
    return value

def insert_value(db_cursor, param_name, last_row_id, value):
    if last_row_id:
        db_cursor.execute("UPDATE runs SET {0} = {1} WHERE id = {2}" \
                          .format(param_name, value, last_row_id))
    else:
        db_cursor.execute("INSERT INTO runs (status, {0}) VALUES ('new', {1});" \
                          .format(param_name, value))
        last_row_id = db_cursor.lastrowid
    return last_row_id

def main(argv):
    database_name = get_database_name_from_settings()
    if database_name == None:
        database_name = "sim.db"
    db = sqlite3.connect(database_name)

    if len(argv) > 1:
        sim_params_filename = str(argv[1])
    else:
        sim_params_filename = search_for_parameter_file_from_settings()

    try:
        sim_params_file = open(sim_params_filename, 'r')
    except:
        print "Could NOT open {}.".format(sim_params_filename)
        exit(1)

    db_cursor = db.cursor()
    db_cursor.execute("CREATE TABLE IF NOT EXISTS runs (id INTEGER PRIMARY KEY, "
                                                     + "status TEXT, "
                                                     + "name TEXT, "
                                                     + "description TEXT, "
                                                     + "used_walltime REAL, "
                                                     + "job_id INTEGER);")

    column_names, column_types = get_column_names_and_types(db_cursor)

    last_row_id = None
    for i, line in enumerate(sim_params_file.readlines()):
        if len(line.split(':')) > 1:
            param_name, param_type, value = split_parameter_line(line, i)

            try:
                row_index = column_names.index(param_name)
            except ValueError:
                row_index = None

            if row_index is None:
                add_new_column(db_cursor, i, param_type, param_name, value)
            else:
                check_type_matches(param_type, column_types[row_index], value, i)

            value = normalize_value(value, param_type)
            
            last_row_id = insert_value(db_cursor, param_name, last_row_id, value)

    db.commit()
    db_cursor.close()
    db.close()

    return last_row_id

if __name__ == '__main__':
    main(sys.argv)
