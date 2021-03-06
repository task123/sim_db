/// Testing 'sim_db' for C++, that is 'sim_db.hpp' and 'sim_db.cpp'.
///
/// Read in parameters from database, write parameters to database, make unique
/// subdirectory for results and save 'results.txt' in this directory.

// Copyright (C) 2018-2019 Håkon Austlid Taskén <hakon.tasken@gmail.com>
// Licensed under the MIT License.

#include <unistd.h>
#include <cstring>
#include <fstream>
#include <iostream>
#include "sim_db.hpp"

int main(int argc, char** argv) {
    bool store_metadata = true;
    for (int i = 0; i < argc; i++) {
        if (static_cast<std::string>(argv[i]) == "no_metadata") {
            store_metadata = false;
        }
    }

    std::cout << SIM_DB_VERSION << std::endl;

    sim_db::Connection sim_db(argc, argv, store_metadata);

    int param1 = sim_db.read<int>("test_param1");
    std::cout << param1 << std::endl;
    sim_db.write<int>("new_test_param1", param1);
    std::cout << sim_db.read<int>("new_test_param1") << std::endl;

    double param2 = sim_db.read<double>("test_param2");
    std::cout << param2 << std::endl;
    sim_db.write<double>("new_test_param2", param2);
    std::cout << sim_db.read<double>("new_test_param2") << std::endl;

    std::string param3 = sim_db.read<std::string>("test_param3");
    std::cout << param3 << std::endl;
    sim_db.write<std::string>("new_test_param3", param3);
    std::cout << sim_db.read<std::string>("new_test_param3") << std::endl;

    bool param4 = sim_db.read<bool>("test_param4");
    std::cout << param4 << std::endl;
    sim_db.write<bool>("new_test_param4", param4);
    std::cout << sim_db.read<bool>("new_test_param4") << std::endl;

    std::vector<int> param5 = sim_db.read<std::vector<int> >("test_param5");
    for (size_t i = 0; i < param5.size(); i++) {
        std::cout << param5[i] << std::endl;
    }
    sim_db.write<std::vector<int> >("new_test_param5", param5);
    for (size_t i = 0; i < param5.size(); i++) {
        std::cout << param5[i] << std::endl;
    }

    std::vector<double> param6 =
            sim_db.read<std::vector<double> >("test_param6");
    for (size_t i = 0; i < param6.size(); i++) {
        std::cout << param6[i] << std::endl;
    }
    sim_db.write<std::vector<double> >("new_test_param6", param6);
    for (size_t i = 0; i < param6.size(); i++) {
        std::cout << param6[i] << std::endl;
    }

    std::vector<std::string> param7 =
            sim_db.read<std::vector<std::string> >("test_param7");
    for (size_t i = 0; i < param7.size(); i++) {
        std::cout << param7[i] << std::endl;
    }
    sim_db.write<std::vector<std::string> >("new_test_param7", param7);
    for (size_t i = 0; i < param7.size(); i++) {
        std::cout << param7[i] << std::endl;
    }

    std::vector<bool> param8 = sim_db.read<std::vector<bool> >("test_param8");
    for (size_t i = 0; i < param8.size(); i++) {
        std::cout << param8[i] << std::endl;
    }
    sim_db.write<std::vector<bool> >("new_test_param8", param8);
    for (size_t i = 0; i < param8.size(); i++) {
        std::cout << param8[i] << std::endl;
    }

    int param9 = sim_db.read<int>("test_param9");
    std::cout << param9 << std::endl;
    sim_db.write<int>("new_test_param9", param9);
    std::cout << sim_db.read<int>("new_test_param9") << std::endl;

    int param10 = sim_db.read<int>("test_param10");
    std::cout << param10 << std::endl;
    sim_db.write<int>("new_test_param10", param10);
    std::cout << sim_db.read<int>("new_test_param10") << std::endl;

    std::cout << sim_db.is_empty("test_param11") << std::endl;
    sim_db.set_empty("test_param11");
    std::cout << sim_db.is_empty("test_param11") << std::endl;

    if (store_metadata) {
        // Make unique subdirectory in results/.
        std::string filename_result =
                sim_db.unique_results_dir("root/tests/results/")
                + "/results.txt";

        // Save param6 to file in this unique subdirectory.
        std::ofstream result_file;
        result_file.open(filename_result.c_str());
        for (size_t i = 0; i < param6.size(); i++) {
            result_file << param6[i] << std::endl;
        }
    }

    std::cout << sim_db.column_exists("test_param1") << std::endl;
    std::cout << sim_db.column_exists("test_column_does_not_exists")
              << std::endl;
    try {
        sim_db.read<int>("test_column_does_not_exists");
    } catch (std::invalid_argument&) {
        std::cout << "threw exception" << std::endl;
    }

    std::string path_proj_root = sim_db.get_path_proj_root();

    sim_db::Connection sim_db_2 = sim_db::add_empty_sim(false);
    std::cout << sim_db_2.get_id() << std::endl;

    sim_db_2.write<int>("test_param1", 7);
    param1 = sim_db_2.read<int>("test_param1");
    std::cout << param1 << std::endl;

    sim_db_2.delete_from_database();
}
