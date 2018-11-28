# -*- coding: utf-8 -*-
"""Test 'sim_db' functions for Python, C and C++.

Test the python, C and C++ version of the functions and methods used in 
external code for to interact with the database.
"""
# Copyright (C) 2017, 2018 Håkon Austlid Taskén <hakon.tasken@gmail.com>
# Licenced under the MIT License.

import add_package_root_to_path
import common_test_helpers
from sim_db.src_command_line_tool.command_line_tool import command_line_tool
import time


def test_python_functions(capsys):
    __run_python_functions(capsys, True)


def test_python_functions_without_storing_metadata(capsys):
    __run_python_functions(capsys, False)


def __run_python_functions(capsys, store_metadata):
    db_id = command_line_tool("sim_db", [
            "add_sim",
            "--filename",
            "{0}/sim_params_python_program.txt".format(common_test_helpers.get_test_dir())
    ], print_ids_added=False)
    if not store_metadata:
        run_command = __add_no_metadata_flag_to_run_command(capsys, db_id)
    command_line_tool("sim_db", "run_sim --id {0}".format(db_id).split())
    time.sleep(0.1)  # Wait for program.py to finish
    output_program, err_program = capsys.readouterr()
    command_line_tool("sim_db", "print_sim --id {0} -v --columns new_test_param1 new_test_param2 "
            "new_test_param3 new_test_param4 new_test_param5 new_test_param6 "
            "new_test_param7 new_test_param8 new_test_param9 new_test_param10 "
            "results_dir time_started used_walltime --no_headers"
            .format(db_id).split())
    output_print_sim, err_print_sim = capsys.readouterr()
    command_line_tool("sim_db", [
            "delete_sim",
            "--id", str(db_id), 
            "--no_checks"
    ])
    with capsys.disabled():
        if store_metadata:
            print("\nTest python methods...")
            if len(err_program) + len(err_print_sim) > 0:
                print(err_program)
                print(err_print_sim)
        else:
            print("\nTest python methods without storing metadata...")
            if len(err_program) + len(err_print_sim) > 0:
                print(err_program)
                print(err_print_sim)
    common_test_helpers.assert_output_python_program(output_program, db_id)
    common_test_helpers.assert_output_print_sim_after_run_sim(output_print_sim, store_metadata)


def __add_no_metadata_flag_to_run_command(capsys, db_id):
    command_line_tool("sim_db", 
            "print --id {0} -v --columns run_command --no_headers".format(
                    db_id).split())
    run_command, err = capsys.readouterr()
    run_command = run_command.strip() + " no_metadata"
    command_line_tool("sim_db", [
            "update_sim",
            "--id",
            str(db_id), "--columns", "run_command", "--values", run_command
    ])
    return run_command
