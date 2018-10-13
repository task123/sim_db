// Minimal example showing how to use the C++ verions of 'sim_db'.
//
// Usage: 'add_and_run --filename params_minimal_cpp_example.txt'
//    or with parameters with id, ID, in database:
//        'make minimal_cpp_example_updated'
//      + './minimal_cpp_example --id ID --path_sim_db ".."

// Copyright (C) 2018 Håkon Austlid Taskén <hakon.tasken@gmail.com>
// Licensed under the MIT License.

#include <iostream>
#include <string>
#include <vector>

#include "sim_db.hpp"  // Parts from the standard library is also included.

int main(int argc, char** argv) {
    // Open database and write some initial metadata to database.
    sim_db::Connection sim_db(argc, argv);

    // Read parameters from database.
    auto param1 = sim_db.read<std::string>("param1");
    auto param2 = sim_db.read<int>("param2");

    // Demonstrate that the simulation is running.
    std::cout << param1 << std::endl;
}
