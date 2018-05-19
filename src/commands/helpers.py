# -*- coding: utf-8 -*-
""" Read and modify settings."""
# Copyright (C) 2017, 2018 Håkon Austlid Taskén <hakon.tasken@gmail.com>
# Licenced under the MIT License.

import sqlite3
import subprocess
import os
from sys import version_info, platform

default_db_columns = {'id': 'INTEGER PRIMARY KEY',
                      'status': 'TEXT',
                      'name': 'TEXT',
                      'description': 'TEXT',
                      'run_command': 'TEXT',
                      'comment': 'TEXT',
                      'result_dir': 'TEXT',
                      'add_to_job_script': 'TEXT',
                      'max_walltime': 'TEXT',
                      'n_tasks': 'INTEGER',
                      'job_id': 'INTEGER',
                      'time_submitted': 'TEXT',
                      'time_started': 'TEXT',
                      'used_walltime': 'TEXT',
                      'cpu_info': 'TEXT',
                      'git_hash': 'TEXT',
                      'commit_message': 'TEXT',
                      'git_diff_stat': 'TEXT',
                      'git_diff': 'TEXT',
                      'sha1_executables': 'TEXT'
                     }

class Settings:
    settings_dict = {'parameter_files': '## Parameter filenames',
                     'print_config': '## Personalized print configurations',
                     'prefix_run_command': '## Prefix for \'run_command\' for multithreaded/core simultions',
                     'which_job_scheduler': '### Which job scheduler',
                     'n_cpus_per_node': '### Number of logical cpus per node',
                     'memory_per_node': '### Memory per node',
                     'account': '### Account',
                     'email': '### Email for notifications',
                     'add_to_job_script': '### Add to all job scripts submitted:',
                     'other_sim_db_copies': '## Other local sim_db copies'
                    }

    def read(self, key_settings_dict, path_settings=None):
        setting_header = self.settings_dict[key_settings_dict]
        if path_settings == None:
            path_settings = get_closest_sim_db_dir_path() + '/settings.txt'
        settings_file = open(path_settings, 'r')
        settings_found = []
        is_comment = False
        is_found = False
        for line in settings_file:
            line = line.strip()
            if (is_found and len(line) >= 2 and line[:2] == '##'):
                break
            if (len(line) > 0 and line[0] == '('):
                is_comment = True
            if (is_found and not is_comment and len(line) > 1):
                settings_found.append(line)
            if is_comment and len(line) > 0 and line[-1] == ')':
                is_comment = False
            if (len(line) >= len(setting_header) \
                    and line[:len(setting_header)] == setting_header):
                is_found = True
        settings_file.close()
        if is_comment:
            raise ValueError("')' missing in 'settings.txt'.")
        return settings_found

    def add(self, key_settings_dict, setting, path_settings=None):
        setting = setting.strip()
        setting_header = self.settings_dict[key_settings_dict]
        if path_settings == None:
            path_settings = get_closest_sim_db_dir_path() + '/settings.txt'
        settings_file = open(path_settings, 'r')
        settings_content = ''
        is_found = False
        is_comment = False
        is_added = False
        for line in settings_file.readlines():
            settings_content += line
            line = line.strip()
            if (is_found and line == setting):
                settings_file.close()
                return False
            if (is_found and len(line) >= 1 and line[:2] == '##'):
                is_found = False
            if (len(line) > 0 and line[0] == '('):
                is_comment = True
            if (is_found and not is_added and not is_comment):
                settings_content += setting + '\n'
                is_added = True
            if (is_comment and len(line) > 0 and line[-1] == ')'):
                is_comment = False
            if (len(line) >= len(setting_header) \
                    and line[:len(setting_header)] == setting_header):
                is_found = True 
        settings_file.close()
        settings_file = open(path_settings, 'w')
        settings_file.writelines(settings_content)
        settings_file.close()

    def remove(self, key_settings_dict, setting, path_settings=None):
        setting = setting.strip()
        setting_header = self.settings_dict[key_settings_dict]
        if path_settings == None:
            path_settings = get_closest_sim_db_dir_path() + '/settings.txt'
        settings_file = open(path_settings, 'r')
        settings_content = ''
        is_found = False
        is_comment = False
        is_removed = False
        for line in settings_file.readlines():
            line = line.strip()
            if (is_found and len(line) >= 1 and line[:2] == '##'):
                is_found = False
            if (len(line) > 0 and line[0] == '('):
                is_comment = True
            if (is_found and not is_removed and not is_comment):
                is_removed = True
            else:
                settings_content += line + "\n"
            if (is_comment and len(line) > 0 and line[-1] == ')'):
                is_comment = False
            if (len(line) >= len(setting_header) \
                    and line[:len(setting_header)] == setting_header):
                is_found = True 
        settings_file.close()
        settings_file = open(path_settings, 'w')
        settings_file.writelines(settings_content)
        settings_file.close()

