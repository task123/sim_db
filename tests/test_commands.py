# -*- coding: utf-8 -*-
"""Test commands of 'sim_db' command line tool."""
# Copyright (C) 2017, 2018 Håkon Austlid Taskén <hakon.tasken@gmail.com>
# Licenced under the MIT License.

import add_package_root_to_path
import common_test_helpers
from sim_db.src_command_line_tool.command_line_tool import command_line_tool
import sim_db.src_command_line_tool.commands.helpers as helpers
import os
import subprocess
import shutil


def setup_module(module):
    """Clean up 'results/' directory."""
    for entry in os.listdir(common_test_helpers.get_test_dir() + '/results'):
        if os.path.isdir(common_test_helpers.get_test_dir() + '/results/' +
                         entry):
            shutil.rmtree(common_test_helpers.get_test_dir() + '/results/' +
                          entry)
    if os.path.isdir(common_test_helpers.get_test_dir() + '/.sim_db'):
        shutil.rmtree(common_test_helpers.get_test_dir() + '/.sim_db')


def test_init(capsys):
    common_test_helpers.skip_if_outside_sim_db()
    command_line_tool("sim_db", [
            "init", "--path", "{0}".format(common_test_helpers.get_test_dir())
    ])
    with capsys.disabled():
        print("\nTest init...")

    assert os.path.isdir(common_test_helpers.get_test_dir() + '/.sim_db')
    assert os.path.isfile(common_test_helpers.get_test_dir() +
                          '/.sim_db/settings.txt')
    shutil.rmtree(common_test_helpers.get_test_dir() + '/.sim_db')


def test_add_sim_print_sim_and_delete_sim(capsys):
    common_test_helpers.skip_if_outside_sim_db()
    db_id = command_line_tool(
            "sim_db", [
                    "add_sim", "--filename",
                    "{0}/sim_params_python_program.txt".format(
                            common_test_helpers.get_test_dir())
            ],
            print_ids_added=False)
    command_line_tool(
            "sim_db",
            "print --id {0} -v --no_headers --columns name test_param1 "
            "test_param2 test_param3 test_param4 test_param5 test_param6 "
            "test_param7 test_param8 test_param9 test_param10 test_param11 "
            "test_param12".format(db_id).split())
    output_print_sim, err = capsys.readouterr()
    command_line_tool("sim_db",
                      ["delete_sim", "--id",
                       str(db_id), "--no_checks"])
    command_line_tool("sim_db", "print -n 1 --no_headers --columns id".split())
    output_after_delete, err = capsys.readouterr()
    with capsys.disabled():
        print("\nTest add_sim, print_sim and delete_sim...")

    __assert_output_print_sim_after_add_sim(output_print_sim)

    # Test that the added simulation parameters are deleted
    assert (len(output_after_delete) == 0
            or output_after_delete.splitlines()[-1].strip() !=
            "{0}".format(db_id))


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


def test_add_and_run(capsys):
    common_test_helpers.skip_if_outside_sim_db()
    db_id = command_line_tool(
            "sim_db", [
                    "add_and_run", "--filename",
                    "{0}/sim_params_python_program.txt".format(
                            common_test_helpers.get_test_dir())
            ],
            print_ids_added=False)
    assert db_id != None
    output_program, err = capsys.readouterr()
    command_line_tool(
            "sim_db",
            "print_sim --id {0} -v --no_headers --columns name test_param1 "
            "test_param2 test_param3 test_param4 test_param5 test_param6 "
            "test_param7 test_param8 test_param9 test_param10 test_param11 "
            "test_param12".format(db_id).split())
    output_print_sim_after_add_sim, err = capsys.readouterr()
    command_line_tool(
            "sim_db",
            "print_sim --id {0} -v --columns new_test_param1 new_test_param2 "
            "new_test_param3 new_test_param4 new_test_param5 new_test_param6 "
            "new_test_param7 new_test_param8 new_test_param9 new_test_param10 "
            "results_dir time_started used_walltime --no_headers"
            .format(db_id).split())
    output_print_sim_after_run_sim, err = capsys.readouterr()
    command_line_tool("sim_db",
                      ["delete_sim", "--id",
                       str(db_id), "--no_checks"])
    with capsys.disabled():
        print("\nTest add_and_run...")
    __assert_output_print_sim_after_add_sim(output_print_sim_after_add_sim)
    common_test_helpers.assert_output_python_program(output_program, db_id)
    common_test_helpers.assert_output_print_sim_after_run_sim(
            output_print_sim_after_run_sim, True)


