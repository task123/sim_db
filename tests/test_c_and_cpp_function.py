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
import os


def test_c_functions(capsys):
    common_test_helpers.skip_if_outside_sim_db()
    __c_functions(capsys, True)


def test_c_functions_without_storing_metadata(capsys):
    common_test_helpers.skip_if_outside_sim_db()
    __c_functions(capsys, False)


def __c_functions(capsys, store_metadata):
    db_id = command_line_tool("sim_db", [
            "add_sim",
            "--filename",
            "{0}/sim_params_c_program.txt".format(common_test_helpers.get_test_dir())
    ], print_ids_added=False)
    if not store_metadata:
        __add_no_metadata_flag_to_run_command(capsys, db_id)
    command_line_tool("sim_db", "run_sim --id {0}".format(db_id).split())
    time.sleep(0.1)  # Wait for c_program to finish
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
            print("\nTest C functions...")
            if len(err_program) + len(err_print_sim) > 0:
                print(err_program)
                print(err_print_sim)
        else:
            print("\nTest C functions without storing metadata...")
            if len(err_program) + len(err_print_sim) > 0:
                print(err_program)
                print(err_print_sim)
    ___output_c_and_cpp_program(output_program, db_id)
    common_test_helpers.assert_output_print_sim_after_run_sim(output_print_sim, 
                                                        store_metadata)


def test_cpp_functions(capsys):
    common_test_helpers.skip_if_outside_sim_db()
    __cpp_functions(capsys, True)


def test_cpp_functions_without_storing_metadata(capsys):
    common_test_helpers.skip_if_outside_sim_db()
    __cpp_functions(capsys, False)


def __cpp_functions(capsys, store_metadata):
    db_id = command_line_tool("sim_db", [
            "add_sim",
            "--filename",
            "{0}/sim_params_cpp_program.txt".format(common_test_helpers.get_test_dir())
    ], print_ids_added=False)
    if not store_metadata:
        __add_no_metadata_flag_to_run_command(capsys, db_id)
    command_line_tool("sim_db", "run_sim --id {0}".format(db_id).split())
    time.sleep(0.1)  # Wait for cpp_program to finish
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
            print("\nTest C++ methods...")
            if len(err_program) + len(err_print_sim) > 0:
                print(err_program)
                print(err_print_sim)
        else:
            print("\nTest C++ methods without storing metadata...")
            if len(err_program) + len(err_print_sim) > 0:
                print(err_program)
                print(err_print_sim)
    ___output_c_and_cpp_program(output_program, db_id)
    common_test_helpers.assert_output_print_sim_after_run_sim(output_print_sim, 
                                                        store_metadata)


def ___output_c_and_cpp_program(output_program, db_id):
    printed_lines = output_program.split('\n')
    if printed_lines[0] == "(May take 10-30 seconds.)":
        printed_lines = output_program.split('\n')[3:]
    printed_lines[0] == "3"
    printed_lines[1] == printed_lines[0]
    abs(float(printed_lines[2]) - -5000000000.0) < 0.001
    printed_lines[3] == printed_lines[2]
    printed_lines[4] == "hei"
    printed_lines[5] == printed_lines[4]
    printed_lines[6] == "1"
    printed_lines[7] == printed_lines[6]
    printed_lines[8:11] == ['1', '2', '3']
    printed_lines[8:11] == printed_lines[11:14]
    abs(float(printed_lines[14]) - 1.5) < 0.001
    abs(float(printed_lines[15]) - 2.5) < 0.001
    abs(float(printed_lines[16]) - 3.5) < 0.001
    printed_lines[14:17] == printed_lines[17:20]
    printed_lines[20:23] == ['a', 'b', 'c']
    printed_lines[20:23] == printed_lines[23:26]
    printed_lines[26:29] == ['1', '0', '1']
    printed_lines[26:29] == printed_lines[29:32]
    printed_lines[32] == "9"
    printed_lines[33] == printed_lines[32]
    printed_lines[34] == "11"
    printed_lines[35] == printed_lines[34]
    printed_lines[36] == str(db_id + 1)
    printed_lines[37] == "7"


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