def get_closest_sim_db_dir_path():
    currect_dir = os.getcwd()
    source_commands_dir = os.path.dirname(os.path.abspath(__file__))
    sim_db_dir = os.path.abspath(os.path.join(os.path.join(source_commands_dir, os.pardir), os.pardir))
    settings = Settings()
    sim_db_copies = settings.read('other_sim_db_copies', 
                                  sim_db_dir + '/settings.txt')
    sim_db_copies.append(sim_db_dir)
    longest_match_length = 0
    closest_sim_db_path = None
    for copy in sim_db_copies:
        copy = copy.strip()
        match_length = 0
        for i in range(min(len(copy), len(currect_dir))):
            if copy[i] == currect_dir[i]:
                match_length += 1
        if match_length > longest_match_length:
            longest_match_length = match_length
            closest_sim_db_path = copy
    return closest_sim_db_path

def connect_sim_db(full_path_sim_db=None):
    if (full_path_sim_db == None):
        full_path_sim_db = get_closest_sim_db_dir_path() + '/sim.db'
    return sqlite3.connect(full_path_sim_db)

def get_db_column_names_and_types(db_cursor):
    table_info = db_cursor.execute("PRAGMA table_info('runs')")
    column_names = []
    column_types = []
    for row in table_info:
        column_names.append(row[1])
        column_types.append(row[2])
    return column_names, column_types

def search_for_parameter_file_matching_settings():
    settings_file = open(get_closest_sim_db_dir_path() + '/settings.txt', 'r')
    line = ""
    while len(line) < 11 or line[:11] != "# Databases":
        line = settings_file.readline()
        for file_in_current_dir in os.listdir('.'):
            if file_in_current_dir == line.strip():
                return file_in_current_dir
    return None

def get_run_command(db_cursor, db_id, n_tasks=None):
    db_cursor.execute("SELECT run_command, n_tasks FROM runs WHERE id={0};".format(db_id))
    run_command, n_tasks_database = db_cursor.fetchall()[0]
    if n_tasks == None:
        n_tasks = n_tasks_database

    if n_tasks == None:
        n_tasks = 1
    elif n_tasks > 1:
        settings = Settings()
        prefix_run_command = ""
        for prefix in settings.read('prefix_run_command'):
            prefix_run_command += prefix + ' '
        run_command = prefix_run_command + run_command

    sim_db_dir = get_closest_sim_db_dir_path()
    sim_db_dir = sim_db_dir.replace(' ', '\ ')
    run_command = run_command.replace('sim_db/', ' ' + sim_db_dir + '/')
    run_command = run_command.replace(' # ', " {0} ".format(n_tasks))
    run_command = run_command + " --id {0}".format(db_id)
    run_command = run_command + ' --path_sim_db "{0}"'.format(get_closest_sim_db_dir_path())

    return run_command

def get_cpu_and_mem_info():
    if platform == 'linux' or platform == 'linux2' or platform == 'linux3':
        proc = subprocess.Popen(["lscpu"], stdout=subprocess.PIPE, \
                         stderr=open(os.devnull, 'w'), shell=True)
        (out, err) = proc.communicate()
        cpu_info = ""
        wanted_info = ['Model name:', 'CPU(s):', 'Thread(s) per core:', 'Core(s) per socket:',
                       'L1d cache:', 'L1i cache:','L2 cache:', 'L3 cache:']
        for info in wanted_info:
            for lscpu_line in out.decode('UTF-8').splitlines():
                        if info == lscpu_line[0:len(info)]:
                                cpu_info += lscpu_line + '\n'

        proc = subprocess.Popen(["cat /sys/devices/system/cpu/cpu0/cache/index0/coherency_line_size"], stdout=subprocess.PIPE, stderr=open(os.devnull, 'w'), shell=True)
        (out, err) = proc.communicate()
        if out != None:
            cpu_info += "coherency_line_size: " + out.decode('UTF-8') + '\n'

        proc = subprocess.Popen(["free -g -t"], stdout=subprocess.PIPE, \
                                stderr=open(os.devnull, 'w'), shell=True)
        (out, err) = proc.communicate()
        if out != None:
            memory = out.decode('UTF-8').splitlines()[1].split()[0:2]
            cpu_info += memory[0] + ' ' + memory[1] + '\n'

        return cpu_info

    elif platform == 'darwin':
        proc = subprocess.Popen(["sysctl -a"], stdout=subprocess.PIPE, \
                         stderr=open(os.devnull, 'w'), shell=True)
        (out, err) = proc.communicate()
        cpu_info = ""
        wanted_info = ['machdep.cpu.brand_string:', 'machdep.cpu.core_count:', 
                       'machdep.cpu.thread_count:', 'hw.cachelinesize:',
                       'hw.l1icachesize:', 'hw.l1dcachesize:', 'hw.l2cachesize:',
                       'hw.l3cachesize:', 'hw.memsize:']
        for info in wanted_info:
            for lscpu_line in out.decode('UTF-8').splitlines():
                        if info == lscpu_line[0:len(info)]:
                                cpu_info += lscpu_line + '\n'
        return cpu_info
    else:
        return "Not Linux or Mac"
 
def user_input(message):
    """Call raw_input for python 2 and input for python 3."""
    if version_info[0] < 3:
        return raw_input(message)
    else:
        return input(message)

    

