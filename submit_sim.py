# -*- coding: utf-8 -*-
""" Make job script and submit it to the job scheduler.

Job scripts are added for either the list of ID's provided if provided, or all
runs with status 'new'. A confirmation question is asked if no ID's are 
provided.
"""
# Copyright (C) 2017, 2018 Håkon Austlid Taskén <hakon.tasken@gmail.com>
# Licenced under the MIT License.

import helpers
import sqlite3
import argparse
import time
import subprocess
import sys
import math

def get_arguments(argv):
    parser = argparse.ArgumentParser(description='Submit job')
    parser.add_argument('--id', '-i', type=int, default=None, nargs='+', help="ID of simulations to submit.")
    parser.add_argument('--max_walltime', type=str, default=None, nargs='+', help="Maximum walltime the simulation can use, given in 'hh:mm:ss' format.")
    parser.add_argument('--n_tasks', type=int, default=None, nargs='+', help="Number of tasks to run the simulation with. A warning is given if it is not a multiple of the number of logical cores on a node.")
    parser.add_argument('--n_nodes', type=int, default=None, nargs='+', help="Number of nodes to run the simulation on.")
    parser.add_argument('--additional_lines', type=str, default=[], nargs='+', help="Additional lines added to the job script.")
    parser.add_argument('--notify_all', action='store_true', help="Set notification for when simulation begins and ends or if it fails.")
    parser.add_argument('--notify_fail', action='store_true', help="Set notification for if simulation fails.")
    parser.add_argument('--notify_end', action='store_true', help="Set notification for when simulation ends or if it fails.")
    parser.add_argument('--no_confirmation', action='store_true', help="Does not ask for confirmation about submitting all simulations with status 'new'")
    return parser.parse_args(argv)

