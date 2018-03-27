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

from helpers import Settings
import fnmatch
from sys import platform
import os

def get_previous_path(where_to_add_path):
    bash_file = open(where_to_add_path, 'r')
    previous_path = None
    for line in bash_file.readlines():
        if line.split(' ')[0] == 'export':
            if line.split('/')[-1].strip() == 'sim_db':
                previous_path = line.split(':')[-1].strip()
                previous_path = previous_path.replace('\ ', ' ')
    return previous_path

def add_path(where_to_add_path):
    answer = raw_input("Would you like to add 'sim_db/' to your PATH in " \
                     + "{}? (y/n)".format(where_to_add_path))
    if answer == 'y' or answer == 'Y' or answer == 'yes' or answer == 'Yes':
        bash_file = open(where_to_add_path, 'a')
        bash_file.write("\n# Add sim_db commands to PATH\n")
        bash_file.write("export PATH=$PATH:{}".format(sim_db_dir))
        bash_file.close()
        os.system("source {}".format(where_to_add_path))
    else:
        print("No changes were made to {}".format(where_to_add_path))

def share_paths_between_sim_dbs(previous_path):
    answer = raw_input("\nWould you like to add path to the settings of the " \
                   + "other copies of 'sim_db'? (y/n)\n(Recommended and " \
                   + "needed to run commands.)")
    if answer == 'y' or answer == 'Y' or answer == 'yes' or answer == 'Yes':
        settings = Settings()
        sim_db_copies = settings.read('other_sim_db_copies', 
                                      previous_path + '/settings.txt')
        sim_db_copies.append(previous_path)
        sim_db_dir = os.path.dirname(os.path.abspath(__file__))
        path_this_settings = sim_db_dir + '/settings.txt'
        for copy in sim_db_copies:
            settings.add('other_sim_db_copies', copy)
            settings.add('other_sim_db_copies', path_this_settings,
                         path_settings=copy + '/settings.txt')
    else:
        print("\nNo changes were made to the settings of any the other local" \
            + "copies of 'sim_db'.")
           
def main():
    sim_db_dir = os.path.dirname(os.path.abspath(__file__))
    programs = fnmatch.filter(os.listdir(sim_db_dir), "*.py")
    programs.remove('generate_commands.py')
    programs.remove('helpers.py')
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
        previous_path = get_previous_path(where_to_add_path)
        if previous_path == None:
            add_path()
        else:
            print("There is already a sim_db added to {}.".format(where_to_add_path))
            share_paths_between_sim_dbs(previous_path)
            
if __name__ == '__main__':
    main()
        
        
    

    
