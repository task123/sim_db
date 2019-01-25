// Copyright (C) 2018-2019 Håkon Austlid Taskén <hakon.tasken@gmail.com>
// Licensed under the MIT License.

#ifndef SIM_DB_HPP
#define SIM_DB_HPP
#pragma once

// Outside namespace to make documentation generation work.
extern "C" {
#include "sim_db.h"
}

#include <cstring>
#include <stdexcept>
#include <string>
#include <vector>

namespace sim_db {

/// To interact with the **sim_db** database.
//
/// For an actuall simulation it should be initialised at the very start of the
/// simulation (with 'store_metadata' set to True) in a scope that last the
/// entirety of the simulation. This must be done to add the corrrect metadata.
///
/// For multithreading/multiprocessing each thread/process MUST have its
/// own connection (instance of this class).
///
class Connection {
public:
    /// Connect to the **sim_db** database.
    //
    /// @param argc Length of \p argv.
    /// @param argv Array of command line arguments containg ```--id
    /// 'ID'``` and optionally ```--path_proj_root 'PATH'```. *PATH* is the root
    /// directory of the project, where *.sim_db/* is located. If not passed,
    /// the current working directory and its parent directories will be
    /// searched until *.sim_db/* is found.
    /// @param store_metadata Stores metadata to database if true. Set
    /// to 'false' for postprocessing (e.g. visualization) of data from
    /// simulation.
    Connection(int argc, char** argv, bool store_metadata = true);

    /// Connect to the **sim_db** database.
    //
    /// Will search the currecy working directory and its parent directories
    /// until *.sim_db/* is found.
    ///
    /// @param id ID number of the simulation paramters in the **sim_db**
    /// database.
    /// @param store_metadata Stores metadata to database if true. Set to
    /// 'false' for postprocessing (e.g. visualization) of data from simulation.
    Connection(int id, bool store_metadata = true);

    /// Connect to the **sim_db** database.
    //
    /// @param path_proj_root Path to the root directory of the project, where
    /// *.sim_db/* is located.
    /// @param id ID number of the simulation paramters in the **sim_db**
    /// database.
    /// @param store_metadata Stores metadata to database if true. Set to
    /// 'false' for postprocessing (e.g. visualization) of data from simulation.
    Connection(std::string path_proj_root, int id, bool store_metadata = true);

    /// Read parameter from database.
    //
    /// @param column Name of the parameter and column in the database.
    /// @return Parameter read from database.
    /// @exception std::invalid_argument \p column not a column in the database.
    /// @exception sim_db::TimeoutError Waited more than 5 seconds to read from
    /// the database, because other threads/processes are busy writing to it.
    /// Way too much concurrent writing is done and it indicates an design error
    /// in the user program.
    template <typename T>
    T read(std::string column);

    /// Write \p value to database.
    //
    /// @param column Name of the parameter and column in the database.
    /// @param value To be written to database.
    /// @param only_if_empty If True, it will only write to the database if the
    /// simulation's entry under 'column' is empty. Will avoid potential
    /// timeouts for concurrect applications.
    /// @exception sim_db::TimeoutError Waited more than 5 seconds to write to
    /// the database because other threads/processes are busy writing to it.
    /// Way too much concurrent writing is done and indicates an design error
    /// in the user program.
    template <typename T>
    void write(std::string column, T value, bool only_if_empty = false);

    /// Get path to subdirectory in \p path_directory unique to simulation.
    //
    /// The subdirectory will be named 'date_time_name_id' and is intended to
    /// store results in. If 'results_dir' in the database is empty, a new and
    /// unique directory is created and the path stored in 'results_dir'.
    /// Otherwise the path in 'results_dir' is just returned.
    ///
    /// @param path_directory Path to where the new directory is created. If it
    /// starts with 'root/', that part will be replaced with the full path to
    /// the root directory of the project.
    /// @return Path to new subdirectory.
    std::string unique_results_dir(std::string path_directory);

