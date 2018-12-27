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
    space_escape = " "
    if os.sep == "\\":
        space_escape = "\ "
    path_tests_dir = common_test_helpers.get_test_dir().replace(" ", 
                                                               space_escape)
    path_sim_db_root = os.path.join(path_tests_dir, os.pardir)
    path_build = os.path.join(path_tests_dir, "build")
    path_c_mtap = os.path.join(os.path.join(path_tests_dir, "build"), "c_mtap")
    subprocess.call(["cmake", "-H{0}".format(path_sim_db_root), 
                     "-B{0}".format(path_build)])
    subprocess.call(["cmake", "--build", path_build, "--target", "c_mtap"])
    output = subprocess.check_output([path_c_mtap], universal_newlines=True)
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
