# -*- coding: utf-8 -*-
""" Used by a bash function to change directory to the 'results_dir' of a simulation."""

# Copyright (C) 2018 Håkon Austlid Taskén <hakon.tasken@gmail.com>
# Licenced under the MIT License.

if __name__ == '__main__':
    import add_root_dir_to_path

import src.command_line_tool.commands.helpers as helpers
import argparse
import sys
import os


def command_line_arguments_parser(argv):
    if argv == None:
        argv = sys.argv[1:]
    elif (argv[0] != 'sim_db' and argv[0] != 'sdb' 
            and argv[0] != 'command_line_tool.py'):
        argv = ["get.py", ""] + argv
    # yapf: disable
    parser = argparse.ArgumentParser(
        description="Get value from 'column' of simulation specified or last entry if not specified.",
        prog="{0} {1}".format(argv[0], argv[1]))
    parser.add_argument('column', type=str, help="Column in database from where to get the value.")
    parser.add_argument('--id', '-i', type=int, help="'ID' of the simulation in the 'sim.db' database.")
    parser.add_argument('-n', type=int, help="n'th last entry in the 'sim.db' database. (zero indexed)")
    # yapf: enable

    return parser.parse_args(argv[2:])


def get(argv=None):
    args = command_line_arguments_parser(argv)

    db = helpers.connect_sim_db()
    db_cursor = db.cursor()

    if args.id != None:
        db_cursor.execute("SELECT {0} FROM runs WHERE id={1}"
                .format(args.column, args.id))
        value = db_cursor.fetchone()[0]
    else:
        db_cursor.execute("SELECT {0} FROM runs".format(args.column))
        if args.n == None:
            args.n = 0
        value = db_cursor.fetchall()
        if len(value) > args.n:
            value = value[len(value) - args.n - 1][0]

    db.commit()
    db_cursor.close()
    db.close()

    if value == None:
        print("Specified simulation does not have a value in the {0} column."
              .format(args.column))
        exit()

    value.replace(" ", "\ ")
    return value


if __name__ == '__main__':
    print(get())