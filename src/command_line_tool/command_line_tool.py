# -*- coding: utf-8 -*-
"""Program that perform all the 'sim_db' commands.

Usually called from command line as '$ sim_db <command> <args>' or 
'$ sdb <command> <args>' after '$ make' is used to run 'genereate_progam.py'.

The 'sim_db' program runs simulations while keeping track of the simulation 
parameters, results and metadata.

Usage: 'python program.py <command> <args>'
"""
# Copyright (C) 2018 Håkon Austlid Taskén <hakon.tasken@gmail.com>
# Licenced under the MIT License.

if __name__ == '__main__':
    import add_root_dir_to_path

import src.command_line_tool.commands.add_and_run as add_and_run
import src.command_line_tool.commands.add_and_submit as add_and_submit
import src.command_line_tool.commands.add_column as add_column
import src.command_line_tool.commands.add_comment as add_comment
import src.command_line_tool.commands.add_range_sim as add_range_sim
import src.command_line_tool.commands.add_sim as add_sim
import src.command_line_tool.commands.combine_dbs as combine_dbs
import src.command_line_tool.commands.delete_empty_columns as delete_empty_columns
import src.command_line_tool.commands.delete_sim as delete_sim
import src.command_line_tool.commands.duplicate_and_run as duplicate_and_run
import src.command_line_tool.commands.duplicate_sim as duplicate_sim
import src.command_line_tool.commands.extract_params as extract_params
import src.command_line_tool.commands.get as get
import src.command_line_tool.commands.init as init
import src.command_line_tool.commands.list_commands as list_commands
import src.command_line_tool.commands.print_sim as print_sim
import src.command_line_tool.commands.run_serial_sims as run_serial_sims
import src.command_line_tool.commands.run_sim as run_sim
import src.command_line_tool.commands.settings as settings
import src.command_line_tool.commands.submit_sim as submit_sim
import src.command_line_tool.commands.update_sim as update_sim
import argparse
import sys
import os.path


def command_line_arguments_parser(argv):
    # yapf: disable
    parser = argparse.ArgumentParser(
            description="For running simulations and keeping track of its parameters, results and metadata.", 
            usage="""{0} [-h] <command> [<args>]

Some common sim_db commands:

    init           Initialise 'sim_db' for use in project.
    add            Add set of simulation parameters to database.    
    print          Print parameters in database.
    run            Run simulation with parameters from database.
    list_commands  List all available commands.
 
""".format(argv[0]))
    parser.add_argument('command', type=str, help="The command, 'list_commands', will print all available commands.")
    # yapf: enable

    return parser.parse_args(argv[1:2])


def command_line_tool(argv=None, print_ids_added=True):
    """Perfom command passed as argument.

    Can perform a number of commands run simulations and keeping track of its 
    parameters, results and metadata.

    Args:
        argv (list of str): Command to perform followed be the arguments to the
                            command.
        print_ids_added (bool): Set 'True' to print 'ID's', if added (or value 
                                from get). If 'False' and a non valid command 
                                is passed, a 'ValueError' is raised.
    """
    if argv == None:
        argv = sys.argv[1:]
    if (len(argv) == 0 or (argv[0] != 'sim_db' and argv[0] != 'sdb')):
        argv = ['command_line_tool.py'] + argv
    args = command_line_arguments_parser(argv)
    command = args.command
    res = None
    if command == 'add_and_run':
        last_id = add_and_run.add_and_run(argv)
        if print_ids_added:
            print("ID of last added: {0}".format(last_id))
        res = last_id
    elif command == 'add_and_submit':
        res = add_and_submit.add_and_submit(argv)
    elif command == 'add_column':
        add_column.add_column(argv)
    elif command == 'add_comment':
        res = add_comment.add_comment(argv)
    elif command == 'add_range' or command == 'add_range_sim':
        ids_added = add_range_sim.add_range_sim(argv)
        if print_ids_added:
            print("Added simulations with following ID's:")
            print(ids_added)
        res = ids_added
    elif command == 'add' or command == 'add_sim':
        last_id = add_sim.add_sim(argv)
        if print_ids_added:
            print("ID of last added: {0}".format(last_id))
        res = last_id
    elif command == 'cd_res_dir' or command == 'cd_results_dir':
        path_sim_db_cd_results = os.path.abspath(os.path.join(os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                'command_line_tool'), 'sim_db_cd_results.sh'))
        path_sim_db_cd_results = path_sim_db_cd_results.replace(" ", "\ ")
        os.system(path_sim_db_cd_results)
    elif command == 'combine_dbs':
        combine_dbs.combine_dbs(argv)
    elif command == 'delete_empty_columns':
        delete_empty_columns.delete_empty_columns(argv)
    elif command == 'delete_results_dir':
        delete_results_dir.delete_results_dir(argv)
    elif command == 'delete' or command == 'delete_sim':
        delete_sim.delete_sim(argv)
    elif command == 'duplicate_and_run':
        db_id = duplicate_and_run.duplicate_and_run(argv)
        if print_ids_added:
            print("ID of new simulation: {0}".format(db_id))
        res = db_id
    elif command == 'duplicate' or command == 'duplicate_sim':
        db_id = duplicate_sim.duplicate_sim(argv)
        if print_ids_added:
            print("ID of new simulation: {0}".format(db_id))
        res = db_id
    elif command == 'extract_params':
        extract_params.extract_params(argv)
    elif command == 'get':
        value = get.get(argv)
        if print_ids_added:
            print(value)
        res = value
    elif command == 'init':
        init.init(argv)
    elif command == 'list_commands':
        list_commands.list_commands(argv)
    elif command == 'list_print_configs':
        list_print_configs.list_print_configs(argv)
    elif command == 'print' or command == 'print_sim':
        print_sim.print_sim(argv)
    elif command == 'run_serial' or command == 'run_serial_sims':
        run_serial_sims.run_serial_sims(argv)
    elif command == 'run' or command == 'run_sim':
        run_sim.run_sim(argv)
    elif command == 'settings':
        settings.settings(argv)
    elif command == 'submit' or command == 'submit_sim':
        res = submit_sim.submit_sim(argv)
    elif command == 'update' or command == 'update_sim':
        update_sim.update_sim(argv)
    else:
        if print_ids_added:
            print("'{0}' is not a {1} command. See '{1} list_commands' for "
                  "available commands.".format(command, argv[1]))
        else:
            raise ValueError
    if res != None:
        return res


if __name__ == '__main__':
    command_line_tool()
