// Example program showing how to use the C verions of 'sim_db'.
//
// Usage: 'add_and_run --filename sim_params_example_c_program.txt'
//    or with parameters with id, ID, in database:
//        'make build_c_example'
//      + './c_example --id ID --path_sim_db ".."

#include <stdio.h>
#include <string.h>
#include "../sim_db.h"

int main(int argc, char** argv) {
    // Open database and write some initial metadata to database.
    SimDB* sim_db = sim_db_ctor(argc, argv);

    // Read parameters from database.
    char* example_param1 = sim_db_read_string(sim_db, "example_param1");
    SimDBIntVec example_param2 = sim_db_read_int_vec(sim_db, "example_param2");

    // Show that SimDBIntVec contain array of integers and size.
    int* int_array = example_param2.array;
    int size_int_array = example_param2.size;

    // Write to database.
    double small_result = 42.0;
    sim_db_write_double(sim_db, "example_small_result", small_result);

    // Make unique subdirectory for storing results and write its name to
    // database.
    char* name_results_dir =
            sim_db_make_unique_subdir_rel_path(sim_db, "example/results");

    // Write some results to a file in the newly create subdirectory.
    int results[3] = {1, 3, 7};
    FILE* results_file = fopen(strcat(name_results_dir, "/results.txt"), "w");
    for (int i = 0; i < 3; i++) {
        fprintf(results_file, "%d\n", results[i]);
    }
    fclose(results_file);

    // Write final metadata to database and free memory allocated by sim_db.
    sim_db_dtor(sim_db);
}

