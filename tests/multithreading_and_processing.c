/// Testing multithreading and multiprocessing for C verison of 'sim_db'.

// Copyright (C) 2018-2019 Håkon Austlid Taskén <hakon.tasken@gmail.com>
// Licensed under the MIT License.

#define _POSIX_C_SOURCE 2

#include <assert.h>
#include <errno.h>
#include <fcntl.h>
#include <limits.h>
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/wait.h>
#include <unistd.h>
#include "sim_db.h"

#ifndef PATH_MAX
#define PATH_MAX 4096
#endif

void print_array(int* array, int length) {
    for (int i = 0; i < length; i++) {
        printf("%d ", array[i]);
    }
    printf("\n");
}

void read_and_write(SimDB* sim_db) {
    assert(sim_db_read_int(sim_db, "test_multithread") == 99);
    assert(!sim_db_have_timed_out(sim_db));
    char column_name[100];
    sprintf(column_name, "test_multithread_%d", getpid());
    sim_db_write_int(sim_db, column_name, getpid(), true);
    assert(!sim_db_have_timed_out(sim_db));
}

typedef struct {
    int id;
    int n_writes_per_thread;
} ThreadInput;

void* thread_function(void* args) {
    ThreadInput thread_input = *((ThreadInput*) args);

    SimDB* sim_db = sim_db_ctor_with_id(thread_input.id, false);
    sim_db_allow_timeouts(sim_db, false);

    for (int i = 0; i < thread_input.n_writes_per_thread; i++) {
        read_and_write(sim_db);
    }

    sim_db_dtor(sim_db);
    return NULL;
}

// Return EXIT_SUCCESS if file can be opened
int run_shell_command(const char* command, char* output, size_t len_output) {
    FILE* file;
    file = popen(command, "r");
    size_t i = 0;
    int c;
    if (file) {
        while ((c = getc(file)) != EOF && i < len_output - 1) {
            output[i++] = (char) c;
        }
        output[i] = '\0';
        pclose(file);
        return EXIT_SUCCESS;
    } else {
        pclose(file);
        return EXIT_FAILURE;
    }
}

int main() {
    int n_processes = 2;  // Can NOT be too high.
    int n_threads_per_process = 2;
    int n_writes_per_thread = 1;
    int n_programs_parallel = 10;

    SimDB* sim_db_parent = sim_db_add_empty_sim(false);
    sim_db_write_int(sim_db_parent, "test_multithread", 99, true);
    int id = sim_db_get_id(sim_db_parent);
    char path_proj_root[PATH_MAX + 100];
    strcpy(path_proj_root, sim_db_get_path_proj_root(sim_db_parent));
    int child_pid = 1;
    int child_pids[n_processes];
    for (int i = 0; i < n_processes; i++) {
        if (child_pid > 0) {
            child_pid = fork();
            child_pids[i] = child_pid;
        }
    }
    if (child_pid == 0) {
        pthread_t* threads =
                (pthread_t*) malloc(n_threads_per_process * sizeof(pthread_t));
        ThreadInput thread_input;
        thread_input.id = id;
        thread_input.n_writes_per_thread = n_writes_per_thread;
        for (int i = 0; i < n_threads_per_process; i++) {
            pthread_create(&threads[i], NULL, &thread_function, &thread_input);
        }
        for (int i = 0; i < n_threads_per_process; i++) {
            pthread_join(threads[i], NULL);
        }
    } else {
        int wpid;
        while ((wpid = wait(NULL)) > 0) {
        };
        char column_name[100];
        for (int i = 0; i < n_processes; i++) {
            sprintf(column_name, "test_multithread_%d", child_pids[i]);
            assert(sim_db_read_int(sim_db_parent, column_name)
                   == child_pids[i]);
        }
        sim_db_delete_from_database(sim_db_parent);
        sim_db_dtor(sim_db_parent);
    }
    int output_length = 80;
    char output[output_length];
    run_shell_command("sim_db add -f root/tests/params_c_program.txt", output,
                      output_length);
    char* id_str_added = strchr(output, ':') + 2;
    *(strchr(id_str_added, '\n')) = '\0';
    int id_added = atoi(id_str_added);

    for (int i = 0; i < n_programs_parallel; i++) {
        if (child_pid > 0) {
            child_pid = fork();
        }
    }
    if (child_pid == 0) {
        char command[PATH_MAX + 100];
        sprintf(command, "\"%s/tests/c_program\" --id %d running_in_parallel",
                path_proj_root, id_added);
        int output_program_length = 300;
        char output_program[output_program_length];
        run_shell_command(command, output_program, output_program_length);
        assert(output_program[strlen(output_program) - 2] == '0');
    } else {
        int wpid;
        while ((wpid = wait(NULL)) > 0) {
        };
        char command[100];
        sprintf(command, "sim_db delete --id %d --no_checks", id_added);
        run_shell_command(command, output, output_length);
        printf("finished\n");
    }
}
