// Example program showing how to use the C++ verions of 'sim_db'.
//
// Usage: 'add_and_run --filename sim_params_example_cpp_program.txt'
//    or with parameters with id, ID, in database:
//        'make build_cpp_example'
//      + './cpp_example --id ID --path_sim_db ".."

// Copyright (C) 2018 Håkon Austlid Taskén <hakon.tasken@gmail.com>
// Licensed under the MIT License.

#include <fstream>
#include <string>
#include <vector>
#include "sim_db.hpp"

int main(int argc, char** argv) {
    // Open database and write some initial metadata to database.
    sim_db::Connection sim_db(argc, argv);

    // Read parameters from database.
    std::string example_param1 = sim_db.read<std::string>("example_param1");
    std::vector<int> example_param2 =
            sim_db.read<std::vector<int> >("example_param2");

    // Write to database.
    double small_result = 42.0;
    sim_db.write<double>("example_small_result", small_result);

    // Make unique subdirectory for storing results and write its name to
    // database.
    std::string name_results_dir = sim_db.make_unique_subdir("example/results");

    // Write some results to a file in the newly create subdirectory.
    int results[3] = {1, 3, 7};
    std::ofstream results_file;
    results_file.open(name_results_dir + "/results.txt");
    for (auto i : results) {
        results_file << i << std::endl;
    }
}