def test_list_commands(capsys):
    common_test_helpers.skip_if_outside_sim_db()
    command_line_tool("sim_db", ["list_commands"])
    output_list_commands, err = capsys.readouterr()
    with capsys.disabled():
        print("\nTest list_commands...")
    output_lines = output_list_commands.split('\n')
    assert output_lines[2] == "add_and_run"
    assert output_lines[3] == "add_and_submit"
    assert output_lines[4] == "add_column"
    assert output_lines[5] == "add_comment"
    assert output_lines[6] == "add_range / add_range_sim"
    assert output_lines[7] == "add / add_sim"
    assert output_lines[8] == "cd_res / cd_results"
    assert output_lines[9] == "combine_dbs"
    assert output_lines[10] == "delete_empty_columns"
    assert output_lines[11] == "delete_results_dir"
    assert output_lines[12] == "delete / delete_sim"
    assert output_lines[13] == "duplicate_and_run"
    assert output_lines[14] == "duplicate / duplicate_sim"
    assert output_lines[15] == "extract_params"
    assert output_lines[16] == "get"
    assert output_lines[17] == "init"
    assert output_lines[18] == "list_commands"
    assert output_lines[19] == "list_print_configs"
    assert output_lines[20] == "print / print_sim"
    assert output_lines[21] == "run_serial / run_serial_sims"
    assert output_lines[22] == "run / run_sim"
    assert output_lines[23] == "settings"
    assert output_lines[24] == "submit / submit_sim"
    assert output_lines[25] == "update / update_sim"


def test_add_column_and_delete_empty_columns(capsys):
    common_test_helpers.skip_if_outside_sim_db()
    with capsys.disabled():
        print("\nTest add_column and delete_empty_columns...")
    command_line_tool("sim_db",
                      "add_column --column new_column --type 'TEXT'".split())
    db = helpers.connect_sim_db()
    db_cursor = db.cursor()
    column_names, column_types = helpers.get_db_column_names_and_types(
            db_cursor)
    assert "new_column" in column_names
    command_line_tool("sim_db", ["delete_empty_columns"])
    column_names, column_types = helpers.get_db_column_names_and_types(
            db_cursor)
    assert "new_column" not in column_names


def test_extract_params(capsys):
    common_test_helpers.skip_if_outside_sim_db()
    db_id = command_line_tool(
            "sim_db", [
                    "add_sim", "--filename",
                    "{0}/sim_params_python_program.txt".format(
                            common_test_helpers.get_test_dir())
            ],
            print_ids_added=False)
    command_line_tool("sim_db",
                      "extract_params --id {0}".format(db_id).split())
    output_extract_params, err = capsys.readouterr()
    command_line_tool("sim_db",
                      ["delete_sim", "--id",
                       str(db_id), "--no_checks"])
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
    common_test_helpers.skip_if_outside_sim_db()
    db_id = command_line_tool(
            "sim_db", [
                    "add_sim", "--filename",
                    "{0}/sim_params_python_program.txt".format(
                            common_test_helpers.get_test_dir())
            ],
            print_ids_added=False)
    command_line_tool(
            "sim_db",
            "update_sim --id {0} --columns test_param1 --values 100".format(
                    db_id).split())
    command_line_tool(
            "sim_db",
            "print_sim --id {0} --columns test_param1 --no_headers".format(
                    db_id).split())
    output_print_sim, err = capsys.readouterr()
    command_line_tool("sim_db",
                      ["delete_sim", "--id",
                       str(db_id), "--no_checks"])
    with capsys.disabled():
        print("\nTest update_sim...")
    assert output_print_sim.strip() == "100"


