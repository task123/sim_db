# -*- coding: utf-8 -*-
""" Duplicate a set of simulation parameters found in sim_db's database.

The 'ID' of a set of simulation parameters if passed to 'duplicate_sim.py' and
a new set of almost identically simulation parameters will be created. The only
parameters that are NOT identical is the 'id', which will be unique, and 
'status', which will be set to 'new'.

Usage: 'python duplicate_sim.py --id ID' or 'python add_sim.py -i ID'
"""
# Copyright (C) 2018 Håkon Austlid Taskén <hakon.tasken@gmail.com>
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
        argv = ["print.py", ""] + argv
    # yapf: disable
    parser = argparse.ArgumentParser(
        description="Duplicate simulation in database. All parameters (including possible results) of specified simulation is duplicated with the exception of 'id' and 'status', which is kept unique and set to 'new' respectfully.", 
        prog="{0} {1} ".format(argv[0], argv[1]))
    parser.add_argument('--id', '-i', type=int, required=True, help="<Required> 'ID' of the simulation parameters in the 'sim.db' database that should be duplicated.")
    # yapf: enable

    return parser.parse_args(argv[2:])

def duplicate_sim(argv=None):
    args = command_line_arguments_parser(argv)

    db = helpers.connect_sim_db()
    db_cursor = db.cursor()

    db_cursor.execute("CREATE TEMPORARY TABLE tmp AS SELECT * FROM runs WHERE "
            "id = {0};".format(args.id))
    db_cursor.execute("UPDATE tmp SET id = NULL;")
    db_cursor.execute("UPDATE tmp SET status = 'new';")
    db_cursor.execute("INSERT INTO runs SELECT * FROM tmp;")
    db_id = db_cursor.lastrowid
    db_cursor.execute("DROP TABLE tmp")

    db.commit()
    db_cursor.close()
    db.close()

    return db_id

if __name__ == '__main__':
    db_id = duplicate_sim()
    print("ID of new simulation: {0}".format(db_id))
