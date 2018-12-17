# -*- coding: utf-8 -*-
"""Test commands of 'sim_db' command line tool."""
# Copyright (C) 2017, 2018 Håkon Austlid Taskén <hakon.tasken@gmail.com>
# Licenced under the MIT License.

import add_package_root_to_path
import common_test_helpers
import subprocess

def test_c_multithreading(capsys):
    with capsys.disabled():
        print("\nTest C Multithreading and Processing...")
    output = subprocess.check_output(
            "make -f handwritten_makefile c_mtap_run".split(' '), 
            universal_newlines=True)
    last_line = output.splitlines()[-1]
    assert last_line.strip() == "finished"

def test_python_multithreading(capsys):
    with capsys.disabled():
        print("\nTest Python Multithreading and Processing...")
    output = subprocess.check_output(
            "python multithreading_and_processing.py".split(' '), 
            universal_newlines=True)
    last_line = output.splitlines()[-1]
    assert last_line.strip() == "finished"