def make_job_script(db_cursor, i, args, id_submit):
    try:
        db_cursor.execute("SELECT name, max_walltime, n_tasks " \
                + "FROM runs WHERE id={}".format(id_submit)) 
    except:
        raise ValueError("ID {} in the database is ".format(id_submit) \
                + "missing neccessary parameters to submit job script.")
    job_script_variables = db_cursor.fetchall()[0]
    settings = helpers.Settings()
    which_job_scheduler = settings.read('which_job_scheduler')[0]
    if which_job_scheduler != 'SLURM' and which_job_scheduler != 'PBS':
        print("'Which job scheduler' in settings.txt is NOT one of the valid " \
            + "values: 'SLURM' or 'PBS'.")
        exit()

    name = job_script_variables[0]
    if name != None:
        job_script_name = 'job_script_' + time.strftime("%Y-%b-%d_%H-%M-%S") \
                        + '_' + name + '_' + str(id_submit) + ".sh"
    else:
        job_script_name = 'job_script_' + time.strftime("%Y-%b-%d_%H-%M-%S") \
                        + '_' + str(id_submit) + ".sh"
    job_script_file = open(job_script_name, 'w')    
    job_script_file.write("#!/bin/bash\n")

    if name != None:
        if which_job_scheduler == 'SLURM':
            job_script_file.write("#SBATCH --job-name={}\n".format(name))
        elif which_job_scheduler == 'PBS': 
            job_script_file.write("#PBS -N {}\n".format(name))

    max_walltime = job_script_variables[1]
    if args.max_walltime != None:
        max_walltime = args.max_walltime[i]
        db_cursor.execute("UPDATE runs SET max_walltime = '{0}' WHERE id = {1}" \
                .format(max_walltime, id_submit))
    if which_job_scheduler == 'SLURM':
        job_script_file.write("#SBATCH --time={}\n".format(max_walltime))
    elif which_job_scheduler == 'PBS': 
        job_script_file.write("#PBS -l walltime={}\n".format(max_walltime))
   

    n_cpus_per_node = settings.read('n_cpus_per_node')
    if len(n_cpus_per_node) > 0:
        n_cpus_per_node = n_cpus_per_node[0]
    else:
        n_cpus_per_node = None

    n_tasks = job_script_variables[2]
    if args.n_tasks != None or args.n_nodes != None:
        if args.n_tasks != None:
            n_tasks = args.n_tasks[i]
        else:
            n_tasks = args.n_nodes[i]*n_cpus_per_node
        db_cursor.execute("UPDATE runs SET n_tasks = {0} WHERE id = {1}" \
                .format(n_tasks, id_submit))
    if n_cpus_per_node != None:
        if n_tasks % n_cpus_per_node != 0:
            print("WARNING: Number of tasks (processes) is NOT a multiple of " \
                 +"the number of logical cpus per node.")
    if which_job_scheduler == 'SLURM':
        job_script_file.write("#SBATCH --ntasks={}\n".format(n_tasks))
    elif which_job_scheduler == 'PBS':
        n_nodes = int(math.ceil(n_tasks/float(n_cpus_per_node)))
        job_script_file.write("#PBS -l nodes={0}:ppn={1}\n".format(n_nodes, n_cpus_per_node))

    memory_per_node = settings.read('memory_per_node')
    if len(memory_per_node) > 0:
        memory_per_cpu = memory_per_node[0]/float(n_cpus_per_node)
        if which_job_scheduler == 'SLURM':
            job_script_file.write("#SBATCH --mem-per-cpu={}G\n".format(memory_per_cpu))
        elif which_job_scheduler == 'PBS':
            job_script_file.write("PBS --mem={}GB\n".format(memory_per_node[0]))

    account = settings.read('account')
    if len(account) > 0:
        account = account[0]
        if which_job_scheduler == 'SLURM':
            job_script_file.write("#SBATCH --account={}\n".format(account))
        elif which_job_scheduler == 'PBS':
            job_script_file.write("#PBS -A {}\n".format(account))

    if args.notify_all or args.notify_fail or args.notify_fail:
        if which_job_scheduler == 'SLURM':
            job_script_file.write("#SBATCH --mail-user={}\n".format(settings.read('email')))
            if args.notify_all:
                job_script_file.write("#SBATCH --mail-type=ALL\n")
            if args.notify_fail:
                job_script_file.write("#SBATCH --mail-type=FAIL\n")
            if args.notify_end:
                job_script_file.write("#SBATCH --mail-type=END\n")
        elif which_job_scheduler == 'PBS':
            job_script_file.write("#PBS -M {}\n".format(settings.read('email')))
            if args.notify_all:
                job_script_file.write("#PBS -m abe\n")
            if args.notify_fail:
                job_script_file.write("#PBS -m a\n")
            if args.notify_end:
                job_script_file.write("#PBS -m e\n")

    for line in args.additional_lines:
        job_script_file.write(line + '\n')

    for line in settings.read('add_to_job_script'):
        job_script_file.write(line)

    run_command = helpers.get_run_command(db_cursor, id_submit, job_script_variables[2])
    job_script_file.write('\n')
    for command in run_command.split(';'):
        job_script_file.write("{}\n".format(command))

    job_script_file.close()

    return job_script_name

def submit_sim(argv=None):
    args = get_arguments(argv)
    ids = args.id

    db = helpers.connect_sim_db()
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

    which_job_scheduler = helpers.Settings().read('which_job_scheduler')[0]
    for i, id_submit in enumerate(ids):
        job_script_name = make_job_script(db_cursor, i, args, id_submit)
        if which_job_scheduler == 'SLURM':
            p = subprocess.Popen(["sbatch", job_script_name])
            (job_id, err) = p.communicate()
        elif which_job_scheduler == 'PBS':
            p = subprocess.Popen(["qsub", job_script_name])
            (job_id, err) = p.communicate()
        db_cursor.execute("UPDATE runs SET status='submitted' WHERE id={}" \
                          .format(id_submit))
        db_cursor.execute("UPDATE runs SET job_id={0} WHERE id={1}" \
                          .format(out, id_submit))

    db.commit()
    db_cursor.close()
    db.close()

if __name__ == '__main__':
    submit_sim()
