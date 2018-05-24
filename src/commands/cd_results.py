# -*- coding: utf-8 -*-
""" Used by a bash function to change directory to the 'result_dir' of a simulation."""

# Copyright (C) 2018 Håkon Austlid Taskén <hakon.tasken@gmail.com>
# Licenced under the MIT License.

import helpers
import argparse
import os


def command_line_arguments_parser():
    # yapf: disable
    parser = argparse.ArgumentParser(description="Return full path to 'result_dir' of simulation with provided id, '-i ID'. Used by a bash function, 'cd_results', to change directory to this 'result_dir'.")
    parser.add_argument('--id', '-i', type=int, required=True, help="<Required> 'ID' of the 'result_dir' in the 'sim.db' database.")
    # yapf: enable

    return parser


def cd_results(argv=None):
    args = command_line_arguments_parser().parse_args(argv)

    db = helpers.connect_sim_db()
    db_cursor = db.cursor()

    db_cursor.execute("SELECT result_dir FROM runs WHERE id={0}".format(
            args.id))
    result_dir = db_cursor.fetchone()[0]

    db.commit()
    db_cursor.close()
    db.close()

    return result_dir


if __name__ == '__main__':
    print(cd_results())
