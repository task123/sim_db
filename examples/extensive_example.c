// Extensive example showing how to use the C verions of 'sim_db'.
//
// Usage: 'add_and_run --filename params_extensive_c_example.txt'
//    or with parameters with id, ID, in database:
//        'make extensive_cpp_example_updated'
//      + './extensive_c_example --id ID --path_sim_db ".."

// Copyright (C) 2018-2019 Håkon Austlid Taskén <hakon.tasken@gmail.com>
// Licensed under the MIT License.

#include <limits.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

#ifndef PATH_MAX
#define PATH_MAX 4096
#endif

#include "sim_db.h"  // Parts from the standard library is also included.

int main(int argc, char** argv) {
    // Open database and write some initial metadata to database.
    SimDB* sim_db = sim_db_ctor(argc, argv);

    // Read parameters from database.
    int param1 = sim_db_read_int(sim_db, "param1_extensive");
    double param2 = sim_db_read_double(sim_db, "param2_extensive");
    char* param3 = sim_db_read_string(sim_db, "param3_extensive");
    bool param4 = sim_db_read_bool(sim_db, "param4_extensive");
    SimDBIntVec param5 = sim_db_read_int_vec(sim_db, "param5_extensive");
    SimDBDoubleVec param6 = sim_db_read_double_vec(sim_db, "param6_extensive");
    SimDBStringVec param7 = sim_db_read_string_vec(sim_db, "param7_extensive");
    SimDBBoolVec param8 = sim_db_read_bool_vec(sim_db, "param8_extensive");

    // Show that SimDBIntVec contain array of integers and size.
    int* int_array = param5.array;
    int size_int_array = param5.size;

    // Demonstrate that the simulation is running.
    printf("%s\n", param3);

    // Write all the possible types to database.
    // Only these types are can be written to the database.
    sim_db_write_int(sim_db, "example_result_1", param1, false);
    sim_db_write_double(sim_db, "example_result_2", param2, true);
    sim_db_write_string(sim_db, "example_result_3", param3, false);
    sim_db_write_bool(sim_db, "example_result_4", param4, true);
    sim_db_write_int_array(sim_db, "example_result_5", param5.array,
                           param5.size, false);
    sim_db_write_double_array(sim_db, "example_result_6", param6.array,
                              param6.size, true);
    sim_db_write_string_array(sim_db, "example_result_7", param7.array,
                              param7.size, false);
    sim_db_write_bool_array(sim_db, "example_result_8", param8.array,
                            param8.size, true);

    // Make unique subdirectory for storing results and write its name to
    // database. Large results are recommended to be saved in this subdirectory.
    char* name_subdir =
            sim_db_unique_results_dir(sim_db, "root/examples/results");

    // Write some results to a file in the newly create subdirectory.
    FILE* result_file = fopen(strcat(name_subdir, "/results.txt"), "w");
    for (size_t i = 0; i < param6.size; i++) {
        fprintf(result_file, "%f\n", param6.array[i]);
    }
    fclose(result_file);

    // Check if column exists in database.
    bool is_column_in_database =
            sim_db_column_exists(sim_db, "column_not_in_database");

    // Check if column is empty and then set it to empty.
    bool is_empty = sim_db_is_empty(sim_db, "example_result_1");
    sim_db_set_empty(sim_db, "example_result_1");

    // Get the 'ID' of the connected simulation and the path to the project's
    // root directoy.
    int id = sim_db_get_id(sim_db);
    char path_proj_root[PATH_MAX + 1];
    strcpy(path_proj_root, sim_db_get_path_proj_root(sim_db));

    // Write final metadata to the database, close the connection and free
    // memory allocated by sim_db.
    sim_db_dtor(sim_db);

    // Add an empty simulation to the database, open connection and write to it.
    SimDB* sim_db_2 =
            sim_db_add_empty_sim_without_search(path_proj_root, false);
    sim_db_write_int(sim_db_2, "param1_extensive", 7, false);

    // Delete simulation from database.
    sim_db_delete_from_database(sim_db_2);

    // Close connection to the database and free memory allocated by sim_db.
    sim_db_dtor(sim_db_2);
}
