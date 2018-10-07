# -*- coding: utf-8 -*-
"""Delete a row in the sim.db.

One must either provide a list of ID's or a condition to delete sets of 
simulation parameters (rows) from the database.

Usage: python delete_sim.py -id 'ID'
       python delete_sim.py -where 'CONDITION'
"""
# Copyright (C) 2017, 2018 Håkon Austlid Taskén <hakon.tasken@gmail.com>
# Licenced under the MIT License.

import helpers
import sqlite3
import argparse
import os.path


def command_line_arguments_parser():
    # yapf: disable
    parser = argparse.ArgumentParser(description='Delete simulations from sim.db.')
    parser.add_argument('--id', '-i', type=int, nargs='+', default=[], help="ID's of runs to delete.")
    parser.add_argument('--where', '-w', type=str, default=None, help="Condition for which entries should be deleted. Must be a valid SQL (sqlite3) command when added after WHERE in a DELETE command.")
    # yapf: enable

    return parser


def delete_sim(argv=None):
    db = helpers.connect_sim_db()
    db_cursor = db.cursor()

    args = command_line_arguments_parser().parse_args(argv)
    if len(args.id) == 0 and args.where == None:
        print("Nothing was deleted. --id 'ID' or --where 'CONDITION' must be " \
              + "passed to the program.")
        exit(0)

    for delete_id in args.id:
        db_cursor.execute("DELETE FROM runs WHERE id = {0}".format(delete_id))

    if args.where:
        db_cursor.execute("DELETE FROM runs WHERE {0}".format(args.where))

    db.commit()
    db_cursor.close()
    db.close()


if __name__ == '__main__':
    delete_sim()
