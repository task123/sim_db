# -*- coding: utf-8 -*-
"""Make a update in the database.

Usage: python update_run.py -id 'ID' -columns 'COLUMN_NAME' -values 'NEW_VALUE'
    or python update_run.py -columns 'COLUMN_NAME_1' 'COLUMN_NAME_2'
                            -values 'NEW_VALUE_1' 'NEW_VALUE_2'
                            -where 'COLUMN_NAME_1' > 10
"""
# Copyright (C) 2017 Håkon Austlid Taskén <hakon.tasken@gmail.com>
# Licenced under the MIT License.

from add_sim import get_database_name_from_settings
from add_sim import get_column_names_and_types
import sqlite3
import argparse
import os.path

def get_arguments():
    parser = argparse.ArgumentParser(description='Print content in sim_runs.db.')
    parser.add_argument('-id', type=int, default=None, help="ID of run to update.")
    parser.add_argument('-where', type=str, default="id > -1", help="Condition for which entries should be updated. Must be a valid SQL (sqlite3) command when added after WHERE in a DELETE command.")
    parser.add_argument('-columns', type=str, nargs='+', required=True, help="<Required> Name of column to update in runs.")
    parser.add_argument('-values', type=str, nargs='+', required=True, help="<Required> New value updated at run with id and column as specifed.")
    args = parser.parse_args()
    if args.id == None and args.where == "id > -1":
        print "Nothing was updated. -id 'ID' or -where 'CONDITION' must be passed to the program."
        exit(0)
    return args

def main():
    args = get_arguments()

    database_name = get_database_name_from_settings()
    if database_name:
        db = sqlite3.connect(database_name)
    else:
        print "Could NOT find a path to a database in 'settings.txt'." \
            + "Add path to the database to 'settings.txt'."

    db_cursor = db.cursor()

    column_names, column_types = get_column_names_and_types(db_cursor)
    type_dict = dict(zip(column_names, column_types))

    condition = args.where
    if args.id:
        condition = condition + " AND id = {}".format(args.id)
    for column, value in zip(args.columns, args.values):
        if type_dict[column] == 'TEXT':
            value = "'{}'".format(value)
        db_cursor.execute("UPDATE runs SET {0} = {1} WHERE {2}" \
                          .format(column, value, condition))

    db.commit()
    db_cursor.close()
    db.close()

if __name__ == '__main__':
    main()




