# -*- coding: utf-8 -*-
"""Helper functions for used by both test_commands and test_function."""
# Copyright (C) 2018 Håkon Austlid Taskén <hakon.tasken@gmail.com>
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


def assert_output_python_program(output_program, db_id):
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
    assert printed_params[22] == "True"
    assert printed_params[23] == "False"
    assert printed_params[24] == "raised ColumnError"
    assert printed_params[25] == str(db_id + 1)
    assert printed_params[26] == "7"


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
