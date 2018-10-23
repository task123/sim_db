# -*- coding: utf-8 -*-
""" Test 'sim_db'.

Test all the python scripts called by the commands, the python, C and C++ 
version of the functions and methods used in external code for to interact with
the database.
"""
# Copyright (C) 2017, 2018 Håkon Austlid Taskén <hakon.tasken@gmail.com>
# Licenced under the MIT License.

import add_sim
import print_sim
import delete_sim
import run_sim
import list_sim_db_commands
import add_and_run
import add_column
import helpers
import delete_empty_columns
import extract_params
import update_sim
import add_comment
import cd_results
import submit_sim
import add_and_submit
import add_range_sim
import run_serial_sims
import combine_dbs
import os
import time
import subprocess
import shutil

def setup_module(module):
    """Clean up 'results/' directory."""
    for entry in os.listdir(__get_test_dir() + '/results'):
        if os.path.isdir(__get_test_dir() + '/results/' + entry):
            shutil.rmtree(__get_test_dir() + '/results/' + entry)

def test_add_sim_print_sim_and_delete_sim(capsys):
    db_id = add_sim.add_sim([
            "--filename",
            "{0}/sim_params_python_program.txt".format(__get_test_dir())
    ])
    print_sim.print_sim("--id {0} -v --no_headers --columns name test_param1 "
           "test_param2 test_param3 test_param4 test_param5 test_param6 "
           "test_param7 test_param8 test_param9 test_param10 test_param11 "
           "test_param12".format(db_id).split())
    output_print_sim, err = capsys.readouterr()
    del_sim_params = "--id {0}".format(db_id).split()
    del_sim_params.append("--no_check")
    delete_sim.delete_sim(del_sim_params)
    print_sim.print_sim("-n 1 --no_headers --columns id".split())
    output_after_delete, err = capsys.readouterr()
    with capsys.disabled():
        print("\nTest add_sim, print_sim and delete_sim...")
    __assert_output_print_sim_after_add_sim(output_print_sim)

    # Test that the added simulation parameters are deleted
    assert (len(output_after_delete) == 0
            or output_after_delete != "{0}".format(db_id))


def __get_test_dir():
    return os.path.dirname(os.path.abspath(__file__))


def __assert_output_print_sim_after_add_sim(output_print_sim):
    printed_params = output_print_sim.split('\n')[0::2]
    printed_params = [param.strip() for param in printed_params]
    assert printed_params[0] == "test_sim"
    assert printed_params[1] == "3"
    assert printed_params[2] == "-5000000000.0"
    assert printed_params[3] == "hei"
    assert printed_params[4] == "True"
    assert printed_params[5] == "int[1, 2, 3]"
    assert printed_params[6] == "float[1.5, 2.5, 3.5]"
    assert printed_params[7] == "string[a, b, c]"
    assert printed_params[8] == "bool[True, False, True]"
    assert printed_params[9] == "9"
    assert printed_params[10] == "11"
    assert printed_params[11] == "None"
    assert printed_params[12] == "None"


def test_run_sim_and_python_functions(capsys):
    __run_sim_and_python_functions(capsys, True)


def test_python_functions_without_storing_metadata(capsys):
    __run_sim_and_python_functions(capsys, False)


def __run_sim_and_python_functions(capsys, store_metadata):
    db_id = add_sim.add_sim([
            "--filename",
            "{0}/sim_params_python_program.txt".format(__get_test_dir())
    ])
    if not store_metadata:
        run_command = __add_no_metadata_flag_to_run_command(capsys, db_id)
    run_sim.run_sim("--id {0}".format(db_id).split())
    time.sleep(0.1)  # Wait for program.py to finish
    output_program, err_program = capsys.readouterr()
    print_sim.print_sim("--id {0} -v --columns new_test_param1 new_test_param2 "
            "new_test_param3 new_test_param4 new_test_param5 new_test_param6 "
            "new_test_param7 new_test_param8 new_test_param9 new_test_param10 "
            "results_dir time_started used_walltime --no_headers"
            .format(db_id).split())
    output_print_sim, err_print_sim = capsys.readouterr()
    del_sim_params = "--id {0}".format(db_id).split()
    del_sim_params.append("--no_checks")
    delete_sim.delete_sim(del_sim_params)
    with capsys.disabled():
        if store_metadata:
            print("\nTest run_sim and python methods...")
            if len(err_program) + len(err_print_sim) > 0:
                print(err_program)
                print(err_print_sim)
        else:
            print("\nTest python methods without storing metadata...")
            if len(err_program) + len(err_print_sim) > 0:
                print(err_program)
                print(err_print_sim)
    __assert_output_python_program(output_program)
    __assert_output_print_sim_after_run_sim(output_print_sim, store_metadata)


