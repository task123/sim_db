// Extensive example showing how to use the C++ verions of 'sim_db'.
//
// Usage: 'add_and_run --filename params_extensive_cpp_example.txt'
//    or with parameters with id, ID, in database:
//        'make extensive_cpp_example_updated'
//      + './extensive_cpp_example --id ID --path_sim_db ".."

// Copyright (C) 2018 Håkon Austlid Taskén <hakon.tasken@gmail.com>
// Licensed under the MIT License.

#include <fstream>
#include <iostream>
#include <string>
#include <vector>

#include "sim_db.hpp"  // Parts from the standard library is also included.

int main(int argc, char** argv) {
    // Open database and write some initial metadata to database.
    sim_db::Connection sim_db(argc, argv);

    // Read parameters from database.
    auto example_param1 = sim_db.read<int>("param1");
    auto example_param2 = sim_db.read<double>("param2");
    auto example_param3 = sim_db.read<std::string>("param3");
    auto example_param4 = sim_db.read<bool>("param4");
    auto example_param5 = sim_db.read<std::vector<int> >("param5");
    auto example_param6 = sim_db.read<std::vector<double> >("param6");
    auto example_param7 = sim_db.read<std::vector<std::string> >("param7");
    auto example_param8 = sim_db.read<std::vector<bool> >("param8");

    // Demonstrate that the simulation is running.
    std::cout << example_param3 << std::endl;

    // Write all the possible types to database.
    // Only these types are can be written to the database.
    sim_db.write("example_result_1", example_param1);
    sim_db.write("example_result_2", example_param2);
    sim_db.write("example_result_3", example_param3);
    sim_db.write("example_result_4", example_param4);
    sim_db.write("example_result_5", example_param5);
    sim_db.write("example_result_6", example_param6);
    sim_db.write("example_result_7", example_param7);
    sim_db.write("example_result_8", example_param8);

    // Make unique subdirectory for storing results and write its name to
    // database. Large results are recommended to be saved in this subdirectory.
    std::string name_results_dir = sim_db.make_unique_subdir("example/results");

    // Write some results to a file in the newly create subdirectory.
    std::ofstream results_file;
    results_file.open(name_results_dir + "/results.txt");
    for (auto i : example_param6) {
        results_file << i << std::endl;
    }
}

