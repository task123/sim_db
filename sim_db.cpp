// Copyright (C) 2018 Håkon Austlid Taskén <hakon.tasken@gmail.com>
// Licensed under the MIT License.

#include "sim_db.hpp"

namespace sim_db {
Connection::Connection(int argc, char** argv) {
    sim_db = sim_db_ctor(argc, argv);
}

Connection::Connection(std::string path_sim_db, int id) {
    sim_db = sim_db_ctor_with_id(path_sim_db.c_str(), id);
}

std::string Connection::make_unique_subdir(std::string path_directory,
                                           bool is_path_relative) {
    std::string name_subdir;
    if (is_path_relative) {
        name_subdir = std::string(sim_db_make_unique_subdir_rel_path(
                sim_db, path_directory.c_str()));
    } else {
        name_subdir = std::string(sim_db_make_unique_subdir_abs_path(
                sim_db, path_directory.c_str()));
    }
    return name_subdir;
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
