/// @file sim_db.h
/// @brief All C functions to use ```sim_db```.

// Copyright (C) 2018-2020 Håkon Austlid Taskén <hakon.tasken@gmail.com>
// Licensed under the MIT License.

#ifndef SIM_DB_H
#define SIM_DB_H
#pragma once

#include <stdbool.h>
#include <stdlib.h>  // To get definition of size_t.

#define SIM_DB_VERSION "0.2.9"
#define SIM_DB_VERSION_NUMBER 209
#define SIM_DB_MAJOR_VERSION_NUMBER SIM_DB_VERSION_NUMBER / 10000
#define SIM_DB_MINOR_VERSION_NUMBER (SIM_DB_VERSION_NUMBER / 100) % 100
#define SIM_DB_PATCH_VERSION_NUMBER SIM_DB_VERSION_NUMBER % 100

typedef struct SimDB SimDB;

/// Initialize SimDB and connect to the **sim_db** database.
//
/// Should be called at the very start of the simulation and
/// {@link sim_db_dtor(SimDB*)} at the very end, to add the correct metadata.
/// {@link sim_db_dtor(SimDB*)} also does the clean up, so it MUST be called.
///
/// For multithreading/multiprocessing each thread/process MUST have its
/// own connection.
///
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
/// database. Should be used instead of {@link sim_db_ctor()} for
/// postprocessing.
///
/// {@link sim_db_dtor(SimDB*)} MUST be called to clean up.
///
/// For multithreading/multiprocessing each thread/process MUST have its
/// own connection.
///
/// @param argc Length of \p argv.
/// @param argv Array of command line arguments containing ```--id 'ID'``` and
/// optionally ```--path_proj_root 'PATH'```. *PATH* is the root directory of
/// the project, where *.sim_db/* is located. If not passed, the current working
/// directory and its parent directories will be searched until *.sim_db/* is
/// found.
SimDB* sim_db_ctor_no_metadata(int argc, char** argv);

/// Initialize SimDB and connect to the **sim_db** database.
//
/// Will search the current working directory and its parents directories until
/// *.sim_db/* is found.
///
/// {@link sim_db_dtor(SimDB*)} MUST be called to clean up.
///
/// For multithreading/multiprocessing each thread/process MUST have its
/// own connection.
///
/// @param id ID number of the simulation paramters in the **sim_db** database.
/// @param store_metadata Stores metadata if true. Set to 'false' for
/// postprocessing (e.g. visualization) of data from simulation.
SimDB* sim_db_ctor_with_id(int id, bool store_metadata);

/// Initialize SimDB and connect to the **sim_db** database.
//
/// {@link sim_db_dtor(SimDB*)} MUST be called to clean up.
///
/// For multithreading/multiprocessing each thread/process MUST have its
/// own connection.
///
/// @param path_proj_root Path to root directory of the project, where
/// *.sim_db/* is located.
/// @param id ID number of the simulation paramters in the **sim_db** database.
/// @param store_metadata Stores metadata if true. Set to 'false' for
/// postprocessing (e.g. visualization) of data from simulation.
SimDB* sim_db_ctor_without_search(const char* path_proj_root, int id,
                                  bool store_metadata);

/// Read parameter from the database.
//
/// @param self Return value of {@link sim_db_ctor()} or similar functions.
/// @param column Name of the parameter and column in the database.
/// @return Integer read from database.
int sim_db_read_int(SimDB* self, const char* column);

/// Read parameter from the database.
//
/// @param self Return value of {@link sim_db_ctor()} or similar functions.
/// @param column Name of the parameter and column in the database.
/// @return Double read from database.
double sim_db_read_double(SimDB* self, const char* column);

/// Read parameter from the database.
//
/// @param self Return value of {@link sim_db_ctor()} or similar functions.
/// @param column Name of the parameter and column in the database.
/// @return String read from database. Do NOT free the string, as {@link
/// sim_db_dtor()} will do that.
char* sim_db_read_string(SimDB* self, const char* column);

