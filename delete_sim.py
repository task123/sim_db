# -*- coding: utf-8 -*-
"""Delete a row in the sim_runs.db.

One must either provide a list of ID's or a condition to delete sets of 
simulation parameters (rows) from sim_runs.db.

Usage: python delete_run.py -id 'ID'
       python delete_run.py -where 'CONDITION'
"""
# Copyright (C) 2017 Håkon Austlid Taskén <hakon.tasken@gmail.com>
# Licenced under the MIT License.

from add_sim import get_database_name_from_settings
import sqlite3
import argparse
import os.path

def get_arguments():
    parser = argparse.ArgumentParser(description='Print content in sim_runs.db.')
    parser.add_argument('-id', type=int, nargs='+', default=[], help="ID's of runs to delete.")
    parser.add_argument('-where', type=str, default=None, help="Condition for which entries should be deleted. Must be a valid SQL (sqlite3) command when added after WHERE in a DELETE command.")
    args = parser.parse_args() 
    if len(args.id) == 0 and args.where == None:
        print "Nothing was deleted. -id 'ID' or -where 'CONDITION' must be passed to the program."
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

    for delete_id in args.id:
        db_cursor.execute("DELETE FROM runs WHERE id = {}".format(delete_id))

    if args.where:
        db_cursor.execute("DELETE FROM runs WHERE {}".format(args.where))

    db.commit()
    db_cursor.close()
    db.close()

if __name__ == '__main__':
    main()




