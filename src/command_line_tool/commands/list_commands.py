# -*- coding: utf-8 -*-
""" Print a list of all the sim_db commands.

These are the commands available after running: 'python generate_commands.py'.
"""
# Copyright (C) 2018 Håkon Austlid Taskén <hakon.tasken@gmail.com>
# Licenced under the MIT License.

import os
import fnmatch
import argparse
import sys


def command_line_arguments_parser(name_command_line_tool="sim_db", name_command="list_commands"):
    # yapf: disable
    parser = argparse.ArgumentParser(
        description="Print a list of all the sim_db commands.", 
        prog="{0} {1}".format(name_command_line_tool, name_command))
    # yapf: enable

    return parser


def list_commands(name_command_line_tool="sim_db", name_command="list_commands", argv=None):
    command_line_arguments_parser(name_command_line_tool, name_command).parse_args(argv)
    commands_dir = os.path.dirname(os.path.abspath(__file__))
    programs = fnmatch.filter(os.listdir(commands_dir), "*.py")
    programs.remove('helpers.py')
    programs.remove('__init__.py')
    programs.remove('add_root_dir_to_path.py')
    programs.append('cd_res / cd_results')
    programs.sort()
    print("All commands: ('command -h' will explain command and use.)\n")
    for program in programs:
        script_name = program.split('.')[0]
        if (len(script_name) > 4 and script_name[-4:] == '_sim'):
            script_name = script_name[:-4] + ' / ' + script_name
        if (len(script_name) > 5 and script_name[-5:] == '_sims'):
            script_name = script_name[:-5] + ' / ' + script_name       
        print(script_name)


if __name__ == '__main__':
    list_commands("", sys.argv[0], sys.argv[1:])
