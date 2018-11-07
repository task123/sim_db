# -*- coding: utf-8 -*-
""" Run a simulation, by running the 'run_command' with 'ID' in database.

Usage: 'python run_sim.py --id ID'
"""
# Copyright (C) 2017, 2018 Håkon Austlid Taskén <hakon.tasken@gmail.com>
# Licenced under the MIT License.

if __name__ == '__main__':
    import add_root_dir_to_path

import src.commands.helpers as helpers
import src.commands.update_sim as update_sim
import argparse
import sqlite3
import subprocess
import sys


def command_line_arguments_parser():
    # yapf: disable
    parser = argparse.ArgumentParser(description='Run simulation with ID in database.')
    parser.add_argument('--id', '-i', type=int, default=None, help="'ID' of the simulation parameters in the 'sim.db' database that should be used in the simulation.")
    parser.add_argument('-n', type=int, default=None, help="Number of threads/core to run the simulation on.")
    # yapf: enable

    return parser


def run_sim(argv=None):
    """Run simulation with parameters with ID passed or the highest ID."""
    args = command_line_arguments_parser().parse_args(argv)

    db = helpers.connect_sim_db()
    db_cursor = db.cursor()
    if args.id == None:
        db_cursor.execute("SELECT id FROM runs WHERE status = 'new';")
        ids = db_cursor.fetchall()
        ids = [i[0] for i in ids]
        args.id = max(ids)
        print("Start simulation with ID {0}.".format(args.id))

    run_command = helpers.get_run_command(db_cursor, args.id, args.n)
    db.commit()
    db_cursor.close()
    db.close()
    update_sim.update_sim([
            "--id",
            str(args.id), "--columns", "cpu_info", "--values",
            helpers.get_cpu_and_mem_info()
    ])
    update_sim.update_sim([
            "--id",
            str(args.id), "--columns", "status", "--values", "running"
    ])

    for command in run_command.split(';'):
        process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True)
        if sys.version_info[0] < 3:
            for line in iter(process.stdout.readline, ''):
                sys.stdout.write(line.decode('UTF-8'))
                sys.stdout.flush()
            for line in iter(process.stderr.readline, ''):
                sys.stdout.write(line.decode('UTF-8'))
                sys.stdout.flush()
        else:
            for line in iter(process.stdout.readline, b''):
                sys.stdout.write(line.decode('UTF-8'))
                sys.stdout.flush()
            for line in iter(process.stderr.readline, b''):
                sys.stdout.write(line.decode('UTF-8'))
                sys.stdout.flush()
    update_sim.update_sim([
            "--id",
            str(args.id), "--columns", "status", "--values", "finished"
    ])


if __name__ == '__main__':
    run_sim()
