# -*- coding: utf-8 -*-
"""Print and change the settings.

Pass either 'print', 'add' or 'remove' as commands.

usage: python settings <command> <args>
"""
# Copyright (C) 2017, 2018 Håkon Austlid Taskén <hakon.tasken@gmail.com>
# Licenced under the MIT License.

if __name__ == '__main__':
    import add_root_dir_to_path

import src.command_line_tool.commands.helpers as helpers
import argparse
import sys


def command_line_arguments_parser(argv):
    if argv == None:
        argv = sys.argv[1:]
    elif (argv[0] != 'sim_db' and argv[0] != 'sdb' 
            and argv[0] != 'command_line_tool.py'):
        argv = ["settings.py", ""] + argv
    # yapf: disable
    parser = argparse.ArgumentParser(
        description="Print and change settings. The settings can also be changed be editing the '.sim_db/settings.txt' file.", 
        prog="{0} {1}".format(argv[0], argv[1]))
    parser.add_argument('command', type=str, help="'print', 'add' or 'remove'")
    # yapf: enable

    return parser.parse_args(argv[2:3])


def parser_for_print(argv):
    if argv == None:
        argv = sys.argv[1:]
    elif (argv[0] != 'sim_db' and argv[0] != 'sdb' 
            and argv[0] != 'command_line_tool.py'):
        argv = ["settings.py", ""] + argv
    # yapf: disable
    parser = argparse.ArgumentParser(
        description="Print the current settings.",
        usage="{0} {1} print".format(argv[0], argv[1]))
    parser.add_argument('--setting', '-s', type=str, default=None, help="Which setting to print. If no setting is specified, the entire setting file is printed.")
    # yapf: enable

    return parser.parse_args(argv[3:])


def parser_for_add(argv):
    if argv == None:
        argv = sys.argv[1:]
    elif (argv[0] != 'sim_db' and argv[0] != 'sdb' 
            and argv[0] != 'command_line_tool.py'):
        argv = ["settings.py", ""] + argv
    # yapf: disable
    parser = argparse.ArgumentParser(
        description="Add a line to the settings.",
        usage="{0} {1} print".format(argv[0], argv[1]))
    parser.add_argument('--line', '-l', type=str, required=True, help="<Required> Line added to 'setting' in the settings.")
    parser.add_argument('--setting', '-s', type=str, required=True, help="<Required> Which setting to add a line to.")
    # yapf: enable

    return parser.parse_args(argv[3:])


def parser_for_remove(argv):
    if argv == None:
        argv = sys.argv[1:]
    elif (argv[0] != 'sim_db' and argv[0] != 'sdb' 
            and argv[0] != 'command_line_tool.py'):
        argv = ["settings.py", ""] + argv
    # yapf: disable
    parser = argparse.ArgumentParser(
        description="Remove a line from the settings.",
        usage="{0} {1} print".format(argv[0], argv[1]))
    parser.add_argument('--line', '-l', type=str, required=True, help="<Required> Line to remove from 'setting' in the settings.")
    parser.add_argument('--setting', '-s', type=str, required=True, help="<Required> Which setting to remove a line from.")
    # yapf: enable

    return parser.parse_args(argv[3:])


def settings(argv=None):
    args = command_line_arguments_parser(argv)
    command = args.command
    if command == 'print':
        args = parser_for_print(argv)
        if args.setting == None:
            settings_file = open(helpers.get_dot_sim_db_dir_path() + '/settings.txt', 'r')
            for line in settings_file.readlines():
                print(line)
            settings_file.close()
        else:
            settings = helpers.Settings()
            if args.setting not in settings.settings_dict:
                print("{0} is NOT a valid setting.".format(args.setting))
                print("\nChoose on of the following settings:")
                for setting_key in settings.settings_dict.keys():
                    print(setting_key)
                exit(1)
            for line in settings.read(args.setting):
                print(line)
    elif command == 'add':
        args = parser_for_add(argv)
        settings = helpers.Settings()
        if args.setting not in settings.settings_dict:
            print("{0} is NOT a valid setting.".format(args.setting))
            print("\nChoose on of the following settings:")
            for setting_key in settings.settings_dict.keys():
                print(setting_key)
            exit(1)
        settings.add(args.setting, args.line)
    elif command == 'remove':
        args = parser_for_remove(argv)
        settings = helpers.Settings()
        if args.setting not in settings.settings_dict:
            print("{0} is NOT a valid setting.".format(args.setting))
            print("\nChoose on of the following settings:")
            for setting_key in settings.settings_dict.keys():
                print(setting_key)
            exit(1)
        is_removed = settings.remove(args.setting, args.line)
        if not is_removed:
            print("'{0}' was NOT found under the '{1}' settings.\nIt was "
                  "therefor NOT removed from the settings."
                  .format(args.line, args.setting))
    else:
        print("'{0}' is not a valid command. 'print', 'add' and 'remove' are "
              "the valid commands.".format(command))


if __name__ == '__main__':
    settings()
