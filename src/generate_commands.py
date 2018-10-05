# -*- coding: utf-8 -*-
""" Generate commands (shell scripts) to run the programs."""
# Copyright (C) 2017, 2018 Håkon Austlid Taskén <hakon.tasken@gmail.com>
# Licenced under the MIT License.

import fnmatch
import os
 
def main():
    sim_db_src_dir = os.path.dirname(os.path.abspath(__file__))
    src_commands_dir = sim_db_src_dir + "/commands"
    programs = fnmatch.filter(os.listdir(src_commands_dir), "*.py")
    programs.remove('helpers.py')
    programs.remove('__init__.py')
    programs.remove('cd_results.py')
    sim_db_src_dir = sim_db_src_dir.replace(" ", "\ ")
    for program in programs:
        script_name = "commands/" + program.split('.')[0]
        script_file = open(script_name, 'w')
        script_file.write('python {0}/commands/{1} "$@"'.format(sim_db_src_dir, program))
        script_file.close()
        os.system("chmod u+x {0}".format(script_name))
            
if __name__ == '__main__':
    main()
