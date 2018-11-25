# -*- coding: utf-8 -*-
""" Add a new column to the database.

If the column already exists, then nothing happens.

Usage: 'python add_column.py -column NAME'
"""
# Copyright (C) 2017, 2018 Håkon Austlid Taskén <hakon.tasken@gmail.com>
# Licenced under the MIT License.

if __name__ == '__main__':
    import add_root_dir_to_path

import src.command_line_tool.commands.helpers as helpers
import sqlite3
import argparse
import sys


def command_line_arguments_parser(argv):
    if argv == None:
        argv = sys.argv[1:]
    elif (argv[0] != 'sim_db' and argv[0] != 'sdb' 
            and argv[0] != 'command_line_tool.py'):
        argv = ["add_column.py", ""] + argv
    # yapf: disable
    parser = argparse.ArgumentParser(
        description='Add column to database.', 
        prog="{0} {1}".format(argv[0], argv[1]))
    parser.add_argument('--column', '-c', type=str, required=True, help="<Required> Name of the new column.")
    parser.add_argument('--type', '-t', type=str, required=True, help="<Required> Type of the column. 'INTEGER', 'REAL', 'TEXT', 'int', 'float', 'string', 'bool' and 'int/float/string/bool array' are the valid choices.")
    # yapf: enable

    return parser.parse_args(argv[2:])


def add_column(argv=None):
    db = helpers.connect_sim_db()
    db_cursor = db.cursor()

    column_names, column_types = helpers.get_db_column_names_and_types(
            db_cursor)

    args = command_line_arguments_parser(argv)
    if args.column not in column_names:
        if args.type == 'int' or args.type == int:
            db_cursor.execute("ALTER TABLE runs ADD COLUMN \
                               {0} INTEGER".format(args.column))
        elif args.type == 'float' or args.type == float:
            db_cursor.execute("ALTER TABLE runs ADD COLUMN \
                               {0} REAL".format(args.column))
        else:
            db_cursor.execute("ALTER TABLE runs ADD COLUMN \
                               {0} TEXT".format(args.column))

    db.commit()
    db_cursor.close()
    db.close()


if __name__ == '__main__':
    add_column()