def __add_no_metadata_flag_to_run_command(capsys, db_id):
    print_sim.print_sim(
            "--id {0} -v --columns run_command --no_headers".format(
                    db_id).split())
    run_command, err = capsys.readouterr()
    run_command = run_command.strip() + " no_metadata"
    update_sim.update_sim([
            "--id",
            str(db_id), "--columns", "run_command", "--values", run_command
    ])
    return run_command


def __assert_output_python_program(output_program):
    printed_params = output_program.split('\n')
    assert printed_params[0] == "3"
    assert printed_params[1] == printed_params[0]
    assert printed_params[2] == "-5000000000.0"
    assert printed_params[3] == printed_params[2]
    assert printed_params[4] == "hei"
    assert printed_params[5] == printed_params[4]
    assert printed_params[6] == "True"
    assert printed_params[7] == printed_params[6]
    assert printed_params[8] == "[1, 2, 3]"
    assert printed_params[9] == printed_params[8]
    assert printed_params[10] == "[1.5, 2.5, 3.5]"
    assert printed_params[11] == printed_params[10]
    assert printed_params[12] == "['a', 'b', 'c']"
    assert printed_params[13] == printed_params[12]
    assert printed_params[14] == "[True, False, True]"
    assert printed_params[15] == printed_params[14]
    assert printed_params[16] == "9"
    assert printed_params[17] == printed_params[16]
    assert printed_params[18] == "11"
    assert printed_params[19] == printed_params[18]
    assert printed_params[20] == "None"
    assert printed_params[21] == "None"


def __assert_output_print_sim_after_run_sim(output_print_sim, store_metadata):
    printed_params = output_print_sim.split('\n')[0::2]
    printed_params = [param.strip() for param in printed_params]
    assert printed_params[0] == "3"
    assert printed_params[1] == "-5000000000.0"
    assert printed_params[2] == "hei"
    assert printed_params[3] == "True"
    assert printed_params[4] == "int[1, 2, 3]"
    assert printed_params[5] == "float[1.5, 2.5, 3.5]"
    assert printed_params[6] == "string[a, b, c]"
    assert printed_params[7] == "bool[True, False, True]"
    assert printed_params[8] == "9"
    assert printed_params[9] == "11"
    if store_metadata:
        assert printed_params[10] != 'None'
        assert printed_params[11] != 'None'
        assert printed_params[12] != 'None'
    else:
        assert printed_params[10] == 'None'
        assert printed_params[11] == 'None'
        assert printed_params[12] == 'None'


def test_c_functions(capsys):
    __c_funcionts(capsys, True)


def test_c_functions_without_storing_metadata(capsys):
    __c_funcionts(capsys, False)


def __c_funcionts(capsys, store_metadata):
    db_id = add_sim.add_sim([
            "--filename",
            "{0}/sim_params_c_program.txt".format(__get_test_dir())
    ])
    if not store_metadata:
        __add_no_metadata_flag_to_run_command(capsys, db_id)
    run_sim.run_sim("--id {0}".format(db_id).split())
    time.sleep(0.1)  # Wait for c_program to finish
    output_program, err_program = capsys.readouterr()
    print_sim.print_sim("--id {0} -v --columns new_test_param1 new_test_param2 "
            "new_test_param3 new_test_param4 new_test_param5 new_test_param6 "
            "new_test_param7 new_test_param8 new_test_param9 new_test_param10 "
            "results_dir time_started used_walltime --no_headers"
            .format(db_id).split())
    output_print_sim, err_print_sim = capsys.readouterr()
    del_sim_params = "--id {0}".format(db_id).split()
    del_sim_params.append("--no_checks")
    delete_sim.delete_sim(del_sim_params)
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
    __assert_output_c_and_cpp_program(output_program)
    __assert_output_print_sim_after_run_sim(output_print_sim, store_metadata)


