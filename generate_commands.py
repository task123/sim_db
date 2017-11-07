# -*- coding: utf-8 -*-
""" Generate commands (shell scripts) to run the programs.

This directory is added to the PATH if wished, so that the commands can be 
performed from anywhere. For Linux and Mac this involes adding a line to 
~/.bashrc and ~/.bash_profile respectfully, where for Windows nothing is done.

'sim.db' in this directory is also added to the databases in 
settings.txt if wished.
"""
# Copyright (C) 2017 Håkon Austlid Taskén <hakon.tasken@gmail.com>
# Licenced under the MIT License.

import fnmatch
from sys import platform
import os

def add_database_to_settings():
    settings_file = open('settings.txt', 'r')
    settings_content = settings_file.readlines()
    settings_file.close()

    for i, line in enumerate(settings_content):
        if len(line) > 10 and line[:11] == "# Databases":
            break
    sim_db_dir = os.path.dirname(os.path.abspath(__file__))
    settings_content.insert(i+3, sim_db_dir + "/sim.db\n")

    settings_file = open('settings.txt', 'w')
    settings_file.writelines(settings_content)
    settings_file.close()
            
def main():
    sim_db_dir = os.path.dirname(os.path.abspath(__file__))
    programs = fnmatch.filter(os.listdir(sim_db_dir), "*.py")
    programs.remove('generate_commands.py')
    sim_db_dir = sim_db_dir.replace(" ", "\ ")
    for program in programs:
        script_name = program.split('.')[0]
        script_file = open(script_name, 'w')
        script_file.write('python {0}/{1} "$@"'.format(sim_db_dir, program))
        script_file.close()
        os.system("chmod 700 {}".format(script_name))

    where_to_add_path = None
    home = os.path.expanduser("~")
    if platform == "linux" or platform == "linux2":
        where_to_add_path = "{}/.bashrc".format(home)
    elif platform == "darwin":
        where_to_add_path = "{}/.bash_profile".format(home)

    if where_to_add_path:
        answer = raw_input("Would you like to add 'sim_db/' to your PATH in " \
                         + "{}? (y/n)".format(where_to_add_path))
        if answer == 'y' or answer == 'Y' or answer == 'yes' or answer == 'Yes':
            bash_file = open(where_to_add_path, 'a')
            bash_file.write("\n# Add sim_db commands to PATH\n")
            bash_file.write("export PATH=$PATH:{}".format(sim_db_dir))
            bash_file.close()
            os.system("source {}".format(where_to_add_path))
        else:
            print "No changes were made to {}".format(where_to_add_path)

    answer = raw_input("\nWould you like to add 'sim.db' in this " \
                     + "directory to the databases in settings.txt? (y/n)")
    if answer == 'y' or answer == 'Y' or answer == 'yes' or answer == 'Yes':
        add_database_to_settings()
    else:
        print "No changes were made to settings.txt"

if __name__ == '__main__':
    main()
        
        
    

    