/// Read parameter from the database.
//
/// @param self Return value of {@link sim_db_ctor()} or similar functions.
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
/// @param self Return value of {@link sim_db_ctor()} or similar functions.
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
/// @param self Return value of {@link sim_db_ctor()} or similar functions.
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
/// @param self Return value of {@link sim_db_ctor()} or similar functions.
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
/// @param self Return value of {@link sim_db_ctor()} or similar functions.
/// @param column Name of the parameter and column in the database.
/// @return Vector of booleans read from database. Do NOT free array as {@link
/// sim_db_dtor()} will do that.
SimDBBoolVec sim_db_read_bool_vec(SimDB* self, const char* column);

/// Write \p value to database.
//
/// @param self Return value of {@link sim_db_ctor()} or similar functions.
/// @param column Name of the column in the database to write to.
/// @param only_if_empty If True, it will only write to the database if the
/// simulation's entry under 'column' is empty. Will avoid any potential
/// timeouts for concurrect applications.
void sim_db_write_int(SimDB* self, const char* column, int value,
                      bool only_if_empty);

/// Write \p value to database.
//
/// @param self Return value of {@link sim_db_ctor()} or similar functions.
/// @param column Name of the column in the database to write to.
/// @param only_if_empty If True, it will only write to the database if the
/// simulation's entry under 'column' is empty. Will avoid any potential
/// timeouts for concurrect applications.
void sim_db_write_double(SimDB* self, const char* column, double value,
                         bool only_if_empty);

/// Write \p value to database.
//
/// @param self Return value of {@link sim_db_ctor()} or similar functions.
/// @param column Name of the column in the database to write to.
/// @param only_if_empty If True, it will only write to the database if the
/// simulation's entry under 'column' is empty. Will avoid any potential
/// timeouts for concurrect applications.
void sim_db_write_string(SimDB* self, const char* column, const char* value,
                         bool only_if_empty);

/// Write \p value to database.
//
/// @param self Return value of {@link sim_db_ctor()} or similar functions.
/// @param column Name of the column in the database to write to.
/// @param only_if_empty If True, it will only write to the database if the
/// simulation's entry under 'column' is empty. Will avoid any potential
/// timeouts for concurrect applications.
void sim_db_write_bool(SimDB* self, const char* column, bool value,
                       bool only_if_empty);

/// Write \p arr to database.
//
/// @param self Return value of {@link sim_db_ctor()} or similar functions.
/// @param column Name of the column in the database to write to.
/// @param arr Array to be written to simulation database.
/// @param len Length of \p arr.
/// @param only_if_empty If True, it will only write to the database if the
/// simulation's entry under 'column' is empty. Will avoid any potential
/// timeouts for concurrect applications.
void sim_db_write_int_array(SimDB* self, const char* column, int* arr,
                            size_t len, bool only_if_empty);

/// Write \p arr to database.
//
/// @param self Return value of {@link sim_db_ctor()} or similar functions.
/// @param column Name of the column in the database to write to.
/// @param arr Array to be written to simulation database.
/// @param len Length of \p arr.
/// @param only_if_empty If True, it will only write to the database if the
/// simulation's entry under 'column' is empty. Will avoid any potential
/// timeouts for concurrect applications.
void sim_db_write_double_array(SimDB* self, const char* column, double* arr,
                               size_t len, bool only_if_empty);

/// Write \p arr to database.
//
/// @param self Return value of {@link sim_db_ctor()} or similar functions.
/// @param column Name of the column in the database to write to.
/// @param arr Array to be written to simulation database.
/// @param len Length of \p arr.
/// @param only_if_empty If True, it will only write to the database if the
/// simulation's entry under 'column' is empty. Will avoid any potential
/// timeouts for concurrect applications.
void sim_db_write_string_array(SimDB* self, const char* column, char** arr,
                               size_t len, bool only_if_empty);

/// Write \p arr to database.
//
/// @param self Return value of {@link sim_db_ctor()} or similar functions.
/// @param column Name of the column in the database to write to.
/// @param arr Array to be written to simulation database.
/// @param len Length of \p arr.
/// @param only_if_empty If True, it will only write to the database if the
/// simulation's entry under 'column' is empty. Will avoid any potential
/// timeouts for concurrect applications.
void sim_db_write_bool_array(SimDB* self, const char* column, bool* arr,
                             size_t len, bool only_if_empty);