def test_cpp_functions(capsys):
    __cpp_functions(capsys, True)


def test_cpp_functions_without_storing_metadata(capsys):
    __cpp_functions(capsys, False)


def __cpp_functions(capsys, store_metadata):
    db_id = add_sim.add_sim([
            "--filename",
            "{0}/sim_params_cpp_program.txt".format(__get_test_dir())
    ])
    if not store_metadata:
        __add_no_metadata_flag_to_run_command(capsys, db_id)
    run_sim.run_sim("--id {0}".format(db_id).split())
    time.sleep(0.1)  # Wait for cpp_program to finish
    output_program, err_program = capsys.readouterr()
    print_sim.print_sim("--id {0} -v --columns new_test_param1 new_test_param2 "
            "new_test_param3 new_test_param4 new_test_param5 new_test_param6 "
            "new_test_param7 new_test_param8 new_test_param9 new_test_param10 "
            "results_dir time_started used_walltime --no_headers"
            .format(db_id).split())
    output_print_sim, err_print_sim = capsys.readouterr()
    del_sim_params = "--id {0}".format(db_id).split()
    del_sim_params.append("--no_checks")
    delete_sim.delete_sim(del_sim_params)
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
    __assert_output_c_and_cpp_program(output_program)
    __assert_output_print_sim_after_run_sim(output_print_sim, store_metadata)


def __assert_output_c_and_cpp_program(output_popen):
    printed_lines = output_popen.split('\n')
    if printed_lines[0] == "(May take 10-30 seconds.)":
        printed_lines = output_popen.split('\n')[3:]
    assert printed_lines[0] == "3"
    assert printed_lines[1] == printed_lines[0]
    assert abs(float(printed_lines[2]) - -5000000000.0) < 0.001
    assert printed_lines[3] == printed_lines[2]
    assert printed_lines[4] == "hei"
    assert printed_lines[5] == printed_lines[4]
    assert printed_lines[6] == "1"
    assert printed_lines[7] == printed_lines[6]
    assert printed_lines[8:11] == ['1', '2', '3']
    assert printed_lines[8:11] == printed_lines[11:14]
    assert abs(float(printed_lines[14]) - 1.5) < 0.001
    assert abs(float(printed_lines[15]) - 2.5) < 0.001
    assert abs(float(printed_lines[16]) - 3.5) < 0.001
    assert printed_lines[14:17] == printed_lines[17:20]
    assert printed_lines[20:23] == ['a', 'b', 'c']
    assert printed_lines[20:23] == printed_lines[23:26]
    assert printed_lines[26:29] == ['1', '0', '1']
    assert printed_lines[26:29] == printed_lines[29:32]
    assert printed_lines[32] == "9"
    assert printed_lines[33] == printed_lines[32]
    assert printed_lines[34] == "11"
    assert printed_lines[35] == printed_lines[34]


def test_add_and_run(capsys):
    db_id = add_and_run.add_and_run([
            "--filename",
            "{0}/sim_params_python_program.txt".format(__get_test_dir())
    ])
    time.sleep(0.1)  # Wait for program.py to finish
    output_program, err = capsys.readouterr()
    print_sim.print_sim("--id {0} -v --no_headers --columns name test_param1 "
            "test_param2 test_param3 test_param4 test_param5 test_param6 "
            "test_param7 test_param8 test_param9 test_param10 test_param11 "
            "test_param12".format(db_id).split())
    output_print_sim_after_add_sim, err = capsys.readouterr()
    print_sim.print_sim("--id {0} -v --columns new_test_param1 new_test_param2 "
            "new_test_param3 new_test_param4 new_test_param5 new_test_param6 "
            "new_test_param7 new_test_param8 new_test_param9 new_test_param10 "
            "results_dir time_started used_walltime --no_headers"
            .format(db_id).split())
    output_print_sim_after_run_sim, err = capsys.readouterr()
    del_sim_params = "--id {0}".format(db_id).split()
    del_sim_params.append("--no_checks")
    delete_sim.delete_sim(del_sim_params)
    with capsys.disabled():
        print("\nTest add_and_run...")
    __assert_output_print_sim_after_add_sim(output_print_sim_after_add_sim)
    __assert_output_python_program(output_program)
    __assert_output_print_sim_after_run_sim(output_print_sim_after_run_sim,
                                            True)


