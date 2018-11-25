# -*- coding: utf-8 -*-
"""Delete a row in the sim.db.

One must either provide a list of ID's or a condition to delete sets of 
simulation parameters (rows) from the database.

Usage: python delete_sim.py --id 'ID'
       python delete_sim.py --where 'CONDITION'
"""
# Copyright (C) 2017, 2018 Håkon Austlid Taskén <hakon.tasken@gmail.com>
# Licenced under the MIT License.

if __name__ == '__main__':
    import add_root_dir_to_path

import src.command_line_tool.commands.delete_results_dir as delete_results_dir
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
        argv = ["delete_sim.py", ""] + argv
    # yapf: disable
    parser = argparse.ArgumentParser(
        description='Delete simulations from sim.db.', 
        prog="{0} {1}".format(argv[0], argv[1]))
    parser.add_argument('--id', '-i', type=int, nargs='+', default=[], help="ID's of runs to delete.")
    parser.add_argument('--where', '-w', type=str, default=None, help="Condition for which entries should be deleted. Must be a valid SQL (sqlite3) command when added after WHERE in a DELETE command.")
    parser.add_argument('--no_checks', action='store_true', help="No questions are asked about wheter you really want to delete simulation or the 'results_dir' of the simulation.")
    # yapf: enable

    return parser.parse_args(argv[2:])


def delete_sim(argv=None):
    db = helpers.connect_sim_db()
    db_cursor = db.cursor()

    args = command_line_arguments_parser(argv)

    answer = 'n'
    if len(args.id) == 0 and args.where == None:
        print("--id 'ID' or --where 'CONDITION' must be passed to the "
              "program.")
    elif len(args.id) > 0 and not args.no_checks:
        print("Do you really want to delete simulations with following ID's:")
        for delete_id in args.id:
            print(delete_id)
        answer = helpers.user_input("? (y/n)")
    elif args.where != None and not args.no_checks:
        print("Do you really want to delete simulations with following "
              "condition:")
        print(args.where)
        answer = helpers.user_input("? (y/n)")

    if (answer == 'y' or answer == 'Y' or answer == 'yes' or answer == 'Yes'
                or args.no_checks):
        if len(args.id) > 0:
            if args.no_checks:
                delete_results_dir_params = ['--no_checks', '--id']
            else:
                delete_results_dir_params = ['--id']
            for delete_id in args.id:
                delete_results_dir_params.append(str(delete_id))
            delete_results_dir.delete_results_dir(delete_results_dir_params)
        for delete_id in args.id:
            db_cursor.execute(
                    "DELETE FROM runs WHERE id = {0}".format(delete_id))

        if args.where:
            delete_results_dir.delete_results_dir(["--where", args.where])
            db_cursor.execute("DELETE FROM runs WHERE {0}".format(args.where))
    else:
        print("No simulations were deleted.")

    db.commit()
    db_cursor.close()
    db.close()


if __name__ == '__main__':
    delete_sim()