/// Testing 'sim_db' for C, that is 'sim_db.h' and 'sim_db.c'.
///
/// Read in parameters from database, write parameters to database, make unique
/// subdirectory for results and save 'results.txt' in this directory.

// Copyright (C) 2018 Håkon Austlid Taskén <hakon.tasken@gmail.com>
// Licensed under the MIT License.

#include <unistd.h>
#include <cstring>
#include <fstream>
#include <iostream>
#include "sim_db.hpp"

int main(int argc, char** argv) {
    sim_db::Connection sim_db(argc, argv);

    int param1 = sim_db.read<int>("param1");
    std::cout << param1 << std::endl;
    sim_db.write<int>("new_param1", param1);
    std::cout << sim_db.read<int>("new_param1") << std::endl;

    double param2 = sim_db.read<double>("param2");
    std::cout << param2 << std::endl;
    sim_db.write<double>("new_param2", param2);
    std::cout << sim_db.read<double>("new_param2") << std::endl;

    std::string param3 = sim_db.read<std::string>("param3");
    std::cout << param3 << std::endl;
    sim_db.write<std::string>("new_param3", param3);
    std::cout << sim_db.read<std::string>("new_param3") << std::endl;

    bool param4 = sim_db.read<bool>("param4");
    std::cout << param4 << std::endl;
    sim_db.write<bool>("new_param4", param4);
    std::cout << sim_db.read<bool>("new_param4") << std::endl;

    std::vector<int> param5 = sim_db.read<std::vector<int> >("param5");
    for (int i = 0; i < param5.size(); i++) {
        std::cout << param5[i] << std::endl;
    }
    sim_db.write<std::vector<int> >("new_param5", param5);
    for (int i = 0; i < param5.size(); i++) {
        std::cout << param5[i] << std::endl;
    }

    std::vector<double> param6 = sim_db.read<std::vector<double> >("param6");
    for (int i = 0; i < param6.size(); i++) {
        std::cout << param6[i] << std::endl;
    }
    sim_db.write<std::vector<double> >("new_param6", param6);
    for (int i = 0; i < param6.size(); i++) {
        std::cout << param6[i] << std::endl;
    }

    std::vector<std::string> param7 =
            sim_db.read<std::vector<std::string> >("param7");
    for (int i = 0; i < param7.size(); i++) {
        std::cout << param7[i] << std::endl;
    }
    sim_db.write<std::vector<std::string> >("new_param7", param7);
    for (int i = 0; i < param7.size(); i++) {
        std::cout << param7[i] << std::endl;
    }

    std::vector<bool> param8 = sim_db.read<std::vector<bool> >("param8");
    for (int i = 0; i < param8.size(); i++) {
        std::cout << param8[i] << std::endl;
    }
    sim_db.write<std::vector<bool> >("new_param8", param8);
    for (int i = 0; i < param8.size(); i++) {
        std::cout << param8[i] << std::endl;
    }

    // Get full path to result directory.
    char cwd[4097];
    getcwd(cwd, 4096);
    std::string path_res_dir = cwd + std::string("/") + __FILE__;
    path_res_dir.erase(path_res_dir.find_last_of('/'), path_res_dir.size());
    path_res_dir += "/results";

    // Make unique subdirectory in results/.
    std::string filename_result =
            sim_db.make_unique_subdir("test/results/") + "/results.txt";

    // Save param6 to file in this unique subdirectory.
    std::ofstream result_file;
    result_file.open(filename_result);
    for (int i = 0; i < param6.size(); i++) {
        result_file << param6[i] << std::endl;
    }
}
