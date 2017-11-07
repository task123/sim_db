# -*- coding: utf-8 -*-
""" Make job script and submit it to the queue of vilje.

Job scripts are added for either the list of ID's provided if provided, or all
runs with status 'new'. A confirmation question is asked if no ID's are 
provided.

vilje uses PBS (Portable Batch System).
"""
# Copyright (C) 2017 Håkon Austlid Taskén <hakon.tasken@gmail.com>
# Licenced under the MIT License.

from add_sim import get_database_name_from_settings
import sqlite3
import argparse
import time
import subprocess
import os.path

def get_arguments():
    parser = argparse.ArgumentParser(description='Submit job')
    parser.add_argument('-id', type=int, default=None, nargs='+', help="ID of simulations to submit.")
    parser.add_argument('--no_confirmation', action='store_true', help="Does not ask for confirmation about submitting all simulations with status 'new'")
    return parser.parse_args()

def make_job_script(job_script_variables):
    name = job_script_variables[0]
    max_walltime = job_script_variables[1]
    n_nodes = job_script_variables[2]
    project_name = job_script_variables[3]
    module_loads = job_script_variables[4]
    if len(module_loads) > 0:
        module_loads = module_loads[7:-1].split(',')
    export_paths = job_script_variables[5]  
    if len(export_paths) > 0:
        export_paths = export_paths[7:-1].split(',')
    interpreter = job_script_variables[6]  
    program_path = job_script_variables[7]   
    sim_runs_db_path = job_script_variables[8]    
    job_script_name = 'job_script_' + name \
                    + time.strftime("_%Y-%b-%d_%H-%M-%S") + ".sh"
    job_script_file = open(job_script_name, 'w')    
    job_script_file.write("#!/bin/bash\n")
    job_script_file.write("#PBS -N {}\n".format(name))
    job_script_file.write("#PBS -l walltime={}\n".format(max_walltime))
    job_script_file.write("#PBS -l select={}:ncpus=32:mpiprocs=16\n"\
                          .format(n_nodes))
    job_script_file.write("#PBS -A {}\n\n".format(project_name))
    job_script_file.write("module purge\n")
    for module in module_loads:
        job_script_file.write("module load {}\n".format(module))
    for path in export_paths:
        job_script_file.write("export {}\n".format(path))
    job_script_file.write("\nmpirun -np {0} {1} {2} {3}\n"
            .format(16*n_nodes, interpreter, program_path, sim_runs_db_path))
    job_script_file.close()
    return job_script_name

def main():
    args = get_arguments()
    ids = args.id

    database_name = get_database_name_from_settings()
    if database_name:
        db = sqlite3.connect(database_name)
    else:
        print "Could NOT find a path to a database in 'settings.txt'." \
            + "Add path to the database to 'settings.txt'."

    db_cursor = db.cursor()

    if ids == None:
        db_cursor.execute("SELECT id FROM runs WHERE status = 'new';")
        ids = db_cursor.fetchall()
        ids = [i[0] for i in ids]
        answer = None
        while not args.no_confirmation and answer != 'y' and answer != 'Y' \
                and answer != 'yes' and answer != 'Yes':
            answer = raw_input("Would you like to submit simulations with " \
                             + "the following ID's: {}? (y/n) ".format(ids))
            if answer == 'n' or answer == 'N' or answer == 'no' or answer == 'No':
                db.commit()
                db_cursor.close()
                db.close()
                return

    for id_submit in ids:
        try:
            db_cursor.execute("SELECT name, max_walltime, n_nodes, " \
                    + "project_name, module_loads, export_paths, " \
                    + "interpreter, program_path, sim_runs_db_path FROM " \
                    + "runs WHERE id={}".format(id_submit)) 
        except:
            raise ValueError("ID {} in sim_runs.db is ".format(id_submit) \
                    + "missing neccessary parameters to submit job script.")
        job_script_variables = db_cursor.fetchall()[0]
        job_script_name = make_job_script(job_script_variables) 
        subprocess.call(["qsub", job_script_name])
        p = subprocess.Popen(["qsub", job_script_name], stdout=subprocess.PIPE)
        (out, err) = p.communicate()
        db_cursor.execute("UPDATE runs SET status='submitted' WHERE id={}" \
                          .format(id_submit))
        db_cursor.execute("UPDATE runs SET job_id={0} WHERE id={1}" \
                          .format(out, id_submit))

    db.commit()
    db_cursor.close()
    db.close()

if __name__ == '__main__':
    main()

