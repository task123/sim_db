// Copyright (C) 2018 Håkon Austlid Taskén <hakon.tasken@gmail.com>
// Licensed under the MIT License.

#ifndef SIM_DB_HPP
#define SIM_DB_HPP

extern "C" {
#include "sim_db.h"
}

#include <cstring>
#include <stdexcept>
#include <string>
#include <vector>

namespace sim_db {

/// To interact with the 'sim_db' database.
class Connection {
public:
    /// To the 'sim_db' database.
    /// @param argc Length of \p argv.
    /// @param argv Array of command line arguments containg ```--id ID```.
    /// @param store_metadata Store metadata to database if true. Set to 'false'
    ///         for postprocessing (visualization) of data from simulation.
    Connection(int argc, char** argv, bool store_metadata = true);

    /// To the 'sim_db' database.
    Connection(std::string path_sim_db, int id, bool store_metadata = true);

    /// Read parameter from database.
    template <typename T>
    T read(std::string column);

    template <typename T>
    void write(std::string column, T value);

    std::string make_unique_subdir(std::string path_directory,
                                   bool is_path_relative = true);

    void update_sha1_executables(std::vector<std::string> paths_executables);

    ~Connection();

private:
    struct SimDB* sim_db;
};

template <typename T>
class TemplateSpecializationHelper {};

template <>
class TemplateSpecializationHelper<int> {
    static int read(struct SimDB* sim_db, std::string column) {
        return sim_db_read_int(sim_db, column.c_str());
    }
    static void write(struct SimDB* sim_db, std::string column, int value) {
        sim_db_write_int(sim_db, column.c_str(), value);
    }
    friend class Connection;
};

template <>
class TemplateSpecializationHelper<double> {
    static double read(struct SimDB* sim_db, std::string column) {
        return sim_db_read_double(sim_db, column.c_str());
    }
    static void write(struct SimDB* sim_db, std::string column, double value) {
        sim_db_write_double(sim_db, column.c_str(), value);
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
                      std::string value) {
        sim_db_write_string(sim_db, column.c_str(), value.c_str());
    }
    friend class Connection;
};

template <>
class TemplateSpecializationHelper<bool> {
    static bool read(struct SimDB* sim_db, std::string column) {
        return sim_db_read_bool(sim_db, column.c_str());
    }
    static void write(struct SimDB* sim_db, std::string column, bool value) {
        sim_db_write_bool(sim_db, column.c_str(), value);
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
                      std::vector<int> value) {
        sim_db_write_int_array(sim_db, column.c_str(), &value[0], value.size());
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
                      std::vector<double> value) {
        sim_db_write_double_array(sim_db, column.c_str(), &value[0],
                                  value.size());
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
                      std::vector<std::string> value) {
        char** string_vec = new char*[value.size()];
        for (size_t i = 0; i < value.size(); i++) {
            string_vec[i] = new char[value[i].size() + 1];
            strcpy(string_vec[i], value[i].c_str());
        }
        sim_db_write_string_array(sim_db, column.c_str(), string_vec,
                                  value.size());
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
                      std::vector<bool> value) {
        bool* bool_vec = new bool[value.size()];
        for (size_t i = 0; i < value.size(); i++) {
            bool_vec[i] = value[i];
        }
        sim_db_write_bool_array(sim_db, column.c_str(), bool_vec, value.size());
        delete[] bool_vec;
    }
    friend class Connection;
};

template <typename T>
T Connection::read(std::string column) {
    return TemplateSpecializationHelper<T>::read(sim_db, column);
};

template <typename T>
void Connection::write(std::string column, T value) {
    TemplateSpecializationHelper<T>::write(sim_db, column, value);
};

}  // namespace sim_db
#endif