    /// Return true if \p column is a column in the database.
    //
    /// @exception sim_db::TimeoutError Waited more than 5 seconds to write to
    /// the database because other threads/processes are busy writing to it.
    /// Way too much concurrent writing is done and indicates an design error
    // / in the user program.
    bool column_exists(std::string column);

    /// Return true if entry for under \p column in database is empty.
    bool is_empty(std::string column);

    /// Set entry in database under \p column to empty.
    void set_empty(std::string column);

    /// Return ID number of simulation in the database that is connected.
    int get_id();

    /// Return path to root directory of the project, where *.sim_db/* is
    /// located.
    std::string get_path_proj_root();

    /// Save the sha1 hash of the file \p paths_executables to the database.
    //
    /// @param paths_executables Paths to executable files.
    /// @param only_if_empty If True, it will only write to the database if the
    /// simulation's entry under 'column' is empty. Will avoid potential
    /// timeouts for concurrect applications.
    /// @exception sim_db::TimeoutError Waited more than 5 seconds to write to
    /// the database because other threads/processes are busy writing to it.
    /// Way too much concurrent writing is done and indicates an design error
    /// in the user program.
    void update_sha1_executables(std::vector<std::string> paths_executables,
                                 bool only_if_empty = false);

    /// Delete simulation from database.
    void delete_from_database();

