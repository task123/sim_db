/// @file sim_db.h
/// @brief All C functions to use ```sim_db```.

// Copyright (C) 2018 Håkon Austlid Taskén <hakon.tasken@gmail.com>
// Licensed under the MIT License.

#ifndef SIM_DB_H
#define SIM_DB_H
#include <stdbool.h>
#include <stdlib.h>  // To get definition of size_t.

typedef struct SimDB SimDB;

/// Initialize SimDB and connect to the **sim_db** database.
//
/// {@link sim_db_dtor(SimDB*)} MUST be called to clean up.
/// @param argc Length of \p argv.
/// @param argv Array of command line arguments containing ```--id 'ID'``` and
/// optionally ```--path_proj_root 'PATH'```. *PATH* is the root directory of
/// the project, where *.sim_db/* is located. If not passed, the current working
/// directory and its parent directories will be searched until *.sim_db/* is
/// found.
SimDB* sim_db_ctor(int argc, char** argv);

/// Initialize SimDB and connect to the **sim_db** database.
//
/// No metadata store automatically, and only explicit calls will write to the
/// database.
///
/// {@link sim_db_dtor(SimDB*)} MUST be called to clean up.
/// @param argc Length of \p argv.
/// @param argv Array of command line arguments containing ```--id 'ID'``` and
/// optionally ```--path_proj_root 'PATH'```. *PATH* is the root directory of
/// the project, where *.sim_db/* is located. If not passed, the current working
/// directory and its parent directories will be searched until *.sim_db/* is
/// found.
SimDB* sim_db_ctor_no_metadata(int argc, char** argv);

/// Initialize SimDB and connect to the **sim_db** database.
//
/// {@link sim_db_dtor(SimDB*)} MUST be called to clean up.
/// @param path_proj_root Path to root directory of the project, where
/// *.sim_db/* is located.
/// @param id ID number of the simulation paramters in the **sim_db** database.
/// @param store_metadata Whether or not to store metadata automatically to the
/// database. (Recommended)
SimDB* sim_db_ctor_with_id(const char* path_proj_root, int id,
                           bool store_metadata);

/// Read parameter from the database.
//
/// @param self Return value of {@link sim_db_ctor()} or {@link
/// sim_db_ctor_with_id()}.
/// @param column Name of the parameter and column in the database.
/// @return Integer read from database.
int sim_db_read_int(SimDB* self, const char* column);

/// Read parameter from the database.
//
/// @param self Return value of {@link sim_db_ctor()} or {@link
/// sim_db_ctor_with_id()}.
/// @param column Name of the parameter and column in the database.
/// @return Double read from database.
double sim_db_read_double(SimDB* self, const char* column);

/// Read parameter from the database.
//
/// @param self Return value of {@link sim_db_ctor()} or {@link
/// sim_db_ctor_with_id()}.
/// @param column Name of the parameter and column in the database.
/// @return String read from database. Do NOT free the string, as {@link
/// sim_db_dtor()} will do that.
char* sim_db_read_string(SimDB* self, const char* column);

/// Read parameter from the database.
//
/// @param self Return value of {@link sim_db_ctor()} or {@link
/// sim_db_ctor_with_id()}.
/// @param column Name of the parameter and column in the database.
/// @return Bool read from database.
bool sim_db_read_bool(SimDB* self, const char* column);

/// Vector of integers
typedef struct SimDBIntVec {
    size_t size;  ///< Length of array
    int* array;   ///< Array of integers
} SimDBIntVec;

/// Read parameter from the database.
//
/// @param self Return value of {@link sim_db_ctor()} or {@link
/// sim_db_ctor_with_id()}.
/// @param column Name of the parameter and column in the database.
/// @return Vector of integers read from database. Do NOT free array as {@link
/// sim_db_dtor()} will do that.
SimDBIntVec sim_db_read_int_vec(SimDB* self, const char* column);

/// Vector of doubles
typedef struct SimDBDoubleVec {
    size_t size;    ///< Length of array
    double* array;  ///< Array of doubles
} SimDBDoubleVec;

/// Read parameter from the database.
//
/// @param self Return value of {@link sim_db_ctor()} or {@link
/// sim_db_ctor_with_id()}.
/// @param column Name of the parameter and column in the database.
/// @return Vector of doubles read from database. Do NOT free array as {@link
/// sim_db_dtor()} will do that.
SimDBDoubleVec sim_db_read_double_vec(SimDB* self, const char* column);

/// Vector of strings
typedef struct SimDBStringVec {
    size_t size;   ///< Length of array
    char** array;  ///< Array of strings
} SimDBStringVec;

/// Read parameter from the database.
//
/// @param self Return value of {@link sim_db_ctor()} or {@link
/// sim_db_ctor_with_id()}.
/// @param column Name of the parameter and column in the database.
/// @return Vector of strings read from database. Do NOT free array as {@link
/// sim_db_dtor()} will do that.
SimDBStringVec sim_db_read_string_vec(SimDB* self, const char* column);

/// Vector of booleans
typedef struct SimDBBoolVec {
    size_t size;  ///< Length of array
    bool* array;  ///< Array of booleans
} SimDBBoolVec;

/// Read parameter from the database.
/// @param self Return value of {@link sim_db_ctor()} or {@link
/// sim_db_ctor_with_id()}.
/// @param column Name of the parameter and column in the database.
/// @return Vector of booleans read from database. Do NOT free array as {@link
/// sim_db_dtor()} will do that.
SimDBBoolVec sim_db_read_bool_vec(SimDB* self, const char* column);

