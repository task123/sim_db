# -*- coding: utf-8 -*-
""" Generate commands (shell scripts) to run the programs.

This directory is added to the PATH if wished, so that the commands can be 
performed from anywhere. For Linux and Mac this involes adding a line to 
~/.bashrc and ~/.bash_profile respectfully, where for Windows nothing is done.

'sim.db' in this directory is also added to the databases in 
settings.txt if wished.
"""
# Copyright (C) 2017, 2018 Håkon Austlid Taskén <hakon.tasken@gmail.com>
# Licenced under the MIT License.

from source_commands import helpers
import fnmatch
from sys import platform
import os

def get_previous_path(where_to_add_path):
    bash_file = open(where_to_add_path, 'r')
    previous_path = None
    for line in bash_file.readlines():
        if line.split(' ')[0] == 'export':
            if len(line.split('/sim_db/commands')) == 2:
                previous_path = line.split(':')[-1].strip()
                previous_path = previous_path.replace('\ ', ' ')
                previous_path = previous_path.rsplit('/', 1)[0]
    return previous_path

def add_path(where_to_add_path):
    answer = helpers.user_input("Would you like to add 'sim_db/' to your PATH " \
            +"and 'cd_results' function in {0}? (y/n)\n(Recommended ".format(where_to_add_path) \
            +"and needed to run commands.)\n")
                    
    if answer == 'y' or answer == 'Y' or answer == 'yes' or answer == 'Yes':
        bash_file = open(where_to_add_path, 'a')
        bash_file.write("\n# Add sim_db commands to PATH\n")
        sim_db_dir = helpers.get_closest_sim_db_dir_path()
        sim_db_dir = sim_db_dir.replace(' ', '\ ')
        bash_file.write("export PATH=$PATH:{0}\n".format(sim_db_dir + "/commands"))
        bash_file.write("\n# Add a 'sim_db' command (as 'cd' called from a " \
                       +"script don't work)\n")
        bash_file.write("function cd_results(){\n")
        bash_file.write('    cd "$(python {0}/source_commands/cd_results.py $@)"\n' \
                .format(sim_db_dir)) 
        bash_file.write("}\n")
        bash_file.close()
        print("\nRemember to source the newly added path:")
        print("$ source {0}".format(where_to_add_path))
    else:
        print("No changes were made to {0}".format(where_to_add_path))

def share_paths_between_sim_dbs(previous_path):
    answer = helpers.user_input("\nWould you like to add path to the settings " \
                   + "of the other copies of 'sim_db'? (y/n)\n(Recommended " \
                   + "and needed to run commands.)")
    if answer == 'y' or answer == 'Y' or answer == 'yes' or answer == 'Yes':
        settings = helpers.Settings()
        sim_db_copies = settings.read('other_sim_db_copies', 
                                      previous_path + '/settings.txt')
        sim_db_copies.append(previous_path)
        sim_db_dir = helpers.get_closest_sim_db_dir_path()
        for copy in sim_db_copies:
            if os.path.exists(copy):
                settings.add('other_sim_db_copies', copy)
                settings.add('other_sim_db_copies', sim_db_dir,
                             path_settings=copy + '/settings.txt')
            else:
                for copy_2 in sim_db_copies:
                    if copy_2 != copy and os.path.exists(copy_2 + '/settings.txt'):
                        settings.remove('other_sim_db_copies', copy, \
                                path_settings=copy_2 + '/settings.txt') 
    else:
        print("\nNo changes were made to the settings of any the other local" \
            + "copies of 'sim_db'.")

def replace_old_path(previous_path, where_to_add_path):
    sim_db_dir = helpers.get_closest_sim_db_dir_path()
    sim_db_dir = sim_db_dir.replace(' ', '\ ')
    previous_path = previous_path.replace(' ', '\ ')
    answer = helpers.user_input("\nWould you like to replace paths to a 'sim_db', " \
            +"that no longer exists, in {0} with new ones?".format(where_to_add_path) \
            +"\n('{0}' => '{1}')\n".format(previous_path, sim_db_dir) \
            +"(Recommended and needed to run commands.)\n")
    if answer == 'y' or answer == 'Y' or answer == 'yes' or answer == 'Yes':
        all_new_lines = []
        with open(where_to_add_path, 'r') as bash_file:
            for line in bash_file:
                all_new_lines.append(line.replace('{0}'.format(previous_path), 
                                             '{0}'.format(sim_db_dir)))
        with open(where_to_add_path, 'w') as bash_file:
            for line in all_new_lines:
                bash_file.write(line)
    else:
        print("No changes were made to {0}".format(where_to_add_path))
 
def main():
    sim_db_dir = os.path.dirname(os.path.abspath(__file__))
    source_commands_dir = sim_db_dir + "/source_commands"
    programs = fnmatch.filter(os.listdir(source_commands_dir), "*.py")
    programs.remove('helpers.py')
    programs.remove('__init__.py')
    programs.remove('cd_results.py')
    sim_db_dir = sim_db_dir.replace(" ", "\ ")
    for program in programs:
        script_name = "commands/" + program.split('.')[0]
        script_file = open(script_name, 'w')
        script_file.write('python {0}/source_commands/{1} "$@"'.format(sim_db_dir, program))
        script_file.close()
        os.system("chmod u+x {0}".format(script_name))

    where_to_add_path = None
    home = os.path.expanduser("~")
    if platform == "linux" or platform == "linux2" or platform == "linux3":
        where_to_add_path = "{0}/.bashrc".format(home)
    elif platform == "darwin":
        where_to_add_path = "{0}/.bash_profile".format(home)
    elif platform == 'cygwin':
        where_to_add_path = "{0}/.bashrc".format(home)

    if where_to_add_path:
        previous_path = get_previous_path(where_to_add_path)
        if previous_path == None:
            add_path(where_to_add_path)
        elif not os.path.exists(previous_path):
            replace_old_path(previous_path, where_to_add_path)
        else:
            print("There is already a sim_db added to {0}.".format(where_to_add_path))
            share_paths_between_sim_dbs(previous_path)
            
if __name__ == '__main__':
    main()