def test_add_comment(capsys):
    common_test_helpers.skip_if_outside_sim_db()
    db_id = command_line_tool(
            "sim_db", [
                    "add_sim", "--filename",
                    "{0}/sim_params_python_program.txt".format(
                            common_test_helpers.get_test_dir())
            ],
            print_ids_added=False)
    command_line_tool("sim_db", [
            "add_comment", "--id", "{0}".format(db_id), "--comment",
            "This is a test comment."
    ])
    command_line_tool(
            "sim_db",
            "print_sim --id {0} --columns comment --no_headers".format(
                    db_id).split())
    output_print_sim, err = capsys.readouterr()
    command_line_tool("sim_db",
                      ["delete_sim", "--id",
                       str(db_id), "--no_checks"])
    with capsys.disabled():
        print("\nTest add_comment...")
    assert output_print_sim.strip() == "This is a test comment."


def test_get_and_cd_results(capsys):
    common_test_helpers.skip_if_outside_sim_db()
    db_id = command_line_tool("sim_db", [
            "add_and_run", "--filename",
            "{0}/sim_params_python_program.txt".format(
                    common_test_helpers.get_test_dir())
    ])
    output_program, err_program = capsys.readouterr()
    results_dir = command_line_tool(
            "sim_db", "get results_dir --id {0}".format(db_id).split())
    command_line_tool(
            "sim_db",
            "print_sim --id {0} -v --columns results_dir --no_headers".format(
                    db_id).split())
    output_print_sim, err_print_sim = capsys.readouterr()
    with capsys.disabled():
        print("\nTest get and cd_results...")
    assert os.path.isdir(results_dir)
    command_line_tool("sim_db",
                      ["delete_sim", "--id",
                       str(db_id), "--no_checks"])
    assert not os.path.isdir(results_dir)


def test_submit_sim(capsys):
    common_test_helpers.skip_if_outside_sim_db()
    settings_no_set, job_scheduler, n_cpus_per_node, memory_per_node = \
            __read_job_scheduler_settings()

    with capsys.disabled():
        print("\nTest submit_sim...")
        for no_set in settings_no_set:
            print("WARNING: In settings.txt '{0}' is NOT set, but must be to test "
                  "submit_sim.".format(no_set))

    if len(settings_no_set) == 0:
        db_id = command_line_tool(
                "sim_db", [
                        "add_sim", "--filename",
                        "{0}/sim_params_python_program.txt".format(
                                common_test_helpers.get_test_dir())
                ],
                print_ids_added=False)
        job_script_name, job_id = command_line_tool("sim_db", [
                "submit_sim", "--id",
                str(db_id), "--do_not_submit_job_script", "--max_walltime",
                "03:34:00", "--n_nodes", "2"
        ])
        command_line_tool("sim_db",
                          ["delete_sim", "--id",
                           str(db_id), "--no_checks"])
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
    common_test_helpers.skip_if_outside_sim_db()
    settings_no_set, job_scheduler, n_cpus_per_node, memory_per_node = \
            __read_job_scheduler_settings()

    with capsys.disabled():
        print("\nTest add_and_submit...")
        for no_set in settings_no_set:
            print("WARNING: In settings.txt '{0}' is NOT set, but must be to test "
                  "add_and_submit.".format(no_set))

    if len(settings_no_set) == 0:
        db_id, job_script_name, job_id = command_line_tool(
                "sim_db", [
                        "add_and_submit", "--filename",
                        "{0}/sim_params_python_program.txt".format(
                                common_test_helpers.get_test_dir()),
                        "--n_nodes", "2", "--max_walltime", "03:34:00",
                        "--do_not_submit_job_script"
                ],
                print_ids_added=False)
        command_line_tool("sim_db",
                          ["delete_sim", "--id",
                           str(db_id), "--no_checks"])
        job_script_file = open(job_script_name, 'r')
        lines = job_script_file.readlines()
        job_script_file.close()
        os.remove(job_script_name)
        __assert_lines_job_script(lines, job_scheduler, n_cpus_per_node,
                                  memory_per_node)


