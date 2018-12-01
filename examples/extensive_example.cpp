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
    auto param1 = sim_db.read<int>("param1_extensive");
    auto param2 = sim_db.read<double>("param2_extensive");
    auto param3 = sim_db.read<std::string>("param3_extensive");
    auto param4 = sim_db.read<bool>("param4_extensive");
    auto param5 = sim_db.read<std::vector<int> >("param5_extensive");
    auto param6 = sim_db.read<std::vector<double> >("param6_extensive");
    auto param7 = sim_db.read<std::vector<std::string> >("param7_extensive");
    auto param8 = sim_db.read<std::vector<bool> >("param8_extensive");

    // Demonstrate that the simulation is running.
    std::cout << param3 << std::endl;

    // Write all the possible types to database.
    // Only these types are can be written to the database.
    sim_db.write("example_result_1", param1);
    sim_db.write("example_result_2", param2);
    sim_db.write("example_result_3", param3);
    sim_db.write("example_result_4", param4);
    sim_db.write("example_result_5", param5);
    sim_db.write("example_result_6", param6);
    sim_db.write("example_result_7", param7);
    sim_db.write("example_result_8", param8);

    // Make unique subdirectory for storing results and write its name to
    // database. Large results are recommended to be saved in this subdirectory.
    std::string name_results_dir =
            sim_db.make_unique_subdir("root/examples/results");

    // Write some results to a file in the newly create subdirectory.
    std::ofstream results_file;
    results_file.open(name_results_dir + "/results.txt");
    for (auto i : param6) {
        results_file << i << std::endl;
    }

    // Check is column exists in database.
    bool is_column_in_database = sim_db.column_exists("column_not_in_database");

    // Get the 'ID' of the connected simulation an the path to the project's
    // root directory.
    int id = sim_db.get_id();
    std::string path_proj_root = sim_db.get_path_proj_root();

    // Add an empty simulation to the database.
    id = sim_db::add_empty_sim(path_proj_root);

    // Open this empty simulation and write to it.
    sim_db::Connection sim_db_2(path_proj_root, id);
    sim_db_2.write<int>("param1_extensive", 7);

    // Delete this simulation.
    sim_db::delete_sim(path_proj_root, id);
}
