# -*- coding: utf-8 -*-
""" Used by a bash function to change directory to the 'results_dir' of a simulation."""

# Copyright (C) 2018 Håkon Austlid Taskén <hakon.tasken@gmail.com>
# Licenced under the MIT License.

if __name__ == '__main__':
    import add_root_dir_to_path

import src.commands.helpers as helpers
import argparse
import os


def command_line_arguments_parser():
    # yapf: disable
    parser = argparse.ArgumentParser(description="Return full path to 'results_dir' of simulation specified, of last entry if unspecified. Used by a bash function, 'cd_results', to change directory to this 'results_dir'.")
    parser.add_argument('--id', '-i', type=int, help="'ID' of the 'results_dir' in the 'sim.db' database.")
    parser.add_argument('-n', type=int, help="n'th last entry in the 'sim.db' database. (zero indexed)")
    # yapf: enable

    return parser


def cd_results(argv=None):
    args = command_line_arguments_parser().parse_args(argv)

    db = helpers.connect_sim_db()
    db_cursor = db.cursor()

    if args.id != None:
        db_cursor.execute("SELECT results_dir FROM runs WHERE id={0}".format(
                args.id))
        results_dir = db_cursor.fetchone()[0]
    else:
        db_cursor.execute("SELECT results_dir FROM runs")
        if args.n == None:
            args.n = 0
        results_dir = db_cursor.fetchall()
        if len(results_dir) > args.n:
            results_dir = results_dir[len(results_dir) - args.n - 1][0]

    db.commit()
    db_cursor.close()
    db.close()

    if results_dir == None:
        print("Specified simulation does not have a 'results_dir' path.")
        exit()

    results_dir.replace(" ", "\ ")
    return results_dir


if __name__ == '__main__':
    print(cd_results())
