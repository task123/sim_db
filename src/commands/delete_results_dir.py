# -*- coding: utf-8 -*-
"""Delete results in 'results_dir' of specified simulation in the sim.db.

One must either provide a list of ID's or a condition to delete the results in 
'results_dir' as well as the directory itself of the corresponding simulations i
from the database.

Usage: python delete_results_dir.py -id 'ID'
       python delete_results_dir.py -where 'CONDITION'
"""
# Copyright (C) 2018 Håkon Austlid Taskén <hakon.tasken@gmail.com>
# Licenced under the MIT License.

import helpers
import argparse
import shutil

def command_line_arguments_parser():
    # yapf: disable
    parser = argparse.ArgumentParser(description="Delete results in 'results_dir' of specified simulations.")
    parser.add_argument('--id', '-i', type=int, nargs='+', default=[], help="ID's of simulation which 'results_dir' to deleted.")
    parser.add_argument('--where', '-w', type=str, default=None, help="Condition for which simulation's 'results_dir' to deleted. Must be a valid SQL (sqlite3) command when added after WHERE in a SELECT command.")
    # yapf: enable

    return parser


def delete_results_dir(argv=None):
    db = helpers.connect_sim_db()
    db_cursor = db.cursor()

    args = command_line_arguments_parser().parse_args(argv)
    if len(args.id) == 0 and args.where == None:
        print("No 'results_dir' was deleted. --id 'ID' or --where 'CONDITION' "
              + "must be passed to the program.")
        exit(0)

    results_dirs = []
    for delete_id in args.id:
        db_cursor.execute("SELECT results_dir FROM runs WHERE id = {0}".format(delete_id))
        results_dir = db_cursor.fetchone()[0]
        if results_dir != None:
            results_dirs.append(results_dir)

    if args.where:
        db_cursor.execute("SELECT results_dir FROM runs WHERE {0}".format(args.where))
        for selected_output in db_cursor.fetchall():
            if selected_output[0] != None:
                results_dirs.append(selected_output[0])

    db.commit()
    db_cursor.close()
    db.close()

    if len(results_dirs) > 0:
        print("Do you really want to delete the following directories and "
            "everything in them:")
        for results_dir in results_dirs:
            print(results_dir)
        answer = helpers.user_input("? (y/n)")
        if answer == 'y' or answer == 'Y' or answer == 'yes' or answer == 'Yes':
            for results_dir in results_dirs:
                shutil.rmtree(results_dir)
        else: 
            print("No results deleted.")
    else:
        print("No 'results_dir' to delete.")
 

if __name__ == '__main__':
    delete_results_dir()
