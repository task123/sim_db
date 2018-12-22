import multiprocessing as mp
from threading import Thread
import subprocess
import sys
import os
import add_package_root_to_path
import sim_db
import sim_db.src_command_line_tool.commands.add_sim as add_sim

n_processes = 2 # Can NOT be too high.
n_threads_per_process = 2
n_writes_per_thread = 1
n_programs_in_parallel = 10


def read_and_write(sim_database, process_identifier):
    assert sim_database.read("test_multithread") == 99
    sim_database.write("test_multithread_{0}".format(process_identifier), 
                       process_identifier, "int", only_if_empty=True)


class DerivedThread(Thread):
    def __init__(self, process_identifier, db_id):
        Thread.__init__(self)
        self.process_identifier = process_identifier
        self.db_id = db_id

    def run(self):
        self.close_sim_db = False
        self.sim_database = sim_db.SimDB(db_id=self.db_id, store_metadata=True)
        for i in range(n_writes_per_thread):
            read_and_write(self.sim_database, self.process_identifier)
        self.sim_database.close()


def run_multiple_threads(n_threads, process_identifier, db_id):
    threads = []
    for i in range(n_threads):
        threads.append(DerivedThread(process_identifier, db_id))
        threads[i].start()
    for thread in threads:
        thread.join()
    if close_sim_db:
        sim_database.close()

def run_program(db_id, path_proj_root):
    if os.sep == '/':
        space_escaped = '\ '
    else:
        space_escaped = ' '
    command = ["python", "{0}/tests/program.py".format(path_proj_root), 
               "--id", str(db_id), "running_in_parallel"]
    output = subprocess.check_output(command, universal_newlines=True)
    lines = output.splitlines()
    if (lines[0].strip() == "3" and lines[-1] == "raised ColumnError"):
        return "ran_correctly"
    else:
        return "ran_incorrectly"


sim_db.OperationalError
sim_database = sim_db.add_empty_sim(False)
db_id = sim_database.get_id()
path_proj_root = sim_database.get_path_proj_root()

sim_database.write("test_multithread", 99, "int")

pool = mp.Pool(processes=n_processes)
for i in range(n_processes):
    pool.apply_async(run_multiple_threads, args=(n_threads_per_process, i, db_id))
pool.close()
pool.join()

sim_database.delete_from_database()
sim_database.close()

db_id = add_sim.add_sim(
        argv="-f root/tests/params_python_program.txt".split(' '))
pool = mp.Pool(processes=n_programs_in_parallel)
processes = []
for i in range(n_programs_in_parallel):
    processes.append(pool.apply_async(run_program, args=(db_id, path_proj_root)))

pool.close()
pool.join()
for process in processes:
    assert process.get() == "ran_correctly"

print("finished")