/// Get path to subdirectory in \p abs_path_to_dir unique to simulation.
//
/// The subdirectory will be named 'date_time_name_id' and is intended to store
/// results in. If 'results_dir' in the database is empty, a new and unique
/// directory is created and the path stored in 'results_dir'. Otherwise the
/// path in 'results_dir' is just returned.
///
/// @param self Return value of {@link sim_db_ctor()} or similar functions.
/// @param path_to_dir Path to where the new directory is created. If
/// it starts with 'root/', that part will be replaced with the full path to
/// the root directory of the project.
/// @return Path to new subdirectory.
char* sim_db_unique_results_dir(SimDB* self, const char* path_to_dir);

/// Get path to subdirectory in \p abs_path_to_dir unique to simulation.
//
/// The subdirectory will be named 'date_time_name_id' and is intended to store
/// results in. If 'results_dir' in the database is empty, a new and unique
/// directory is created and the path stored in 'results_dir'. Otherwise the
/// path in 'results_dir' is just returned.
///
/// @param self Return value of {@link sim_db_ctor()} or similar functions.
/// @param abs_path_to_dir Absolute path to where the new directory
/// is created.
/// @return Path to new subdirectory.
char* sim_db_unique_results_dir_abs_path(SimDB* self,
                                         const char* abs_path_to_dir);

/// Return true if \p column is a column in the database.
bool sim_db_column_exists(SimDB* self, const char* column);

/// Return true if entry in database under \p column is empty.
bool sim_db_is_empty(SimDB* self, const char* column);

/// Set entry under \p column in database to empty.
void sim_db_set_empty(SimDB* self, const char* column);

/// Return ID number of simulation in the database that is connected.
//
/// @param self Return value of {@link sim_db_ctor()} or similar functions.
int sim_db_get_id(SimDB* self);

/// Return path to root directory of the project, where *.sim_db/* is
/// located.
//
/// @param self Return value of {@link sim_db_ctor()} or similar functions.
char* sim_db_get_path_proj_root(SimDB* self);

/// Save the sha1 hash of the files \p paths_executables to the database.
//
/// @param self Return value of {@link sim_db_ctor()} or similar functions.
/// @param paths_executables Paths to executable files.
/// @param len Length of \p paths_executables.
/// @param only_if_empty If True, it will only write to the database if the
/// simulation's entry under 'sha1_executables' is empty. Will avoid any
/// potential timeouts for concurrect applications.
void sim_db_update_sha1_executables(SimDB* self, char** paths_executables,
                                    size_t len, bool only_if_empty);

/// Allow timeouts to occure without exiting if set to true.
//
/// A timeout occures after waiting more than 5 seconds to access the database
/// because other threads/processes are busy writing to it. **sim_db**
/// will exit with an error in that case, unless allow timeouts is set to true.
/// It is false by default. If allowed and a timeout occures the called
/// funciton will have had no effect.
void sim_db_allow_timeouts(SimDB* self, bool allow_timeouts);

/// Checks if a timeout have occured since last call to this function.
bool sim_db_have_timed_out(SimDB* self);

/// Delete simulation from database.
void sim_db_delete_from_database(SimDB* self);

/// Clean up SimDB.
//
/// Add metadate for 'used_walltime' to database and update 'status' to
/// 'finished'.
/// @param self Return value of {@link sim_db_ctor()} or similar functions.
void sim_db_dtor(SimDB* self);

/// Add empty simulation to database and return a SimDB connected to it.
//
/// The current working directory and its parent directories will be searched
/// until *.sim_db/* is found.
///
/// @return SimDB of the added simulation.
/// @param store_metadata Stores metadata if true. Set to 'false' for
/// postprocessing (e.g. visualization) of data from simulation.
SimDB* sim_db_add_empty_sim(bool store_metadata);

/// Add empty simulation to database and return a SimDB connected to it.
//
/// @return SimDB of the added simulation.
/// @param path_proj_root Path to root directory of the project, where
/// *.sim_db/* is located.
/// @param store_metadata Stores metadata if true. Set to 'false' for
/// postprocessing (e.g. visualization) of data from simulation.
SimDB* sim_db_add_empty_sim_without_search(const char* path_proj_root,
                                           bool store_metadata);

#endif