def test_list_sim_db_commands(capsys):
    list_sim_db_commands.list_sim_db_commands()
    output_list_sim_db_commands, err = capsys.readouterr()
    with capsys.disabled():
        print("\nTest list_sim_db_commands...")
    output_lines = output_list_sim_db_commands.split('\n')
    assert output_lines[2] == "add_and_run"
    assert output_lines[3] == "add_and_submit"
    assert output_lines[4] == "add_column"
    assert output_lines[5] == "add_comment"
    assert output_lines[6] == "add_range_sim"
    assert output_lines[7] == "add_sim"
    assert output_lines[8] == "cd_results"
    assert output_lines[9] == "combine_dbs"
    assert output_lines[10] == "delete_empty_columns"
    assert output_lines[11] == "delete_results_dir"
    assert output_lines[12] == "delete_sim"
    assert output_lines[13] == "extract_params"
    assert output_lines[14] == "list_print_configs"
    assert output_lines[15] == "list_sim_db_commands"
    assert output_lines[16] == "print_sim"
    assert output_lines[17] == "run_serial_sims"
    assert output_lines[18] == "run_sim"
    assert output_lines[19] == "submit_sim"
    assert output_lines[20] == "update_sim"


def test_add_column_and_delete_empty_columns(capsys):
    with capsys.disabled():
        print("\nTest add_column and delete_empty_columns...")
    add_column.add_column("--column new_column --type 'TEXT'".split())
    db = helpers.connect_sim_db()
    db_cursor = db.cursor()
    column_names, column_types = helpers.get_db_column_names_and_types(
            db_cursor)
    assert "new_column" in column_names
    delete_empty_columns.delete_empty_columns()
    column_names, column_types = helpers.get_db_column_names_and_types(
            db_cursor)
    assert "new_column" not in column_names


def test_extract_params(capsys):
    db_id = add_sim.add_sim([
            "--filename",
            "{0}/sim_params_python_program.txt".format(__get_test_dir())
    ])
    extract_params.extract_params("--id {0}".format(db_id).split())
    output_extract_params, err = capsys.readouterr()
    del_sim_params = "--id {0}".format(db_id).split()
    del_sim_params.append("--no_checks")
    delete_sim.delete_sim(del_sim_params)
    lines_extract_params = output_extract_params.split('\n')
    with capsys.disabled():
        print("\nTest extract_params...")
    assert "name (string): test_sim" == lines_extract_params[0]
    assert "test_param1 (int): 3" == lines_extract_params[6]
    assert "test_param2 (float): -5000000000.0" == lines_extract_params[8]
    assert "test_param3 (string): hei" == lines_extract_params[10]
    assert "test_param4 (bool): True" == lines_extract_params[12]
    assert "test_param5 (int array): [1, 2, 3]" == lines_extract_params[14]
    assert "test_param6 (float array): [1.5, 2.5, 3.5]" == lines_extract_params[
            16]
    assert "test_param7 (string array): [a, b, c]" == lines_extract_params[18]
    assert "test_param8 (bool array): [True, False, True]" == lines_extract_params[
            20]
    assert "test_param9 (int): 9" == lines_extract_params[22]
    assert "test_param10 (int): 11" == lines_extract_params[24]


def test_update_sim(capsys):
    db_id = add_sim.add_sim([
            "--filename",
            "{0}/sim_params_python_program.txt".format(__get_test_dir())
    ])
    update_sim.update_sim("--id {0} --columns test_param1 --values 100".format(
            db_id).split())
    print_sim.print_sim("--id {0} --columns test_param1 --no_headers".format(
            db_id).split())
    output_print_sim, err = capsys.readouterr()
    del_sim_params = "--id {0}".format(db_id).split()
    del_sim_params.append("--no_checks")
    delete_sim.delete_sim(del_sim_params)
    with capsys.disabled():
        print("\nTest update_sim...")
    assert output_print_sim.strip() == "100"


