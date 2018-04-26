# -*- coding: utf-8 -*-
""" Print a list of all the sim_db commands.

These are the commands available after running: 'python generate_commands.py'.
"""
# Copyright (C) 2018 Håkon Austlid Taskén <hakon.tasken@gmail.com>
# Licenced under the MIT License.

import os
import fnmatch

sim_db_dir = os.path.dirname(os.path.abspath(__file__))
programs = fnmatch.filter(os.listdir(sim_db_dir), "*.py")
programs.remove('generate_commands.py')
programs.remove('helpers.py')
programs.remove('sim_db.py')
programs.remove('__init__.py')
programs.sort()
sim_db_dir = sim_db_dir.replace(" ", "\ ")
print("All commands: ('command -h' will explain command and use.)\n")
for program in programs:
    script_name = program.split('.')[0]
    print(script_name)
