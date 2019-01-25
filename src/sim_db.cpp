// Copyright (C) 2018, 2019 Håkon Austlid Taskén <hakon.tasken@gmail.com>
// Licensed under the MIT License.

#include "sim_db.hpp"
#include <iostream>

namespace sim_db {
Connection::Connection(int argc, char** argv, bool store_metadata) {
    if (store_metadata) {
        sim_db = sim_db_ctor(argc, argv);
    } else {
        sim_db = sim_db_ctor_no_metadata(argc, argv);
    }
    sim_db_allow_timeouts(sim_db, true);
}

Connection::Connection(int id, bool store_metadata) {
    sim_db = sim_db_ctor_with_id(id, store_metadata);
    sim_db_allow_timeouts(sim_db, true);
}

Connection::Connection(std::string path_proj_root, int id,
                       bool store_metadata) {
    sim_db = sim_db_ctor_without_search(path_proj_root.c_str(), id,
                                        store_metadata);
    sim_db_allow_timeouts(sim_db, true);
}

std::string Connection::unique_results_dir(std::string path_directory) {
    return std::string(
            sim_db_unique_results_dir(sim_db, path_directory.c_str()));
}

void Connection::update_sha1_executables(
        std::vector<std::string> paths_executables, bool only_if_empty) {
    char** string_vec = new char*[paths_executables.size()];
    for (size_t i = 0; i < paths_executables.size(); i++) {
        string_vec[i] = new char[paths_executables[i].size() + 1];
        strcpy(string_vec[i], paths_executables[i].c_str());
    }
    sim_db_update_sha1_executables(sim_db, string_vec, paths_executables.size(),
                                   only_if_empty);
    for (size_t i = 0; i < paths_executables.size(); i++) {
        delete[] string_vec[i];
    }
    delete[] string_vec;
    if (sim_db_have_timed_out(sim_db)) {
        throw TimeoutError();
    }
}

bool Connection::column_exists(std::string column) {
    bool exists = sim_db_column_exists(sim_db, column.c_str());
    if (sim_db_have_timed_out(sim_db)) {
        throw TimeoutError();
    }
    return exists;
}

bool Connection::is_empty(std::string column) {
    return sim_db_is_empty(sim_db, column.c_str());
}

void Connection::set_empty(std::string column) {
    sim_db_set_empty(sim_db, column.c_str());
    if (sim_db_have_timed_out(sim_db)) {
        throw TimeoutError();
    }
}

int Connection::get_id() { return sim_db_get_id(sim_db); }

std::string Connection::get_path_proj_root() {
    std::string path_proj_root(sim_db_get_path_proj_root(sim_db));
    return path_proj_root;
}

void Connection::delete_from_database() {
    sim_db_delete_from_database(sim_db);
    if (sim_db_have_timed_out(sim_db)) {
        throw TimeoutError();
    }
}

Connection::~Connection() { sim_db_dtor(sim_db); }

Connection add_empty_sim(bool store_metadata) {
    SimDB* sim_db = sim_db_add_empty_sim(store_metadata);
    if (sim_db_have_timed_out(sim_db)) {
        sim_db_dtor(sim_db);
        throw TimeoutError();
    }
    int id = sim_db_get_id(sim_db);
    std::string path_proj_root(sim_db_get_path_proj_root(sim_db));
    sim_db_dtor(sim_db);
    return Connection(path_proj_root, id, store_metadata);
}

Connection add_empty_sim(std::string path_proj_root, bool store_metadata) {
    SimDB* sim_db = sim_db_add_empty_sim_without_search(path_proj_root.c_str(),
                                                        store_metadata);
    if (sim_db_have_timed_out(sim_db)) {
        sim_db_dtor(sim_db);
        throw TimeoutError();
    }
    int id = sim_db_get_id(sim_db);
    sim_db_dtor(sim_db);
    return Connection(path_proj_root, id, store_metadata);
}

}  // namespace sim_db
