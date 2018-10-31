// Copyright (C) 2018 Håkon Austlid Taskén <hakon.tasken@gmail.com>
// Licensed under the MIT License.

#include "../include/sim_db.hpp"
#include <iostream>

int call_c_add_empty_sim(std::string path_sim_db) {
    return add_empty_sim(path_sim_db.c_str());
}

void call_c_delete_sim(std::string path_sim_db, int id) {
    delete_sim(path_sim_db.c_str(), id);
}

namespace sim_db {
Connection::Connection(int argc, char** argv, bool store_metadata) {
    if (store_metadata) {
        sim_db = sim_db_ctor(argc, argv);
    } else {
        sim_db = sim_db_ctor_no_metadata(argc, argv);
    }
}

Connection::Connection(std::string path_sim_db, int id, bool store_metadata) {
    sim_db = sim_db_ctor_with_id(path_sim_db.c_str(), id, store_metadata);
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

int Connection::get_id() { return sim_db_get_id(sim_db); }

std::string Connection::get_path() {
    std::string path_sim_db(sim_db_get_path(sim_db));
    return path_sim_db;
}

Connection::~Connection() { sim_db_dtor(sim_db); }

int add_empty_sim(std::string path_sim_db) {
    return call_c_add_empty_sim(path_sim_db.c_str());
}

void delete_sim(std::string path_sim_db, int id) {
    call_c_delete_sim(path_sim_db.c_str(), id);
}

}  // namespace sim_db
