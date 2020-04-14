# -*- coding: utf-8 -*-
"""Helper functions for used by both test_commands and test_function."""
# Copyright (C) 2018-2019 Håkon Austlid Taskén <hakon.tasken@gmail.com>
# Licenced under the MIT License.

import os.path
import pytest


def skip_if_outside_sim_db():
    if is_outside_sim_db():
        pytest.skip("Run from outside of sim_db/.")


def is_outside_sim_db():
    cwd = os.getcwd()
    if os.path.basename(cwd) == "sim_db":
        return False
    elif (os.path.basename(cwd) == "tests"
          and os.path.basename(os.path.dirname(cwd)) == "sim_db"):
        return False
    else:
        return True


def get_test_dir():
    return os.path.dirname(os.path.abspath(__file__))


def remove_cmake_output(output):
    new_output = ""
    for line in output.split('\n'):
        if (not line[0:3] == '-- '
            and not line[0:21] == 'Scanning dependencies'
            and not line[7:15] == 'Building'
            and not line[7:14] == 'Linking'
            and not line[7:19] == 'Built target'):
            new_output = new_output + line + "\n"
    return new_output


def assert_output_python_program(output_program, db_id):
    printed_params = output_program.split('\n')
    assert printed_params[0] == '0.2.8'
    assert printed_params[1] == "3"
    assert printed_params[2] == printed_params[1]
    assert printed_params[3] == "-5000000000.0"
    assert printed_params[4] == printed_params[3]
    assert printed_params[5] == "hei"
    assert printed_params[6] == printed_params[5]
    assert printed_params[7] == "True"
    assert printed_params[8] == printed_params[7]
    assert printed_params[9] == "[1, 2, 3]"
    assert printed_params[10] == printed_params[9]
    assert printed_params[11] == "[1.5, 2.5, 3.5]"
    assert printed_params[12] == printed_params[11]
    assert printed_params[13] == "['a', 'b', 'c']"
    assert printed_params[14] == printed_params[13]
    assert printed_params[15] == "[True, False, True]"
    assert printed_params[16] == printed_params[15]
    assert printed_params[17] == "9"
    assert printed_params[18] == printed_params[17]
    assert printed_params[19] == "11"
    assert printed_params[20] == printed_params[19]
    assert printed_params[21] == "None"
    assert printed_params[22] == "None"
    assert printed_params[23] == "[1, 2, 3]"
    assert printed_params[24] == "False"
    assert printed_params[25] == "True"
    assert printed_params[26] == "True"
    assert printed_params[27] == "False"
    assert printed_params[28] == "raised ColumnError"
    assert printed_params[29] == str(db_id + 1)
    assert printed_params[30] == "7"


def assert_output_print_sim_after_run_sim(output_print_sim, store_metadata):
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
