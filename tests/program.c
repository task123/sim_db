/// Testing 'sim_db' for C, that is 'sim_db.h' and 'sim_db.c'.
///
/// Read in parameters from database, write parameters to database, make unique
/// subdirectory for results and save 'results.txt' in this directory.

// Copyright (C) 2018-2019 Håkon Austlid Taskén <hakon.tasken@gmail.com>
// Licensed under the MIT License.

#include <assert.h>
#include <limits.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include "sim_db.h"

#ifndef PATH_MAX
#define PATH_MAX 4096
#endif

int main(int argc, char** argv) {
    bool store_metadata = true;
    bool running_in_parallel = false;
    for (int i = 0; i < argc; i++) {
        if (strcmp(argv[i], "no_metadata") == 0) {
            store_metadata = false;
        } else if (strcmp(argv[i], "running_in_parallel") == 0) {
            running_in_parallel = true;
        }
    }

    printf("%s\n", SIM_DB_VERSION);

    SimDB* sim_db;
    if (store_metadata) {
        sim_db = sim_db_ctor(argc, argv);
    } else {
        sim_db = sim_db_ctor_no_metadata(argc, argv);
    }
    sim_db_allow_timeouts(sim_db, false);

    int param1 = sim_db_read_int(sim_db, "test_param1");
    printf("%d\n", param1);
    sim_db_write_int(sim_db, "new_test_param1", param1, true);
    printf("%d\n", sim_db_read_int(sim_db, "new_test_param1"));

    double param2 = sim_db_read_double(sim_db, "test_param2");
    printf("%f\n", param2);
    sim_db_write_double(sim_db, "new_test_param2", param2, true);
    printf("%f\n", sim_db_read_double(sim_db, "new_test_param2"));

    char* param3 = sim_db_read_string(sim_db, "test_param3");
    printf("%s\n", param3);
    sim_db_write_string(sim_db, "new_test_param3", param3, true);
    printf("%s\n", sim_db_read_string(sim_db, "new_test_param3"));

    bool param4 = sim_db_read_bool(sim_db, "test_param4");
    printf("%d\n", param4);
    sim_db_write_bool(sim_db, "new_test_param4", param4, true);
    printf("%d\n", sim_db_read_bool(sim_db, "new_test_param4"));

    SimDBIntVec int_vec = sim_db_read_int_vec(sim_db, "test_param5");
    for (size_t i = 0; i < int_vec.size; i++) {
        printf("%d\n", int_vec.array[i]);
    }
    sim_db_write_int_array(sim_db, "new_test_param5", int_vec.array,
                           int_vec.size, true);
    int_vec = sim_db_read_int_vec(sim_db, "new_test_param5");
    for (size_t i = 0; i < int_vec.size; i++) {
        printf("%d\n", int_vec.array[i]);
    }

    SimDBDoubleVec double_vec = sim_db_read_double_vec(sim_db, "test_param6");
    for (size_t i = 0; i < double_vec.size; i++) {
        printf("%f\n", double_vec.array[i]);
    }
    sim_db_write_double_array(sim_db, "new_test_param6", double_vec.array,
                              double_vec.size, true);
    double_vec = sim_db_read_double_vec(sim_db, "new_test_param6");
    for (size_t i = 0; i < double_vec.size; i++) {
        printf("%f\n", double_vec.array[i]);
    }

    SimDBStringVec string_vec = sim_db_read_string_vec(sim_db, "test_param7");
    for (size_t i = 0; i < string_vec.size; i++) {
        printf("%s\n", string_vec.array[i]);
    }
    sim_db_write_string_array(sim_db, "new_test_param7", string_vec.array,
                              string_vec.size, true);
    string_vec = sim_db_read_string_vec(sim_db, "new_test_param7");
    for (size_t i = 0; i < string_vec.size; i++) {
        printf("%s\n", string_vec.array[i]);
    }

    SimDBBoolVec bool_vec = sim_db_read_bool_vec(sim_db, "test_param8");
    for (size_t i = 0; i < bool_vec.size; i++) {
        printf("%d\n", bool_vec.array[i]);
    }
    sim_db_write_bool_array(sim_db, "new_test_param8", bool_vec.array,
                            bool_vec.size, true);
    bool_vec = sim_db_read_bool_vec(sim_db, "new_test_param8");
    for (size_t i = 0; i < bool_vec.size; i++) {
        printf("%d\n", bool_vec.array[i]);
    }

    int param9 = sim_db_read_int(sim_db, "test_param9");
    printf("%d\n", param9);
    sim_db_write_int(sim_db, "new_test_param9", param9, true);
    printf("%d\n", sim_db_read_int(sim_db, "new_test_param9"));

    int param10 = sim_db_read_int(sim_db, "test_param10");
    printf("%d\n", param10);
    sim_db_write_int(sim_db, "new_test_param10", param10, true);
    printf("%d\n", sim_db_read_int(sim_db, "new_test_param10"));

    printf("%d\n", sim_db_is_empty(sim_db, "test_param11"));
    sim_db_set_empty(sim_db, "test_param11");
    printf("%d\n", sim_db_is_empty(sim_db, "test_param11"));

    if (store_metadata) {
        char* results_dir =
                sim_db_unique_results_dir(sim_db, "root/tests/results");
        char results_file[PATH_MAX + 80];
        sprintf(results_file, "%s/results.txt", results_dir);
        FILE* result_file = fopen(results_file, "w");
        if (result_file) {
            for (size_t i = 0; i < double_vec.size; i++) {
                fprintf(result_file, "%f\n", double_vec.array[i]);
            }
            fclose(result_file);
        }
    }

    printf("%d\n", sim_db_column_exists(sim_db, "test_param1"));
    printf("%d\n", sim_db_column_exists(sim_db, "test_column_does_not_exists"));

    char path_proj_root[PATH_MAX + 1];
    strcpy(path_proj_root, sim_db_get_path_proj_root(sim_db));

    sim_db_dtor(sim_db);

    if (!running_in_parallel) {
        SimDB* sim_db_2 =
                sim_db_add_empty_sim_without_search(path_proj_root, false);

        assert(!sim_db_have_timed_out(sim_db_2));
        sim_db_allow_timeouts(sim_db, false);

        printf("%d\n", sim_db_get_id(sim_db_2));

        sim_db_write_int(sim_db_2, "test_param1", 7, true);

        param1 = sim_db_read_int(sim_db_2, "test_param1");
        printf("%d\n", param1);

        sim_db_delete_from_database(sim_db_2);
        sim_db_dtor(sim_db_2);
    }
}