def test_combine_dbs(capsys):
    common_test_helpers.skip_if_outside_sim_db()
    path_db_1 = common_test_helpers.get_test_dir() + "/sim1_test_comb.db"
    path_db_2 = common_test_helpers.get_test_dir() + "/sim2_test_comb.db"
    path_comb_db = common_test_helpers.get_test_dir() + "/new_comb_sim.db"
    if os.path.exists(path_comb_db):
        os.remove(path_comb_db)
    command_line_tool("sim_db",
                      ["combine_dbs", path_db_1, path_db_2, path_comb_db])
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
    common_test_helpers.skip_if_outside_sim_db()
    db_ids = command_line_tool(
            "sim_db",
            "add_range_sim --filename".split() + [
                    "{0}/sim_params_python_program.txt".format(
                            common_test_helpers.get_test_dir())
            ] +
            "--columns test_param1 test_param2 --lin_steps 0 2 --exp_steps "
            "3 1 --end_steps 27 -4999999999 --n_steps 0 2".split(),
            print_ids_added=False)
    db_ids_string = ""
    for db_id in db_ids:
        db_ids_string = db_ids_string + " " + str(db_id)
    command_line_tool(
            "sim_db", "print_sim --id {0} -v --no_headers --columns "
            "test_param1 test_param2".format(db_ids_string).split())
    output_print_sim, err = capsys.readouterr()
    command_line_tool("sim_db",
                      ["delete_sim", "--id",
                       str(db_id), "--no_checks"])
    command_line_tool("sim_db",
                      "print_sim -n 1 --no_headers --columns id".split())
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
    common_test_helpers.skip_if_outside_sim_db()
    id_1 = command_line_tool(
            "sim_db", [
                    "add_sim", "--filename",
                    common_test_helpers.get_test_dir() +
                    "/sim_params_python_program.txt"
            ],
            print_ids_added=False)
    id_2 = command_line_tool(
            "sim_db", [
                    "add_sim", "--filename",
                    common_test_helpers.get_test_dir() +
                    "/sim_params_c_program.txt"
            ],
            print_ids_added=False)
    id_3 = command_line_tool(
            "sim_db", [
                    "add_sim", "--filename",
                    common_test_helpers.get_test_dir() +
                    "/sim_params_cpp_program.txt"
            ],
            print_ids_added=False)
    command_line_tool(
            "sim_db",
            ["run_serial_sims", "--id",
             str(id_1),
             str(id_2),
             str(id_3)])
    output_serial_run, err = capsys.readouterr()
    command_line_tool(
            "sim_db",
            "print_sim --id {0} {1} {2} -v --no_headers --columns name "
            "test_param1 ".format(id_1, id_2, id_3).split())
    output_print_sim, err = capsys.readouterr()
    command_line_tool("sim_db", [
            "delete_sim", "--id",
            str(id_1),
            str(id_2),
            str(id_3), "--no_checks"
    ])
    command_line_tool("sim_db",
                      "print_sim -n 1 --no_headers --columns id".split())
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


def test_duplicate_sim(capsys):
    common_test_helpers.skip_if_outside_sim_db()
    db_id = command_line_tool(
            "sim_db", [
                    "add_sim", "--filename",
                    common_test_helpers.get_test_dir() +
                    "/sim_params_python_program.txt"
            ],
            print_ids_added=False)
    command_line_tool("sim_db", [
            "update_sim", "--id",
            str(db_id), "-c", "status", "-v", "finished"
    ])
    db_id_duplicated = command_line_tool(
            "sim_db",
            ["duplicate_sim", "--id", str(db_id)],
            print_ids_added=False)
    command_line_tool("sim_db",
                      "print_sim -i {0} --no_headers -v".format(db_id).split())
    output_original_sim, err = capsys.readouterr()
    command_line_tool(
            "sim_db", "print_sim -i {0} --no_headers -v".format(
                    db_id_duplicated).split())
    output_duplicated_sim, err = capsys.readouterr()
    command_line_tool("sim_db",
                      ["delete_sim", "--id",
                       str(db_id), "--no_checks"])
    command_line_tool(
            "sim_db",
            ["delete_sim", "--id",
             str(db_id_duplicated), "--no_checks"])
    with capsys.disabled():
        print("\nTest duplicate_sim...")
    assert (output_original_sim.split('\n')[0].strip() !=
            output_duplicated_sim.split('\n')[0].strip())
    assert output_duplicated_sim.split('\n')[2].strip() == 'new'
    assert (output_original_sim.split('\n',
                                      3)[3] == output_duplicated_sim.split(
                                              '\n', 3)[3])