def test_add_comment(capsys):
    db_id = add_sim.add_sim([
            "--filename",
            "{0}/sim_params_python_program.txt".format(__get_test_dir())
    ])
    add_comment.add_comment([
            "--id", "{0}".format(db_id), "--comment", "This is a test comment."
    ])
    print_sim.print_sim(
            "--id {0} --columns comment --no_headers".format(db_id).split())
    output_print_sim, err = capsys.readouterr()
    del_sim_params = "--id {0}".format(db_id).split()
    del_sim_params.append("--no_checks")
    delete_sim.delete_sim(del_sim_params)
    with capsys.disabled():
        print("\nTest add_comment...")
    assert output_print_sim.strip() == "This is a test comment."


def test_cd_results(capsys):
    db_id = add_and_run.add_and_run([
            "--filename",
            "{0}/sim_params_python_program.txt".format(__get_test_dir())
    ])
    output_program, err_program = capsys.readouterr()
    results_dir = cd_results.cd_results("--id {0}".format(db_id).split())
    print_sim.print_sim("--id {0} -v --columns results_dir --no_headers".format(
            db_id).split())
    output_print_sim, err_print_sim = capsys.readouterr()
    with capsys.disabled():
        print("\nTest cd_results...")
    assert os.path.isdir(results_dir)
    del_sim_params = "--id {0}".format(db_id).split()
    del_sim_params.append("--no_checks")
    delete_sim.delete_sim(del_sim_params)
    assert not os.path.isdir(results_dir)


def test_submit_sim(capsys):
    settings_no_set, job_scheduler, n_cpus_per_node, memory_per_node = \
            __read_job_scheduler_settings()

    with capsys.disabled():
        print("\nTest submit_sim...")
        for no_set in settings_no_set:
            print("WARNING: In settings.txt '{0}' is NOT set, but must be to test "
                  "submit_sim.".format(no_set))

    if len(settings_no_set) == 0:
        db_id = add_sim.add_sim([
                "--filename",
                "{0}/sim_params_python_program.txt".format(__get_test_dir())
        ])
        job_script_name, job_id = submit_sim.submit_sim([
                "--id",
                str(db_id), "--do_not_submit_job_script", "--max_walltime",
                "03:34:00", "--n_nodes", "2"
        ])
        del_sim_params = "--id {0}".format(db_id).split()
        del_sim_params.append("--no_checks")
        delete_sim.delete_sim(del_sim_params)
        job_script_file = open(job_script_name, 'r')
        lines = job_script_file.readlines()
        job_script_file.close()
        os.remove(job_script_name)
        __assert_lines_job_script(lines, job_scheduler, n_cpus_per_node,
                                  memory_per_node)


def __read_job_scheduler_settings():
    settings = helpers.Settings()
    job_scheduler = settings.read('which_job_scheduler')
    n_cpus_per_node = settings.read('n_cpus_per_node')
    memory_per_node = settings.read('memory_per_node')

    settings_no_set = []
    if len(job_scheduler) == 0:
        settings_no_set.append("Which job_scheduler")
    if len(n_cpus_per_node) == 0:
        settings_no_set.append("Number of logical cpus per node")
    if len(memory_per_node) == 0:
        settings_no_set.append("Memory per node")

    return (settings_no_set, job_scheduler, n_cpus_per_node, memory_per_node)


def __assert_lines_job_script(lines, job_scheduler, n_cpus_per_node,
                              memory_per_node):
    if job_scheduler[0] == 'SLURM':
        assert lines[0] == '#!/bin/bash\n'
        assert lines[1] == '#SBATCH --job-name=test_sim\n'
        assert lines[2] == '#SBATCH --time=03:34:00\n'
        assert lines[3] == '#SBATCH --ntasks={0}\n'.format(
                int(n_cpus_per_node[0]) * 2)
        assert lines[4] == '#SBATCH --mem-per-cpu={0}M\n'.format(int( \
                float(memory_per_node[0]) / float(n_cpus_per_node[0]) * 1000))
    elif job_scheduler[0] == 'PBS':
        assert lines[0] == '#!/bin/bash\n'
        assert lines[1] == '#PBS -N test_sim\n'
        assert lines[2] == '#PBS -l walltime=03:34:00\n'
        assert lines[3] == '#PBS -l nodes=2:ppn={0}\n'.format(
                int(n_cpus_per_node[0]))
        assert lines[4] == '#PBS --mem={0}GB\n'.format(memory_per_node[0])


