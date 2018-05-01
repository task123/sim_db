// Copyright (C) 2018 Håkon Austlid Taskén <hakon.tasken@gmail.com>
// Licensed under the MIT License.

#include "sim_db.hpp"

namespace sim_db {
Connection::Connection(int argc, char** argv) {
    sim_db = sim_db_ctor(argc, argv);
}

Connection::Connection(int id) { sim_db = sim_db_ctor_with_id(id); }

std::string Connection::make_subdir_result(std::string path_result_directory) {
    std::string str(
            sim_db_make_subdir_result(sim_db, path_result_directory.c_str()));
    return str;
}

void Connection::update_sha1_executables(
        std::vector<std::string> paths_executables) {
    char** string_vec = new char*[paths_executables.size()];
    for (int i = 0; i < paths_executables.size(); i++) {
        string_vec[i] = new char[paths_executables[i].size() + 1];
        strcpy(string_vec[i], paths_executables[i].c_str());
    }
    sim_db_update_sha1_executables(sim_db, string_vec,
                                   paths_executables.size());
    for (int i = 0; i < paths_executables.size(); i++) {
        delete[] string_vec[i];
    }
    delete[] string_vec;
}

Connection::~Connection() { sim_db_dtor(sim_db); }

}  // namespace sim_db