def test_duplicate_and_run(capsys):
    common_test_helpers.skip_if_outside_sim_db()
    db_id = command_line_tool(
            "sim_db", [
                    "add_sim", "--filename",
                    "{0}/sim_params_python_program.txt".format(
                            common_test_helpers.get_test_dir())
            ],
            print_ids_added=False)
    new_id = command_line_tool(
            "sim_db", ["duplicate_and_run", "--id",
                       str(db_id)],
            print_ids_added=False)
    output_program, err = capsys.readouterr()
    command_line_tool(
            "sim_db",
            "print_sim --id {0} -v --no_headers --columns name test_param1 "
            "test_param2 test_param3 test_param4 test_param5 test_param6 "
            "test_param7 test_param8 test_param9 test_param10 test_param11 "
            "test_param12".format(new_id).split())
    output_print_sim_after_duplicate_sim, err = capsys.readouterr()
    command_line_tool(
            "sim_db",
            "print_sim --id {0} -v --columns new_test_param1 new_test_param2 "
            "new_test_param3 new_test_param4 new_test_param5 new_test_param6 "
            "new_test_param7 new_test_param8 new_test_param9 new_test_param10 "
            "results_dir time_started used_walltime --no_headers"
            .format(new_id).split())
    output_print_sim_after_run_sim, err = capsys.readouterr()
    command_line_tool("sim_db",
                      ["delete_sim", "--id",
                       str(db_id), "--no_checks"])
    command_line_tool("sim_db",
                      ["delete_sim", "--id",
                       str(new_id), "--no_checks"])
    with capsys.disabled():
        print("\nTest duplicate_and_run...")
    __assert_output_print_sim_after_add_sim(
            output_print_sim_after_duplicate_sim)
    common_test_helpers.assert_output_python_program(output_program, new_id)
    common_test_helpers.assert_output_print_sim_after_run_sim(
            output_print_sim_after_run_sim, True)


def test_settings(capsys):
    common_test_helpers.skip_if_outside_sim_db()
    command_line_tool("sim_db", [
            "init", "--path", "{0}".format(common_test_helpers.get_test_dir())
    ])
    output_program, err = capsys.readouterr()
    cwd = os.getcwd()
    os.chdir(common_test_helpers.get_test_dir())
    command_line_tool("sim_db",
                      ["settings", "print", "--setting", "parameter_files"])
    output_setting_print_original, err = capsys.readouterr()
    command_line_tool("sim_db", [
            "settings", "add", "--setting", "parameter_files", "--line",
            "test_settings.txt"
    ])
    command_line_tool("sim_db",
                      ["settings", "print", "--setting", "parameter_files"])
    output_setting_print_after_add, err = capsys.readouterr()
    command_line_tool("sim_db", [
            "settings", "remove", "--setting", "parameter_files", "--line",
            "test_settings.txt"
    ])
    command_line_tool("sim_db",
                      ["settings", "print", "--setting", "parameter_files"])
    output_setting_print_after_remove, err = capsys.readouterr()

    with capsys.disabled():
        print("\nTest settings...")

    os.chdir(cwd)
    shutil.rmtree(common_test_helpers.get_test_dir() + '/.sim_db')

    assert output_setting_print_original.strip() == 'sim_params.txt'
    assert output_setting_print_after_add.split('\n')[
            0].strip() == 'sim_params.txt'
    assert output_setting_print_after_add.split('\n')[
            1].strip() == 'test_settings.txt'
    assert output_setting_print_after_remove.strip() == 'sim_params.txt'


def test_delete_results_dir(capsys):
    common_test_helpers.skip_if_outside_sim_db()
    with capsys.disabled():
        print("\nTest delete_results_dir...")
    for entry in os.listdir(common_test_helpers.get_test_dir() + '/results'):
        print(common_test_helpers.get_test_dir() + '/results/' + entry)
        assert not os.path.isdir(common_test_helpers.get_test_dir() +
                                 '/results/' + entry)