    ~Connection();

private:
    struct SimDB* sim_db;
};

/// Add empty simulation to database and return Connection connected to it.
//
/// @param store_metadata Stores metadata to database if true. Set to
/// 'false' for postprocessing (e.g. visualization) of data from simulation.
/// @exception sim_db::TimeoutError Waited more than 5 seconds to write to the
/// database because other threads/processes are busy writing to it. Way too
/// much concurrent writing is done and indicates an design error in the user
/// program.
Connection add_empty_sim(bool store_metadata = false);

/// Add empty simulation to database and return Connection connected to it.
//
/// @param path_proj_root Path to the root directory of the project, where
/// *.sim_db/* is located.
/// @param store_metadata Stores metadata to database if true. Set to
/// 'false' for postprocessing (e.g. visualization) of data from simulation.
/// @return Connection to the added simulation.
/// @exception sim_db::TimeoutError Waited more than 5 seconds to write to the
/// database because other threads/processes are busy writing to it. Way too
/// much concurrent writing is done and indicates an design error in the user
/// program.
Connection add_empty_sim(std::string path_proj_root,
                         bool store_metadata = false);

class TimeoutError : public std::runtime_error {
public:
    TimeoutError() : std::runtime_error("sim_db database is busy."){};
};

template <typename T>
class TemplateSpecializationHelper {};

template <>
class TemplateSpecializationHelper<int> {
    static int read(struct SimDB* sim_db, std::string column) {
        return sim_db_read_int(sim_db, column.c_str());
    }
    static void write(struct SimDB* sim_db, std::string column, int value,
                      bool only_if_empty) {
        sim_db_write_int(sim_db, column.c_str(), value, only_if_empty);
    }
    friend class Connection;
};

template <>
class TemplateSpecializationHelper<double> {
    static double read(struct SimDB* sim_db, std::string column) {
        return sim_db_read_double(sim_db, column.c_str());
    }
    static void write(struct SimDB* sim_db, std::string column, double value,
                      bool only_if_empty) {
        sim_db_write_double(sim_db, column.c_str(), value, only_if_empty);
    }
    friend class Connection;
};

template <>
class TemplateSpecializationHelper<std::string> {
    static std::string read(struct SimDB* sim_db, std::string column) {
        std::string str(sim_db_read_string(sim_db, column.c_str()));
        return str;
    }
    static void write(struct SimDB* sim_db, std::string column,
                      std::string value, bool only_if_empty) {
        sim_db_write_string(sim_db, column.c_str(), value.c_str(),
                            only_if_empty);
    }
    friend class Connection;
};

template <>
class TemplateSpecializationHelper<bool> {
    static bool read(struct SimDB* sim_db, std::string column) {
        return sim_db_read_bool(sim_db, column.c_str());
    }
    static void write(struct SimDB* sim_db, std::string column, bool value,
                      bool only_if_empty) {
        sim_db_write_bool(sim_db, column.c_str(), value, only_if_empty);
    }
    friend class Connection;
};

template <>
class TemplateSpecializationHelper<std::vector<int> > {
    static std::vector<int> read(struct SimDB* sim_db, std::string column) {
        SimDBIntVec i_vec = sim_db_read_int_vec(sim_db, column.c_str());
        std::vector<int> vector(i_vec.array, i_vec.array + i_vec.size);
        return vector;
    }
    static void write(struct SimDB* sim_db, std::string column,
                      std::vector<int> value, bool only_if_empty) {
        sim_db_write_int_array(sim_db, column.c_str(), &value[0], value.size(),
                               only_if_empty);
    }
    friend class Connection;
};

template <>
class TemplateSpecializationHelper<std::vector<double> > {
    static std::vector<double> read(struct SimDB* sim_db, std::string column) {
        SimDBDoubleVec d_vec = sim_db_read_double_vec(sim_db, column.c_str());
        std::vector<double> vector(d_vec.array, d_vec.array + d_vec.size);
        return vector;
    }
    static void write(struct SimDB* sim_db, std::string column,
                      std::vector<double> value, bool only_if_empty) {
        sim_db_write_double_array(sim_db, column.c_str(), &value[0],
                                  value.size(), only_if_empty);
    }
    friend class Connection;
};

template <>
class TemplateSpecializationHelper<std::vector<std::string> > {
    static std::vector<std::string> read(struct SimDB* sim_db,
                                         std::string column) {
        SimDBStringVec s_vec = sim_db_read_string_vec(sim_db, column.c_str());
        std::vector<std::string> vector;
        for (size_t i = 0; i < s_vec.size; i++) {
            std::string str(s_vec.array[i]);
            vector.push_back(str);
        }
        return vector;
    }
    static void write(struct SimDB* sim_db, std::string column,
                      std::vector<std::string> value, bool only_if_empty) {
        char** string_vec = new char*[value.size()];
        for (size_t i = 0; i < value.size(); i++) {
            string_vec[i] = new char[value[i].size() + 1];
            strcpy(string_vec[i], value[i].c_str());
        }
        sim_db_write_string_array(sim_db, column.c_str(), string_vec,
                                  value.size(), only_if_empty);
        for (size_t i = 0; i < value.size(); i++) {
            delete[] string_vec[i];
        }
        delete[] string_vec;
    }
    friend class Connection;
};

template <>
class TemplateSpecializationHelper<std::vector<bool> > {
    static std::vector<bool> read(struct SimDB* sim_db, std::string column) {
        SimDBBoolVec b_vec = sim_db_read_bool_vec(sim_db, column.c_str());
        std::vector<bool> vector(b_vec.array, b_vec.array + b_vec.size);
        return vector;
    }
    static void write(struct SimDB* sim_db, std::string column,
                      std::vector<bool> value, bool only_if_empty) {
        bool* bool_vec = new bool[value.size()];
        for (size_t i = 0; i < value.size(); i++) {
            bool_vec[i] = value[i];
        }
        sim_db_write_bool_array(sim_db, column.c_str(), bool_vec, value.size(),
                                only_if_empty);
        delete[] bool_vec;
    }
    friend class Connection;
};

template <typename T>
T Connection::read(std::string column) {
    if (!sim_db_column_exists(sim_db, column.c_str())) {
        throw std::invalid_argument(
                "Column does NOT exists in the 'sim_db' database.");
    }
    return TemplateSpecializationHelper<T>::read(sim_db, column);
    if (sim_db_have_timed_out(sim_db)) {
        throw TimeoutError();
    }
};

template <typename T>
void Connection::write(std::string column, T value, bool only_if_empty) {
    TemplateSpecializationHelper<T>::write(sim_db, column, value,
                                           only_if_empty);
    if (sim_db_have_timed_out(sim_db)) {
        throw TimeoutError();
    }
};

}  // namespace sim_db
#endif
