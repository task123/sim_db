/// @file sim_db.h
/// @brief All C functions to use ```sim_db```.

// Copyright (C) 2018 Håkon Austlid Taskén <hakon.tasken@gmail.com>
// Licensed under the MIT License.

#ifndef SIM_DB_H
#define SIM_DB_H
#include <stdbool.h>
#include <stdlib.h>  // To get definition of size_t.

typedef struct SimDB SimDB;

/// @brief Initialize SimDB with command line argument ```--id ID```, where
/// ```ID``` is the id of the simulation parameters in the ```sim_db```
/// database.
///
/// The following metadata is also added to database: 'time_started',
/// 'git_hash', 'git_commit', 'git_diff_stat', 'git_diff' and
/// 'sha1_executables'.
/// sim_db_dtor() must be called to clean up.
/// @param argc Length of \p argv.
/// @param argv Array of command line arguments containg ```--id ID```.
SimDB* sim_db_ctor(int argc, char** argv);

/// Initialize SimDB with id of the simulation parameters in the
/// ```sim_db``` database.
/// Metadata is also added to database. (sha1 is only added if in a git
/// project.) sim_db_dtor() must be called to clean up.
SimDB* sim_db_ctor_with_id(const char* path_sim_db, int id);

/// Read parameter from the database.
/// @param self Return value of fn sim_db_ctor or fn sim_db_ctor_with_id.
/// @param column Name of the parameter and column in the database.
int sim_db_read_int(SimDB* self, const char* column);

/// Read parameter from the database.
/// @param self Return value of fn sim_db_ctor or fn sim_db_ctor_with_id.
/// @param column Name of the parameter and column in the database.
double sim_db_read_double(SimDB* self, const char* column);

/// Read parameter from the database.
/// Clean up is done by sim_db_dtor(), so don't free \p string.
/// @param self Return value of fn sim_db_ctor or fn sim_db_ctor_with_id.
/// @param column Name of the parameter and column in the database.
/// @param string Value from database is returned through this pointer. Don't
///               free \p string as clean up done by sim_db_dtor().
/// @return The length of \p string.
char* sim_db_read_string(SimDB* self, const char* column);

/// Read parameter from the database.
/// @param self Return value of fn sim_db_ctor or fn sim_db_ctor_with_id.
/// @param column Name of the parameter and column in the database.
bool sim_db_read_bool(SimDB* self, const char* column);

typedef struct SimDBIntVec {
    size_t size;
    int* array;
} SimDBIntVec;

/// Read parameter from the database.
/// @param self Return value of fn sim_db_ctor or fn sim_db_ctor_with_id.
/// @param column Name of the parameter and column in the database.
SimDBIntVec sim_db_read_int_vec(SimDB* self, const char* column);

typedef struct SimDBDoubleVec {
    size_t size;
    double* array;
} SimDBDoubleVec;

/// Read parameter from the database.
/// @param self Return value of fn sim_db_ctor or fn sim_db_ctor_with_id.
/// @param column Name of the parameter and column in the database.
SimDBDoubleVec sim_db_read_double_vec(SimDB* self, const char* column);

typedef struct SimDBStringVec {
    size_t size;
    char** array;
} SimDBStringVec;

/// Read parameter from the database.
/// @param self Return value of fn sim_db_ctor or fn sim_db_ctor_with_id.
/// @param column Name of the parameter and column in the database.
SimDBStringVec sim_db_read_string_vec(SimDB* self, const char* column);

typedef struct SimDBBoolVec {
    size_t size;
    bool* array;
} SimDBBoolVec;

/// Read parameter from the database.
/// @param self Return value of fn sim_db_ctor or fn sim_db_ctor_with_id.
/// @param column Name of the parameter and column in the database.
SimDBBoolVec sim_db_read_bool_vec(SimDB* self, const char* column);

/// Write \p value to database.
/// @param self Return value of sim_db_ctor() or sim_db_ctor_with_id().
/// @param column Name of the column in the database to write to.
void sim_db_write_int(SimDB* self, const char* column, int value);

/// Write \p value to database.
/// @param self Return value of sim_db_ctor() or sim_db_ctor_with_id().
/// @param column Name of the column in the database to write to.
void sim_db_write_double(SimDB* self, const char* column, double value);

/// Write \p value to database.
/// @param self Return value of sim_db_ctor() or sim_db_ctor_with_id().
/// @param column Name of the column in the database to write to.
void sim_db_write_string(SimDB* self, const char* column, const char* value);

/// Write \p value to database.
/// @param self Return value of sim_db_ctor() or sim_db_ctor_with_id().
/// @param column Name of the column in the database to write to.
void sim_db_write_bool(SimDB* self, const char* column, bool value);

/// Write \p arr to database.
/// @param self Return value of sim_db_ctor() or sim_db_ctor_with_id().
/// @param column Name of the column in the database to write to.
/// @param arr Array to be written to simulation database.
/// @param len Length of \p arr.
void sim_db_write_int_array(SimDB* self, const char* column, int* arr,
                            size_t len);

/// Write \p arr to database.
/// @param self Return value of sim_db_ctor() or sim_db_ctor_with_id().
/// @param column Name of the column in the database to write to.
/// @param arr Array to be written to simulation database.
/// @param len Length of \p arr.
void sim_db_write_double_array(SimDB* self, const char* column, double* arr,
                               size_t len);

/// Write \p arr to database.
/// @param self Return value of sim_db_ctor() or sim_db_ctor_with_id().
/// @param column Name of the column in the database to write to.
/// @param arr Array to be written to simulation database.
/// @param len Length of \p arr.
void sim_db_write_string_array(SimDB* self, const char* column, char** arr,
                               size_t len);

/// Write \p arr to database.
/// @param self Return value of sim_db_ctor() or sim_db_ctor_with_id().
/// @param column Name of the column in the database to write to.
/// @param arr Array to be written to simulation database.
/// @param len Length of \p arr.
void sim_db_write_bool_array(SimDB* self, const char* column, bool* arr,
                             size_t len);

/// Make unique subdirectory of \p name_result_directory.
/// This new subdirectory is intended for storing results from the simulation.
/// @param name_result_directory Path to a directory.
/// @return Path to new subdirectory.
char* sim_db_make_unique_subdir_rel_path(SimDB* self,
                                         const char* rel_path_to_result_dir);

char* sim_db_make_unique_subdir_abs_path(SimDB* self,
                                         const char* abs_path_to_result_dir);

/// Save the sha1 hash of the file \p paths_executables to the database.
/// @param self Return value of sim_db_ctor() or sim_db_ctor_with_id().
/// @param paths_executables Path to executable file.
/// @param len Length of \p paths_executables.
void sim_db_update_sha1_executables(SimDB* self, char** paths_executables,
                                    size_t len);

/// Clean up \typedef SimDB.
/// Add metadate for 'used_walltime' to database and update 'status' to
/// 'finished'.
/// @param self Return value of sim_db_ctor() or sim_db_ctor_with_id().
void sim_db_dtor(SimDB* self);

#endif
