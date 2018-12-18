# -*- coding: utf-8 -*-
"""Test commands of 'sim_db' command line tool."""
# Copyright (C) 2017, 2018 Håkon Austlid Taskén <hakon.tasken@gmail.com>
# Licenced under the MIT License.

import add_package_root_to_path
import common_test_helpers
import subprocess
import os.path

def test_c_multithreading(capsys):
    common_test_helpers.skip_if_outside_sim_db()
    with capsys.disabled():
        print("\nTest C multithreading and processing...")
    output = subprocess.check_output(
            ["make", "-C", common_test_helpers.get_test_dir(), "c_mtap_run"],
            universal_newlines=True)
    last_line = output.splitlines()[-1]
    assert last_line.strip() == "finished"

def test_python_multithreading(capsys):
    common_test_helpers.skip_if_outside_sim_db()
    with capsys.disabled():
        print("\nTest python multithreading and processing...")
    path_script = os.path.join(common_test_helpers.get_test_dir(), 
                                             "multithreading_and_processing.py")
    if os.sep == '/':
        space_escape = '\ '
    else:
        space_escape = ' '
    output = subprocess.check_output(
            ["python", path_script], 
            universal_newlines=True)
    last_line = output.splitlines()[-1]
    assert last_line.strip() == "finished"
