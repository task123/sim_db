# -*- coding: utf-8 -*-
"""Make a update in the database.

Usage: 
    python update_run.py --id 'ID' --columns 'COLUMN_NAME' --values 'NEW_VALUE'
    or python update_run.py --columns 'COLUMN_NAME_1' 'COLUMN_NAME_2'
                            --values 'NEW_VALUE_1' 'NEW_VALUE_2'
                            --where "'COLUMN_NAME_1' > 10"
"""
# Copyright (C) 2017, 2018 Håkon Austlid Taskén <hakon.tasken@gmail.com>
# Licenced under the MIT License.

if __name__ == '__main__':
    import add_root_dir_to_path

import src.command_line_tool.commands.helpers as helpers
import sqlite3
import argparse
import sys
import os.path


def command_line_arguments_parser(argv):
    if argv == None:
        argv = sys.argv[1:]
    elif (argv[0] != 'sim_db' and argv[0] != 'sdb' 
            and argv[0] != 'command_line_tool.py'):
        argv = ["update_sim.py", ""] + argv
    # yapf: disable
    parser = argparse.ArgumentParser(
        description='Update content in sim.db.', 
        prog="{0} {1}".format(argv[0], argv[1]))
    parser.add_argument('--id', '-i', type=int, default=None, help="ID of run to update.")
    parser.add_argument('--where', '-w', type=str, default="id > -1", help="Condition for which entries should be updated. Must be a valid SQL (sqlite3) command when added after WHERE in a UPDATE command.")
    parser.add_argument('--columns', '-c', type=str, nargs='+', required=True, help="<Required> Name of column to update in runs.")
    parser.add_argument('--values', '-v', type=str, nargs='+', required=True, help="<Required> New value updated at run with id and column as specifed.")
    parser.add_argument('--db_path', type=str, default=None, help="Full path to the database used.")
    # yapf: enable

    return parser.parse_args(argv[2:])


def update_sim(argv=None):
    args = command_line_arguments_parser(argv)
    if args.id == None and args.where == "id > -1":
        print("Nothing was updated. --id 'ID' or --where 'CONDITION' must be " \
              + "passed to the program.")
        exit(0)

    db = helpers.connect_sim_db(args.db_path)
    db_cursor = db.cursor()

    column_names, column_types = helpers.get_db_column_names_and_types(
            db_cursor)
    type_dict = dict(zip(column_names, column_types))

    condition = args.where
    if args.id:
        condition = condition + " AND id = {0}".format(args.id)
    for column, value in zip(args.columns, args.values):
        if type_dict[column] == 'TEXT':
            value = "'{0}'".format(value)
        db_cursor.execute("UPDATE runs SET {0} = {1} WHERE {2}" \
                          .format(column, value, condition))

    db.commit()
    db_cursor.close()
    db.close()


if __name__ == '__main__':
    update_sim()