def test_add_and_submit(capsys):
    settings_no_set, job_scheduler, n_cpus_per_node, memory_per_node = \
            __read_job_scheduler_settings()

    with capsys.disabled():
        print("\nTest add_and_submit...")
        for no_set in settings_no_set:
            print("WARNING: In settings.txt '{0}' is NOT set, but must be to test "
                  "add_and_submit.".format(no_set))

    if len(settings_no_set) == 0:
        db_id, job_script_name, job_id = add_and_submit.add_and_submit([
                "--filename", "{0}/sim_params_python_program.txt".format(
                        __get_test_dir()), "--n_nodes", "2", "--max_walltime",
                "03:34:00", "--do_not_submit_job_script"
        ])
        del_sim_params = "--id {0}".format(db_id).split()
        del_sim_params.append("--no_checks")
        delete_sim.delete_sim(del_sim_params)
        job_script_file = open(job_script_name, 'r')
        lines = job_script_file.readlines()
        job_script_file.close()
        os.remove(job_script_name)
        __assert_lines_job_script(lines, job_scheduler, n_cpus_per_node,
                                  memory_per_node)


def test_combine_dbs(capsys):
    path_db_1 = __get_test_dir() + "/sim1_test_comb.db"
    path_db_2 = __get_test_dir() + "/sim2_test_comb.db"
    path_comb_db = __get_test_dir() + "/new_comb_sim.db"
    if os.path.exists(path_comb_db):
        os.remove(path_comb_db)
    combine_dbs.combine_dbs([path_db_1, path_db_2, path_comb_db])
    comb_sim_db = helpers.connect_sim_db(path_comb_db)
    comb_sim_db_cursor = comb_sim_db.cursor()
    db_1 = helpers.connect_sim_db(path_db_1)
    db_1_cursor = db_1.cursor()
    db_2 = helpers.connect_sim_db(path_db_2)
    db_2_cursor = db_2.cursor()

    column_names_1, column_types_1 = helpers.get_db_column_names_and_types(
            db_1_cursor)
    column_names_2, column_types_2 = helpers.get_db_column_names_and_types(
            db_2_cursor)
    column_names_comb, column_types_comb = helpers.get_db_column_names_and_types( \
            comb_sim_db_cursor)

    old_run_commands = []
    db_1_cursor.execute("SELECT run_command FROM runs WHERE id=1;")
    old_run_commands.append(db_1_cursor.fetchall()[0][0])
    db_1_cursor.execute("SELECT run_command FROM runs WHERE id=2;")
    old_run_commands.append(db_1_cursor.fetchall()[0][0])
    db_2_cursor.execute("SELECT run_command FROM runs WHERE id=1;")
    old_run_commands.append(db_2_cursor.fetchall()[0][0])
    db_2_cursor.execute("SELECT run_command FROM runs WHERE id=2;")
    old_run_commands.append(db_2_cursor.fetchall()[0][0])

    new_run_commands = []
    comb_sim_db_cursor.execute("SELECT run_command FROM runs WHERE id=1;")
    new_run_commands.append(comb_sim_db_cursor.fetchall()[0][0])
    comb_sim_db_cursor.execute("SELECT run_command FROM runs WHERE id=2;")
    new_run_commands.append(comb_sim_db_cursor.fetchall()[0][0])
    comb_sim_db_cursor.execute("SELECT run_command FROM runs WHERE id=3;")
    new_run_commands.append(comb_sim_db_cursor.fetchall()[0][0])
    comb_sim_db_cursor.execute("SELECT run_command FROM runs WHERE id=4;")
    new_run_commands.append(comb_sim_db_cursor.fetchall()[0][0])

    with capsys.disabled():
        print("\nTest combine_dbs...")

    comb_sim_db.commit()
    comb_sim_db_cursor.close()
    comb_sim_db.close()
    os.remove(path_comb_db)

    for column_name in column_names_1:
        assert column_name in column_names_comb
    for column_name in column_names_2:
        assert column_name in column_names_comb
    for (old_command, new_command) in zip(old_run_commands, new_run_commands):
        assert old_command == new_command

