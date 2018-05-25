// Minimal example showing how to use the C verions of 'sim_db'.
//
// Usage: 'add_and_run --filename params_minimal_c_example.txt'
//    or with parameters with id, ID, in database:
//        'make minimal_cpp_example_updated'
//      + './minimal_c_example --id ID --path_sim_db ".."

// Copyright (C) 2018 Håkon Austlid Taskén <hakon.tasken@gmail.com>
// Licensed under the MIT License.

#include <stdio.h>
#include <string.h>

#include "sim_db.h"  // Parts from the standard library is also included.

int main(int argc, char** argv) {
    // Open database and write some initial metadata to database.
    SimDB* sim_db = sim_db_ctor(argc, argv);

    // Read parameters from database.
    char* param1 = sim_db_read_string(sim_db, "param1");
    int param2 = sim_db_read_int(sim_db, "param2");

    // Demonstrate that the simulation is running.
    printf("%s\n", param1);

    // Write final metadata to database and free memory allocated by sim_db.
    sim_db_dtor(sim_db);
}
