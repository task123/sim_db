# -*- coding: utf-8 -*-
""" Print a list of all the personalized print configurations.

These are the print configurations specified in 'settings.txt' and can be 
modified there. The name of each configuration will be printed followd by the
flags they are shortcuts for.

Usage: 'python print_sim.py -p NAME_PERSONALIZED_PRINT_CONFIGURATION'
"""
# Copyright (C) 2018 Håkon Austlid Taskén <hakon.tasken@gmail.com>
# Licenced under the MIT License.

if __name__ == '__main__':
    import add_root_dir_to_path

import src.command_line_tool.commands.helpers as helpers
import argparse
import sys


def command_line_arguments_parser(argv=None):
    if argv == None:
        argv = sys.argv[1:]
    elif (argv[0] != 'sim_db' and argv[0] != 'sdb' 
            and argv[0] != 'command_line_tool.py'):
        argv = ["list_print_configs.py", ""] + argv
    # yapf: disable
    parser = argparse.ArgumentParser(
        description="Print a list of all the personalized print configurations.", 
        prog="{0} {1}".format(argv[0], argv[1]))
    # yapf: enable

    return parser.parse_args(argv[2:])


def list_print_configs():
    command_line_arguments_parser()
    settings = helpers.Settings()
    print_configs = settings.read('print_config')
    for print_config in print_configs:
        print(print_config)


if __name__ == '__main__':
    list_print_configs()