def test_add_range_sim(capsys):
    db_ids = add_range_sim.add_range_sim([
            "--filename",
            "{0}/sim_params_python_program.txt".format(__get_test_dir()),
            "--columns", "test_param1", "test_param2", 
            "--lin_steps", "0", "2",
            "--exp_steps", "3", "1",
            "--end_steps", "27", "-4999999999",
            "--n_steps", "0", "2",
    ])
    db_ids_string = ""
    for db_id in db_ids:
        db_ids_string = db_ids_string + " " + str(db_id)
    print_sim.print_sim("--id {0} -v --no_headers --columns test_param1 " \
           "test_param2".format(db_ids_string).split())
    output_print_sim, err = capsys.readouterr()
    del_sim_params = "--id {0}".format(db_id).split()
    del_sim_params.append("--no_check")
    delete_sim.delete_sim(del_sim_params)
    print_sim.print_sim("-n 1 --no_headers --columns id".split())
    output_after_delete, err = capsys.readouterr()
    with capsys.disabled():
        print("\nTest add_range_sim...") 
    test_param1_list, test_param2_list = output_print_sim.split('\n', 1)
    test_param1_list = test_param1_list.split()
    test_param2_list = test_param2_list.split()
    assert (test_param1_list[0] == "3" and test_param1_list[1] == "3" 
            and test_param1_list[2] == "3")
    assert (test_param1_list[3] == "9" and test_param1_list[4] == "9" 
            and test_param1_list[5] == "9")
    assert (test_param1_list[6] == "27" and test_param1_list[7] == "27" 
            and test_param1_list[8] == "27")
    param2_start = -5000000000.0
    assert (test_param2_list[0] == str(param2_start) 
            and test_param2_list[3] == str(param2_start) 
            and test_param2_list[6] == str(param2_start))
    assert (test_param2_list[1] == str(param2_start + 2) 
            and test_param2_list[4] == str(param2_start + 2) 
            and test_param2_list[7] == str(param2_start + 2))
    assert (test_param2_list[2] == str(param2_start + 4) 
            and test_param2_list[5] == str(param2_start + 4) 
            and test_param2_list[8] == str(param2_start + 4))

    # Test that the added simulation parameters are deleted
    assert (len(output_after_delete) == 0
            or output_after_delete != "{0}".format(db_id))

def test_run_serial_sims(capsys):
    id_1 = add_sim.add_sim(["--filename", 
        __get_test_dir() + "/sim_params_python_program.txt"])
    id_2 = add_sim.add_sim(["--filename", 
        __get_test_dir() + "/sim_params_c_program.txt"])
    id_3 = add_sim.add_sim(["--filename", 
        __get_test_dir() + "/sim_params_cpp_program.txt"])
    run_serial_sims.run_serial_sims(["--id", str(id_1), str(id_2), str(id_3)])
    output_serial_run, err = capsys.readouterr()
    print_sim.print_sim("--id {0} {1} {2} -v --no_headers --columns name "
            "test_param1 ".format(id_1, id_2, id_3).split())
    output_print_sim, err = capsys.readouterr()
    del_sim_params = "--id {0} {1} {2}".format(id_1, id_2, id_3).split()
    del_sim_params.append("--no_check")
    delete_sim.delete_sim(del_sim_params)
    print_sim.print_sim("-n 1 --no_headers --columns id".split())
    output_after_delete, err = capsys.readouterr()
    with capsys.disabled():
        print("\nTest run_serial_sims...")
    printed_params = output_print_sim.split('\n')[0::2]
    printed_names = printed_params[0].split()
    printed_params_1 = printed_params[1].split()
    assert printed_names[0] == printed_names[1] == printed_names[2]
    assert printed_params_1[0] == printed_params_1[1] == printed_params_1[2]

    # Test that the added simulation parameters are deleted
    assert (len(output_after_delete) == 0
            or output_after_delete != "{0}".format(id_3))

def test_delete_results_dir(capsys):
    with capsys.disabled():
        print("\nTest delete_results_dir...")
    for entry in os.listdir(__get_test_dir() + '/results'):
        print(__get_test_dir() + '/results/' + entry)
        assert not os.path.isdir(__get_test_dir() + '/results/' + entry)
