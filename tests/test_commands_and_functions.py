import __init__
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
import os
import time
import subprocess

def test_add_sim_print_sim_and_delete_sim(capsys):
    db_id = add_sim.add_sim("--filename sim_params_python_program.txt".split())
    print_sim.print_sim("--id {} -v --no_headers --columns name param1 param2 " \
            "param3 param4 param5 param6 param7 param8 param9 param10" \
            .format(db_id).split())
    output_print_sim, err = capsys.readouterr()
    delete_sim.delete_sim("--id {}".format(db_id).split())
    print_sim.print_sim("-n 1 --no_headers --columns id".split())
    output_after_delete, err = capsys.readouterr()
    with capsys.disabled():
        print("\nTest add_sim, print_sim and delete_sim...")
    __assert_output_print_sim_after_add_sim(output_print_sim)

    # Test that the added simulation parameters are deleted
    assert len(output_after_delete) == 0 \
            or output_after_delete != "{}".format(db_id)

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
    assert printed_params[9] == "None"
    assert printed_params[10] == "None"

def test_run_sim_and_sim_db_methods(capsys):
    db_id = add_sim.add_sim("--filename sim_params_python_program.txt".split())
    run_sim.run_sim("--id {}".format(db_id).split())
    time.sleep(0.2) # Wait for program.py to finish
    output_program, err = capsys.readouterr()
    print_sim.print_sim("--id {} -v --columns new_param1 new_param2 new_param3 " \
            "new_param4 new_param5 new_param6 new_param7 new_param8 result_dir " \
            "time_started used_walltime --no_headers".format(db_id).split())
    output_print_sim, err = capsys.readouterr()
    delete_sim.delete_sim("--id {}".format(db_id).split())
    with capsys.disabled():
        print("\nTest run_sim and python methods...")
    res_dir = output_print_sim.split('\n')[16].strip()
    os.remove(res_dir + "/results.txt")
    os.rmdir(res_dir)
    __assert_output_python_program(output_program)
    __assert_output_print_sim_after_run_sim(output_print_sim)

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
    assert printed_params[16] == "None"
    assert printed_params[17] == "None"

def __assert_output_print_sim_after_run_sim(output_print_sim):
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
    assert printed_params[8] != None
    assert printed_params[9] != None
    assert printed_params[10] != None

def test_add_and_run(capsys):
    db_id = add_and_run.add_and_run("--filename sim_params_python_program.txt".split())
    time.sleep(0.2) # Wait for program.py to finish
    output_program, err = capsys.readouterr()
    print_sim.print_sim("--id {} -v --no_headers --columns name param1 param2 " \
            "param3 param4 param5 param6 param7 param8 param9 param10" \
            .format(db_id).split())
    output_print_sim_after_add_sim, err = capsys.readouterr()
    print_sim.print_sim("--id {} -v --columns new_param1 new_param2 new_param3 " \
            "new_param4 new_param5 new_param6 new_param7 new_param8 result_dir " \
            "time_started used_walltime --no_headers".format(db_id).split())
    output_print_sim_after_run_sim, err = capsys.readouterr()
    delete_sim.delete_sim("--id {}".format(db_id).split())
    with capsys.disabled():
        print("\nTest add_and_run...")
    res_dir = output_print_sim_after_run_sim.split('\n')[16].strip()
    os.remove(res_dir + "/results.txt")
    os.rmdir(res_dir)
    __assert_output_print_sim_after_add_sim(output_print_sim_after_add_sim)
    __assert_output_python_program(output_program)
    __assert_output_print_sim_after_run_sim(output_print_sim_after_run_sim)

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
    assert output_lines[6] == "add_sim"
    assert output_lines[7] == "cd_results"
    assert output_lines[8] == "combine_dbs"
    assert output_lines[9] == "delete_empty_columns"
    assert output_lines[10] == "delete_sim"
    assert output_lines[11] == "extract_params"
    assert output_lines[12] == "list_sim_db_commands"
    assert output_lines[13] == "print_sim"
    assert output_lines[14] == "run_sim"
    assert output_lines[15] == "submit_sim"
    assert output_lines[16] == "update_sim"

def test_add_column_and_delete_empty_columns(capsys):
    with capsys.disabled():
        print("\nTest add_column and delete_empty_columns...")
    add_column.add_column("--column new_column --type 'TEXT'".split())
    db = helpers.connect_sim_db()
    db_cursor = db.cursor()
    column_names, column_types = helpers.get_db_column_names_and_types(db_cursor)
    assert "new_column" in column_names
    delete_empty_columns.delete_empty_columns()
    column_names, column_types = helpers.get_db_column_names_and_types(db_cursor)
    assert "new_column" not in column_names
    