/// Write \p value to database.
//
/// @param self Return value of {@link sim_db_ctor()} or {@link
/// sim_db_ctor_with_id()}.
/// @param column Name of the column in the database to write to.
void sim_db_write_int(SimDB* self, const char* column, int value);

/// Write \p value to database.
//
/// @param self Return value of {@link sim_db_ctor()} or {@link
/// sim_db_ctor_with_id()}.
/// @param column Name of the column in the database to write to.
void sim_db_write_double(SimDB* self, const char* column, double value);

/// Write \p value to database.
//
/// @param self Return value of {@link sim_db_ctor()} or {@link
/// sim_db_ctor_with_id()}.
/// @param column Name of the column in the database to write to.
void sim_db_write_string(SimDB* self, const char* column, const char* value);

/// Write \p value to database.
//
/// @param self Return value of {@link sim_db_ctor()} or {@link
/// sim_db_ctor_with_id()}.
/// @param column Name of the column in the database to write to.
void sim_db_write_bool(SimDB* self, const char* column, bool value);

/// Write \p arr to database.
//
/// @param self Return value of {@link sim_db_ctor()} or {@link
/// sim_db_ctor_with_id()}.
/// @param column Name of the column in the database to write to.
/// @param arr Array to be written to simulation database.
/// @param len Length of \p arr.
void sim_db_write_int_array(SimDB* self, const char* column, int* arr,
                            size_t len);

/// Write \p arr to database.
//
/// @param self Return value of {@link sim_db_ctor()} or {@link
/// sim_db_ctor_with_id()}.
/// @param column Name of the column in the database to write to.
/// @param arr Array to be written to simulation database.
/// @param len Length of \p arr.
void sim_db_write_double_array(SimDB* self, const char* column, double* arr,
                               size_t len);

/// Write \p arr to database.
//
/// @param self Return value of {@link sim_db_ctor()} or {@link
/// sim_db_ctor_with_id()}.
/// @param column Name of the column in the database to write to.
/// @param arr Array to be written to simulation database.
/// @param len Length of \p arr.
void sim_db_write_string_array(SimDB* self, const char* column, char** arr,
                               size_t len);

/// Write \p arr to database.
//
/// @param self Return value of {@link sim_db_ctor()} or {@link
/// sim_db_ctor_with_id()}.
/// @param column Name of the column in the database to write to.
/// @param arr Array to be written to simulation database.
/// @param len Length of \p arr.
void sim_db_write_bool_array(SimDB* self, const char* column, bool* arr,
                             size_t len);

/// Make unique subdirectory in \p rel_path_to_result_dir.
//
/// This new subdirectory is intended for storing results from the
/// simulation.
/// @param self Return value of {@link sim_db_ctor()} or {@link
/// sim_db_ctor_with_id()}.
/// @param path_to_result_dir Path to where the new directory is created. If
/// it starts with 'root/', that part will be replaced with the full path to
/// the root directory of the project.
/// @return Path to new subdirectory.
char* sim_db_make_unique_subdir(SimDB* self, const char* path_to_result_dir);

/// Make unique subdirectory in \p abs_path_to_result_dir.
//
/// This new subdirectory is intended for storing results from the
/// simulation.
/// @param self Return value of {@link sim_db_ctor()} or {@link
/// sim_db_ctor_with_id()}.
/// @param abs_path_to_result_dir Absolute path to where the new directory
/// is created.
/// @return Path to new subdirectory.
char* sim_db_make_unique_subdir_abs_path(SimDB* self,
                                         const char* abs_path_to_result_dir);

/// Return true if \p column is a column in the database.
bool sim_db_column_exists(SimDB* self, const char* column);

/// Return ID number of simulation in the database that is connected.
//
/// @param self Return value of {@link sim_db_ctor()} or {@link
/// sim_db_ctor_with_id()}.
int sim_db_get_id(SimDB* self);

/// Return path to root directory of the project, where *.sim_db/* is
/// located.
//
/// @param self Return value of {@link sim_db_ctor()} or {@link
/// sim_db_ctor_with_id()}.
char* sim_db_get_path_proj_root(SimDB* self);

/// Save the sha1 hash of the files \p paths_executables to the database.
//
/// @param self Return value of {@link sim_db_ctor()} or {@link
/// sim_db_ctor_with_id()}.
/// @param paths_executables Paths to executable files.
/// @param len Length of \p paths_executables.
void sim_db_update_sha1_executables(SimDB* self, char** paths_executables,
                                    size_t len);

/// Clean up SimDB.
//
/// Add metadate for 'used_walltime' to database and update 'status' to
/// 'finished'.
/// @param self Return value of {@link sim_db_ctor()} or {@link
/// sim_db_ctor_with_id()}.
void sim_db_dtor(SimDB* self);

/// Add empty simulation to database and return its 'ID'.
//
/// @param path_proj_root Path to root directory of the project, where
/// *.sim_db/* is located.
/// @return Integer ID of the added simulation.
int add_empty_sim(const char* path_proj_root);

/// Delete simulation from database with ID number \p id.
//
/// @param path_proj_root Path to root directory of the project, where
/// *.sim_db/* is located.
/// @param id ID number of the simulation paramters in the **sim_db**
/// database.
void delete_sim(const char* path_proj_root, int id);

#endif
