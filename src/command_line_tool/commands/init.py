# -*- coding: utf-8 -*-
"""Initialise 'sim_db'.

Must be called before using 'sim_db'.

This commands should be called from the top directory of your project or with
the path to the top directory as an argument.

The command will create a hidden directory called .sim_db and copy the default
settings into this directory.
"""
# Copyright (C) 2018 Håkon Austlid Taskén <hakon.tasken@gmail.com>
# Licenced under the MIT License.

import os
import argparse
import sys
import shutil


def command_line_arguments_parser(argv=None):
    if argv == None:
        argv = sys.argv[1:]
    elif (argv[0] != 'sim_db' and argv[0] != 'sdb' 
            and argv[0] != 'command_line_tool.py'):
        argv = ["init.py", ""] + argv
    # yapf: disable
    parser = argparse.ArgumentParser(
        description="Initialise 'sim_db' and must be called before using 'sim_db'. Will create a '.sim_db/' directory.", 
        prog="{0} {1}".format(argv[0], argv[1]))
    parser.add_argument('--path', type=str, default=None, help="Path to the top directory of project. If not passed as an argument, the current working directory is assumed to be the top directory.")
    # yapf: enable

    return parser.parse_args(argv[2:])


def init(argv=None):
    args = command_line_arguments_parser(argv)
    if args.path == None:
        args.path = os.getcwd()
    elif args.path[-1] == '/':
        args.path = args.path[:-1]
    os.mkdir(args.path + '/.sim_db')
    commands_dir = os.path.dirname(os.path.abspath(__file__))
    path_default_settings = os.path.join(commands_dir, os.path.join(os.pardir, 
            os.path.join(os.pardir, os.pardir))) + '/default_settings.txt'
    shutil.copyfile(path_default_settings, args.path + '/.sim_db/settings.txt')


if __name__ == '__main__':
    init()
