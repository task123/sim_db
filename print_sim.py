# -*- coding: utf-8 -*-
""" Print parameters of simulations ran or running, i.e. content of database.

Print the content of database with a number of possible restrictions.
"""
# Copyright (C) 2017 Håkon Austlid Taskén <hakon.tasken@gmail.com>
# Licenced under the MIT License.

from add_sim import get_database_name_from_settings
from add_sim import get_column_names_and_types
import sqlite3
import argparse
import os
import sys
import numpy as np

def get_arguments(argv):
    parser = argparse.ArgumentParser(description='Print content in sim_runs.db.')
    parser.add_argument('-id', type=int, nargs='+', help="List of ID's.")
    parser.add_argument('-id_no_print', type=int, nargs='+', help="List of ID's not to print.")
    parser.add_argument('-n', type=int, help="Number of row printed from the bottom up.")
    parser.add_argument('-columns', type=str, nargs='+', default=None, help="Name of the columns to print. All non empty columns are printed by default.")
    parser.add_argument('-columns_no_print', type=str, nargs='+', default=None, help="Name of the columns not to print.")
    parser.add_argument('-col_by_num', type=int, nargs='+', default=None, help="Number of the columns to print. All non empty columns are printed by default.")
    parser.add_argument('-where', default='id > -1', help="Add constraints to which columns to print. Must be a valid SQL (sqlite3) command when added after WHERE in a SELECT search.")
    parser.add_argument('-sort_by', default='id', help="What to sort the output by. Must be a valid SQL (sqlite3) command when added after ORDER BY in a SELECT search. Defalut is id.")
    parser.add_argument('--column_names', action='store_true', help="Print name and type of all columns.")
    parser.add_argument('--all_columns', action='store_true', help="Print all columns. Otherwise only non empty columns are printed.")
    parser.add_argument('--no_headers', action='store_true', help="Print without any headers.")
    parser.add_argument('-max_width', type=int, default=None, help="Upper limit for the width of each column. Default is no limit.")
    parser.add_argument('-p', type=int, default=None, help="Personal print configuration. Apply the print configuration in 'settings.txt' corresponding to the provided number.")
    return parser.parse_args(argv)

def get_personalized_print_config(number):
    sim_db_dir = os.path.dirname(os.path.abspath(__file__))
    settings_file = open(sim_db_dir + '/settings.txt', 'r')
    for line in settings_file:
        split_line = line.split(':')
        if len(split_line) > 1:
            if number == int(split_line[0]):
                return split_line[1].strip()
    return None

def select_command(db_cursor, args, column_names):
    if args.columns == None and args.col_by_num == None:
        columns = '*'
    else:
        columns = ""
        if args.columns != None:
            for col in args.columns:
                columns += "{}, ".format(col)
            columns = columns[:-2]
        if args.col_by_num != None:
            for i in args.col_by_num:
                columns += "{}, ".format(column_names[i])

    if args.id == None:
        db_cursor.execute("SELECT {0} FROM runs WHERE {1} ORDER BY {2}" \
                          .format(columns, args.where, args.sort_by))
        selected_output = db_cursor.fetchall()
    else:
        selected_output = []
        for i in args.id:
            restrictions = args.where + " AND id = {}".format(i)
            db_cursor.execute("SELECT {0} FROM runs WHERE {1} ORDER BY {2}" \
                              .format(columns, restrictions, args.sort_by))
            selected_output.append(db_cursor.fetchall()[0])

    selected_output = np.array(selected_output)
    if not args.all_columns and args.columns == None:
        selected_output, column_names = remove_empty_columns(selected_output, 
                                                             column_names)
    if args.columns_no_print != None:
        selected_output, column_names = remove_columns_not_to_print(
                selected_output, column_names, args.columns_no_print)
    if args.columns != None:
        column_names = args.columns
    if args.id_no_print != None:
        selected_output = remove_rows_not_to_print(selected_output, 
                                                   args.id_no_print)
    n = args.n
    if n == None:
        n = len(selected_output)
    selected_output = selected_output[-n:]

    return selected_output, column_names

def remove_empty_columns(selected_output, column_names):
    if len(selected_output) == 0:
        return selected_output, column_names
    columns_to_remove = []
    for col in range(len(selected_output[0])):
        if not np.any(selected_output[:, col]):
            columns_to_remove.append(col)
    for i, original_col in enumerate(columns_to_remove):
        selected_output = np.delete(selected_output, original_col - i, 1)
        column_names = np.delete(column_names, original_col - i)
    return selected_output, column_names

def remove_columns_not_to_print(selected_output, column_names, columns_no_print):
    if len(selected_output) == 0:
        return selected_output
    columns_to_remove = []
    for i, col_name in enumerate(column_names):
        for col_name_no_print in columns_no_print:
            if col_name == col_name_no_print:
                columns_to_remove.append(i)
    for i, original_col in enumerate(columns_to_remove):
        selected_output = np.delete(selected_output, original_col - i, 1)
        column_names = np.delete(column_names, original_col - i)
    return selected_output, column_names

def remove_rows_not_to_print(selected_output, id_no_print):
    rows_to_remove = []
    for j in range(len(selected_output)):
        for i in id_no_print:
            if selected_output[j][0] == i:
                rows_to_remove.append(j)
    for j in rows_to_remove:
        selected_output = np.delete(selected_output, j, 0)
    return selected_output

def get_max_widths(selected_output, column_names, no_headers, extra_space):
    if len(selected_output) == 0:
        return selected_output
    widths = []
    for col in range(len(selected_output[0])):
        if no_headers:
            max_width = 0
        else:
            max_width = len(column_names[col])
        for row in range(len(selected_output)):
            if max_width < len(str(selected_output[row][col])):
                max_width = len(str(selected_output[row][col]))
        widths.append(max_width + extra_space)
    return widths 

def print_selected_parameters(selected_output, column_names, no_headers, max_width):
    extra_space = 2
    widths = get_max_widths(selected_output, column_names, no_headers, extra_space)
    if not no_headers:
        headers = ""
        total_width = 0
        for w, col in zip(widths, column_names):
            column_header = col + (w - len(col))*" "
            if max_width and w > max_width:
                column_header = column_header[:max_width] + extra_space*" "
                total_width += max_width + extra_space
            else:
                total_width += w
            headers += column_header
        print headers
        print total_width*"="
    for row in selected_output:
        line = ""
        for w, value in zip(widths, row):
            column_value = str(value) + (w - len(str(value)))*" "
            if max_width and w > max_width:
                column_value = column_value[:max_width] + extra_space*" "
            line += column_value
        print line
        
def main(argv=None):
    args = get_arguments(argv)

    if args.p != None:
        print_config = get_personalized_print_config(args.p)
        main(print_config.split())
        exit(0)

    database_name = get_database_name_from_settings()
    if database_name:
        db = sqlite3.connect(database_name)
    else:
        print "Could NOT find a path to a database in 'settings.txt'." \
            + "Add path to the database to 'settings.txt'."

    db_cursor = db.cursor()

    column_names, column_types = get_column_names_and_types(db_cursor)
    type_dict = dict(zip(column_names, column_types))

    selected_output, column_names = select_command(db_cursor, args, column_names)

    print_selected_parameters(selected_output, column_names, args.no_headers,
                              args.max_width)

    if args.column_names:
        print ""
        print "Column names and types in database:"
        for col_name in column_names:
            col_type = type_dict[col_name]
            print col_name, col_type

    db.commit()
    db_cursor.close()
    db.close()

if __name__ == '__main__':
    main()