def test_extract_params(capsys):
    db_id = add_sim.add_sim("--filename sim_params_python_program.txt".split())
    extract_params.extract_params("--id {}".format(db_id).split())
    output_extract_params, err = capsys.readouterr()
    delete_sim.delete_sim("--id {}".format(db_id).split())
    lines_extract_params = output_extract_params.split('\n')
    with capsys.disabled():
        print("\nTest extract_params...")
    assert "name (string): test_sim" == lines_extract_params[0]
    assert "param1 (int): 3" == lines_extract_params[6]
    assert "param2 (float): -5000000000.0" == lines_extract_params[8]
    assert "param3 (string): hei" == lines_extract_params[10]
    assert "param4 (bool): True" == lines_extract_params[12]
    assert "param5 (int array): [1, 2, 3]" == lines_extract_params[14]
    assert "param6 (float array): [1.5, 2.5, 3.5]" == lines_extract_params[16]
    assert "param7 (string array): [a, b, c]" == lines_extract_params[18]
    assert "param8 (bool array): [True, False, True]" == lines_extract_params[20]

def test_update_sim(capsys):
    db_id = add_sim.add_sim("--filename sim_params_python_program.txt".split())
    update_sim.update_sim("--id {} --columns param1 --values 100".format(db_id).split())
    print_sim.print_sim("--id {} --columns param1 --no_headers".format(db_id).split())
    output_print_sim, err = capsys.readouterr()
    delete_sim.delete_sim("--id {}".format(db_id).split())
    with capsys.disabled():
        print("\nTest update_sim...")
    assert output_print_sim.strip() == "100"

def test_add_comment(capsys):
    db_id = add_sim.add_sim("--filename sim_params_python_program.txt".split())
    add_comment.add_comment(["--id", "{}".format(db_id), "--comment",  \
            "This is a test comment."])
    print_sim.print_sim("--id {} --columns comment --no_headers".format(db_id).split())
    output_print_sim, err = capsys.readouterr()
    delete_sim.delete_sim("--id {}".format(db_id).split())
    with capsys.disabled():
        print("\nTest add_comment...")
    assert output_print_sim.strip() == "This is a test comment."

def test_c_functions(capsys):
    db_id = add_sim.add_sim("--filename sim_params_c_program.txt".split())
    run_sim.run_sim("--id {}".format(db_id).split())
    time.sleep(0.2) # Wait for c_program to finish
    output_program, err = capsys.readouterr()
    print_sim.print_sim("--id {} -v --columns new_param1 new_param2 new_param3 " \
            "new_param4 new_param5 new_param6 new_param7 new_param8 result_dir " \
            "time_started used_walltime --no_headers".format(db_id).split())
    output_print_sim, err = capsys.readouterr()
    delete_sim.delete_sim("--id {}".format(db_id).split())
    with capsys.disabled():
        print("\nTest C functions...")
    res_dir = output_print_sim.split('\n')[16].strip()
    os.remove(res_dir + "/results.txt")
    os.rmdir(res_dir)
    __assert_output_c_program(output_program)
    __assert_output_print_sim_after_run_sim(output_print_sim)

def test_cpp_functions(capsys):
    db_id = add_sim.add_sim("--filename sim_params_cpp_program.txt".split())
    run_sim.run_sim("--id {}".format(db_id).split())
    time.sleep(0.2) # Wait for cpp_program to finish
    output_program, err = capsys.readouterr()
    print_sim.print_sim("--id {} -v --columns new_param1 new_param2 new_param3 " \
            "new_param4 new_param5 new_param6 new_param7 new_param8 result_dir " \
            "time_started used_walltime --no_headers".format(db_id).split())
    output_print_sim, err = capsys.readouterr()
    delete_sim.delete_sim("--id {}".format(db_id).split())
    with capsys.disabled():
        print("\nTest C++ methods...")
    res_dir = output_print_sim.split('\n')[16].strip()
    os.remove(res_dir + "/results.txt")
    os.rmdir(res_dir)
    __assert_output_c_program(output_program)
    __assert_output_print_sim_after_run_sim(output_print_sim)

def __assert_output_c_program(output_popen):
    printed_lines = output_popen.split('\n')
    assert printed_lines[1] == "3"
    assert printed_lines[2] == printed_lines[1]
    assert abs(float(printed_lines[3]) - -5000000000.0) < 0.001
    assert printed_lines[4] == printed_lines[3]
    assert printed_lines[5] == "hei"
    assert printed_lines[6] == printed_lines[5]
    assert printed_lines[7] == "1"
    assert printed_lines[8] == printed_lines[7]
    assert printed_lines[9:12] == ['1', '2', '3']
    assert printed_lines[9:12] == printed_lines[12:15]
    assert abs(float(printed_lines[15]) - 1.5) < 0.001
    assert abs(float(printed_lines[16]) - 2.5) < 0.001
    assert abs(float(printed_lines[17]) - 3.5) < 0.001
    assert printed_lines[15:18] == printed_lines[18:21]
    assert printed_lines[21:24] == ['a', 'b', 'c']
    assert printed_lines[21:24] == printed_lines[24:27]
    assert printed_lines[27:30] == ['1', '0', '1']
    assert printed_lines[27:30] == printed_lines[30:33]
