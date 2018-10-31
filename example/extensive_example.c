// Extensive example showing how to use the C verions of 'sim_db'.
//
// Usage: 'add_and_run --filename params_extensive_c_example.txt'
//    or with parameters with id, ID, in database:
//        'make extensive_cpp_example_updated'
//      + './extensive_c_example --id ID --path_sim_db ".."

// Copyright (C) 2018 Håkon Austlid Taskén <hakon.tasken@gmail.com>
// Licensed under the MIT License.

#include <stdio.h>
#include <string.h>
#include <unistd.h>

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
    sim_db_write_int(sim_db, "example_result_1", param1);
    sim_db_write_double(sim_db, "example_result_2", param2);
    sim_db_write_string(sim_db, "example_result_3", param3);
    sim_db_write_bool(sim_db, "example_result_4", param4);
    sim_db_write_int_array(sim_db, "example_result_5", param5.array,
                           param5.size);
    sim_db_write_double_array(sim_db, "example_result_6", param6.array,
                              param6.size);
    sim_db_write_string_array(sim_db, "example_result_7", param7.array,
                              param7.size);
    sim_db_write_bool_array(sim_db, "example_result_8", param8.array,
                            param8.size);

    // Make unique subdirectory for storing results and write its name to
    // database. Large results are recommended to be saved in this subdirectory.
    char* name_subdir =
            sim_db_make_unique_subdir_rel_path(sim_db, "example/results");

    // Write some results to a file in the newly create subdirectory.
    FILE* result_file = fopen(strcat(name_subdir, "/results.txt"), "w");
    for (size_t i = 0; i < param6.size; i++) {
        fprintf(result_file, "%f\n", param6.array[i]);
    }
    fclose(result_file);

    // Get the path to sim_db and the 'ID' of the connected simulation.
    char* path_sim_db = sim_db_get_path(sim_db);
    int db_id = sim_db_get_id(sim_db);

    // Write final metadata to database and free memory allocated by sim_db.
    sim_db_dtor(sim_db);

    // Add an empty simulation to the database.
    db_it = add_empty_sim(path_sim_db);

    // Open this empty simulation and write to it.
    SimDB* sim_db_2 = sim_db_ctor_with_id(path_sim_db, id, false);
    sim_db_write_int(sim_db_2, "param1_extensive", 7);
    sim_db_dtor(sim_db_2);

    // Delete this simulation.
    delete_sim(db_id);
}
