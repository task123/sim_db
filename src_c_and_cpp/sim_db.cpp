// Copyright (C) 2018 Håkon Austlid Taskén <hakon.tasken@gmail.com>
// Licensed under the MIT License.

#include "../include/sim_db.hpp"
#include <iostream>

int call_c_add_empty_sim(std::string path_proj_root) {
    return add_empty_sim(path_proj_root.c_str());
}

void call_c_delete_sim(std::string path_proj_root, int id) {
    delete_sim(path_proj_root.c_str(), id);
}

namespace sim_db {
Connection::Connection(int argc, char** argv, bool store_metadata) {
    if (store_metadata) {
        sim_db = sim_db_ctor(argc, argv);
    } else {
        sim_db = sim_db_ctor_no_metadata(argc, argv);
    }
}

Connection::Connection(std::string path_proj_root, int id,
                       bool store_metadata) {
    sim_db = sim_db_ctor_with_id(path_proj_root.c_str(), id, store_metadata);
}

std::string Connection::make_unique_subdir(std::string path_directory) {
    return std::string(
            sim_db_make_unique_subdir(sim_db, path_directory.c_str()));
}

void Connection::update_sha1_executables(
        std::vector<std::string> paths_executables) {
    char** string_vec = new char*[paths_executables.size()];
    for (size_t i = 0; i < paths_executables.size(); i++) {
        string_vec[i] = new char[paths_executables[i].size() + 1];
        strcpy(string_vec[i], paths_executables[i].c_str());
    }
    sim_db_update_sha1_executables(sim_db, string_vec,
                                   paths_executables.size());
    for (size_t i = 0; i < paths_executables.size(); i++) {
        delete[] string_vec[i];
    }
    delete[] string_vec;
}

bool Connection::column_exists(std::string column) {
    return sim_db_column_exists(sim_db, column.c_str());
}

int Connection::get_id() { return sim_db_get_id(sim_db); }

std::string Connection::get_path_proj_root() {
    std::string path_proj_root(sim_db_get_path_proj_root(sim_db));
    return path_proj_root;
}

Connection::~Connection() { sim_db_dtor(sim_db); }

int add_empty_sim(std::string path_proj_root) {
    return call_c_add_empty_sim(path_proj_root.c_str());
}

void delete_sim(std::string path_proj_root, int id) {
    call_c_delete_sim(path_proj_root.c_str(), id);
}

}  // namespace sim_db
