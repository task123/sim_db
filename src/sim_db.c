// Copyright (C) 2018 Håkon Austlid Taskén <hakon.tasken@gmail.com>
// Licensed under the MIT License.

#define _XOPEN_SOURCE 500

#include "sim_db.h"

#include <ctype.h>
#include <float.h>
#include <limits.h>
#include <math.h>
#include <pthread.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <time.h>
#include <unistd.h>
#include "sqlite3.h"

#ifndef PATH_MAX
#define PATH_MAX 4096
#endif

char errormsg[100] = "";

struct SimDB {
    sqlite3* db;
    const int id;
    void** pointers_to_free;
    size_t n_pointers;
    size_t buffer_size_pointers;
    char path_proj_root[PATH_MAX + 1];
    const bool store_metadata;
    const time_t start_time;
    bool allow_timeouts;
    bool have_timed_out;
    SimDBStringVec column_names;
};

void sim_db_add_pointer_to_free(SimDB* self, void* pointer) {
    if (self->n_pointers >= self->buffer_size_pointers) {
        self->buffer_size_pointers *= 2;
        self->pointers_to_free =
                (void**) realloc(self->pointers_to_free,
                                 self->buffer_size_pointers * sizeof(void*));
    }
    self->pointers_to_free[self->n_pointers] = pointer;
    self->n_pointers++;
}

void sim_db_free(SimDB* self, void* pointer) {
    int pointer_pos = -1;
    for (size_t i = 0; i < self->n_pointers; i++) {
        if (pointer_pos > 0) {
            self->pointers_to_free[i - 1] = self->pointers_to_free[i];
        } else if (&self->pointers_to_free[i] == &pointer) {
            pointer_pos = i;
            free(pointer);
        }
    }
    self->n_pointers--;
}

void sim_db_allow_timeouts(SimDB* self, bool allow_timeouts) {
    self->allow_timeouts = allow_timeouts;
}

bool sim_db_have_timed_out(SimDB* self) {
    bool have_timed_out = self->have_timed_out;
    self->have_timed_out = false;
    return have_timed_out;
}

void sim_db_backslash_unslashed_spaces(char path[PATH_MAX + 1]) {
    char path_backslashed[PATH_MAX + 1];
    const int len_path = strlen(path);
    int n_spaces = 0;
    for (int i = 0; i < len_path + n_spaces + 1; i++) {
        path_backslashed[i + n_spaces] = path[i];
        if (path[i] == ' ' && i > 0 && path[i - 1] != '\\') {
            path_backslashed[i + n_spaces] = '\\';
            path_backslashed[i + n_spaces + 1] = ' ';
            n_spaces++;
        }
    }
    strcpy(path, path_backslashed);
}

void sim_db_get_time_string(char time_string[]) {
    time_t now = time(NULL);
    char local_time[26];
    strcpy(local_time, asctime(localtime(&now)));
    local_time[7] = '\0';
    local_time[10] = '\0';
    local_time[19] = '\0';
    local_time[24] = '\0';
    local_time[13] = '-';
    local_time[16] = '-';
    strcpy(time_string, &local_time[20]);
    strcat(time_string, "-");
    strcat(time_string, &local_time[4]);
    strcat(time_string, "-");
    strcat(time_string, &local_time[8]);
    strcat(time_string, "_");
    strcat(time_string, &local_time[11]);
    if (time_string[9] == ' ') {
        time_string[9] = '0';
    }
}

/* Return EXIT_SUCCESS if database is NOT busy. */
bool sim_db_busy_database(SimDB* self, int sqlite_return_code,
                          const char* function_name, int line_number) {
    if (sqlite_return_code != SQLITE_BUSY) {
        return EXIT_SUCCESS;
    } else {
        if (self->allow_timeouts) {
            self->have_timed_out = true;
            return EXIT_FAILURE;
        } else {
            fprintf(stderr,
                    "Error in function %s at line no. %d.\nERROR: sim_db "
                    "function timed out after being blocked from accessing the "
                    "sim_db\n       database for more than 5 seconds. This is "
                    "caused by too much concurrent\n       writing to the "
                    "database.\n",
                    function_name, line_number);
            exit(EXIT_FAILURE);
        }
    }
}

bool sim_db_is_empty(SimDB* self, const char* column) {
    char* query = malloc(sizeof(char) * (2 * strlen(column) + 100));
    sprintf(query,
            "SELECT \"%s\" FROM runs WHERE \"id\" = %d AND \"%s\" IS NULL",
            column, self->id, column);
    sqlite3_stmt* stmt = NULL;
    int rc = sqlite3_prepare_v2(self->db, query, -1, &stmt, NULL);
    if (sim_db_busy_database(self, rc, __func__, __LINE__)) {
        return false;
    } else if (rc != SQLITE_OK) {
        fprintf(stderr,
                "Error in function %s at line no. %d.\nERROR: Could NOT "
                "prepare the SQLite3 query: '%s'\nSQLite3 error "
                "message:\n%s\n",
                __func__, __LINE__, query, sqlite3_errmsg(self->db));
        exit(EXIT_FAILURE);
    }
    rc = sqlite3_step(stmt);
    bool is_empty = false;
    if (rc == SQLITE_ROW) {
        is_empty = true;
    } else if (rc == SQLITE_DONE) {
        is_empty = false;
    } else if (sim_db_busy_database(self, rc, __func__, __LINE__)) {
        is_empty = false;
    } else {
        fprintf(stderr,
                "Error in function %s at line no. %d.\nERROR: Could NOT "
                "read "
                "column=%s with id=%d form database.\nSQLite3 error "
                "message:\n%s\n",
                __func__, __LINE__, column, self->id, sqlite3_errmsg(self->db));
        exit(EXIT_FAILURE);
    }
    sqlite3_finalize(stmt);
    free(query);
    return is_empty;
}

void sim_db_update(SimDB* self, const char* column, const char* value,
                   bool only_if_empty) {
    bool set_to_empty = false;
    if (value == NULL) {
        set_to_empty = true;
        value = "";
    }
    char* query =
            malloc(sizeof(char) * (2 * strlen(column) + strlen(value) + 100));
    if (set_to_empty) {
        sprintf(query, "UPDATE runs SET \"%s\" = NULL WHERE id = %d", column,
                self->id);
    } else if (only_if_empty) {
        sprintf(query,
                "UPDATE runs SET \"%s\" = '%s' WHERE id = %d AND \"%s\" IS "
                "NULL",
                column, value, self->id, column);
    } else {
        sprintf(query, "UPDATE runs SET \"%s\" = '%s' WHERE id = %d", column,
                value, self->id);
    }

    int rc = SQLITE_BUSY;
    if (only_if_empty || set_to_empty) {
        time_t start_time = time(NULL);
        bool is_empty;
        while (rc == SQLITE_BUSY && time(NULL) < start_time + 5) {
            sqlite3_busy_timeout(self->db, 10000);
            is_empty = sim_db_is_empty(self, column);
            if (self->have_timed_out) {
                rc = SQLITE_OK;
            } else if (only_if_empty && !is_empty) {
                rc = SQLITE_OK;
            } else if (set_to_empty && is_empty) {
                rc = SQLITE_OK;
            } else {
                sqlite3_busy_timeout(self->db, 0);
                rc = sqlite3_exec(self->db, query, NULL, NULL, NULL);
            }
        }
        sqlite3_busy_timeout(self->db, 5000);
    }
    if (rc == SQLITE_BUSY) {
        rc = sqlite3_exec(self->db, query, NULL, NULL, NULL);
    }
    if (rc != SQLITE_OK
        && !sim_db_busy_database(self, rc, __func__, __LINE__)) {
        fprintf(stderr,
                "Error in function %s at line no. %d.\nERROR: Could "
                "NOT "
                "perform the SQLite3 query: '%s'\nSQLite3 error "
                "message:\n%s\n",
                __func__, __LINE__, query, sqlite3_errmsg(self->db));
        free(query);
        exit(EXIT_FAILURE);
    }
    free(query);
}

// Return EXIT_SUCCESS if file can be opened
int sim_db_run_shell_command(const char* command, char* output,
                             size_t len_output) {
    FILE* file;
    file = popen(command, "r");
    size_t i = 0;
    int c;
    if (file) {
        while ((c = getc(file)) != EOF && i < len_output - 1) {
            output[i++] = (char) c;
        }
        output[i] = '\0';
        pclose(file);
        return EXIT_SUCCESS;
    } else {
        pclose(file);
        return EXIT_FAILURE;
    }
}

bool sim_db_is_a_git_project(char path_dot_sim_db_parent_dir[PATH_MAX + 1]) {
    char path_in_project[PATH_MAX + 1];
    strcpy(path_in_project, path_dot_sim_db_parent_dir);
    strcat(path_in_project, "/");
    char git_file[20] = "/.git/index";
    for (int i = strlen(path_in_project) - 1; i >= 0; i--) {
        if (path_in_project[i] == '/') {
            path_in_project[i] = '\0';
            strcat(path_in_project, git_file);
            FILE* fp = fopen(path_in_project, "r");
            if (fp != NULL) {
                fclose(fp);
                return true;
            }
        }
    }
    return false;
}

char* sim_db_escape_quote_with_two_quotes(const char* string) {
    char* escaped_string = malloc(2 * (strlen(string) + 1) * sizeof(char));
    int j = 0;
    for (int i = 0; i < (int) strlen(string) + 1; i++) {
        if (string[i] != '\'') {
            escaped_string[i + j] = string[i];
        } else {
            escaped_string[i + j] = '\'';
            escaped_string[i + (++j)] = '\'';
        }
    }
    return escaped_string;
}

void sim_db_find_path_proj_root(char* path_proj_root, int buffer_size) {
    if (getcwd(path_proj_root, sizeof(char) * (buffer_size))) {
        strcat(path_proj_root, "/");
        char settings[30] = "/.sim_db/settings.txt";
        for (int i = strlen(path_proj_root) - 1; i >= 0; i--) {
            if (path_proj_root[i] == '/') {
                path_proj_root[i] = '\0';
                strcat(path_proj_root, settings);
                FILE* fp = fopen(path_proj_root, "r");
                path_proj_root[i] = '\0';
                if (fp != NULL) {
                    fclose(fp);
                    break;
                }
            }
        }
        if (strlen(path_proj_root) <= 1) {
            fprintf(stderr,
                    "Error in function %s at line no. %d.\nERROR: Could "
                    "NOT find '.sim_db/settings.txt' in this or any "
                    "parents directories.\nRun '$ init' in the "
                    "project's root directory.\n",
                    __func__, __LINE__);
            exit(EXIT_FAILURE);
        }
    } else {
        fprintf(stderr,
                "Error in function %s at line no. %d.\nERROR: getcwd() did "
                "NOT work.",
                __func__, __LINE__);
        exit(EXIT_FAILURE);
    }
}

SimDB* sim_db_ctor_metadata(int argc, char** argv, bool store_metadata) {
    char path_proj_root[PATH_MAX + 1];
    bool is_path_proj_root_found = false;
    bool is_id_found = false;
    int id = -1;
    for (int i = 0; i < argc - 1; i++) {
        if ((strcmp(argv[i], "--id") == 0) || (strcmp(argv[i], "-i") == 0)) {
            is_id_found = true;
            id = atoi(argv[i + 1]);
        }
        if ((strcmp(argv[i], "--path_proj_root") == 0)
            || (strcmp(argv[i], "-p") == 0)) {
            is_path_proj_root_found = true;
            if (strlen(argv[i + 1]) <= PATH_MAX) {
                strcpy(path_proj_root, argv[i + 1]);
            } else {
                fprintf(stderr,
                        "Error in function %s at line no. %d.\nERROR: "
                        "'--path_proj_root' can NOT be longer than %d.\n",
                        __func__, __LINE__, PATH_MAX);
                exit(EXIT_FAILURE);
            }
        }
        if (is_id_found && is_path_proj_root_found) {
            break;
        }
    }
    if (!is_id_found) {
        fprintf(stderr,
                "Error in function %s at line no. %d.\nERROR: '--id ID' or '-i "
                "ID' MUST be passed as command line arguments.\n",
                __func__, __LINE__);
        exit(EXIT_FAILURE);
    }
    if (!is_path_proj_root_found) {
        sim_db_find_path_proj_root(path_proj_root, PATH_MAX + 1);
    }

    SimDB* sim_db =
            sim_db_ctor_without_search(path_proj_root, id, store_metadata);

    if (store_metadata) {
        int len_path_proj_root = strlen(path_proj_root);
        if (len_path_proj_root > 0
            && path_proj_root[len_path_proj_root - 1] == '/') {
            path_proj_root[len_path_proj_root - 1] = '\0';
        }
        if (sim_db_is_a_git_project(path_proj_root)) {
            char* program_name_array[1];
            program_name_array[0] = argv[0];
            FILE* fp = fopen(program_name_array[0], "r");
            if (fp != NULL) {
                fclose(fp);
                sim_db_update_sha1_executables(sim_db, program_name_array, 1,
                                               true);
            }
        }
    }

    return sim_db;
}

SimDB* sim_db_ctor(int argc, char** argv) {
    return sim_db_ctor_metadata(argc, argv, true);
}

SimDB* sim_db_ctor_no_metadata(int argc, char** argv) {
    return sim_db_ctor_metadata(argc, argv, false);
}

SimDB* sim_db_ctor_with_id(int id, bool store_metadata) {
    char path_proj_root[PATH_MAX + 1];
    sim_db_find_path_proj_root(path_proj_root, PATH_MAX + 1);
    return sim_db_ctor_without_search(path_proj_root, id, store_metadata);
}

SimDB* sim_db_ctor_without_search(const char* path_proj_root, int id,
                                  bool store_metadata) {
    char path_database[PATH_MAX + 1];
    int len_path_proj_root = strlen(path_proj_root);
    if (len_path_proj_root <= PATH_MAX) {
        strcpy(path_database, path_proj_root);
    } else {
        fprintf(stderr,
                "Error in function %s at line no. %d.\nERROR: 'path_proj_root' "
                "can NOT be longer than %d.\n",
                __func__, __LINE__, PATH_MAX);
        exit(EXIT_FAILURE);
    }
    sqlite3* db;
    if (len_path_proj_root > 0
        && path_database[len_path_proj_root - 1] == '/') {
        path_database[len_path_proj_root - 1] = '\0';
    }
    strcat(path_database, "/.sim_db/sim.db");
    int rc = sqlite3_open_v2(
            path_database, &db,
            SQLITE_OPEN_READWRITE | SQLITE_OPEN_CREATE | SQLITE_OPEN_FULLMUTEX,
            NULL);
    if (rc != SQLITE_OK) {
        fprintf(stderr,
                "Error in function %s at line no. %d.\nERROR: Can NOT open "
                "database '%s': %s\n",
                __func__, __LINE__, path_database, sqlite3_errmsg(db));
        exit(EXIT_FAILURE);
    }
    sqlite3_busy_timeout(db, 5000);

    SimDB sim_db_init = {
            .db = db,
            .id = id,
            .buffer_size_pointers = 5,
            .pointers_to_free = malloc(5 * sizeof(void*)),
            .n_pointers = 0,
            .store_metadata = store_metadata,
            .start_time = time(NULL),
            .allow_timeouts = true,  // Set to false at end of function.
            .have_timed_out = false};
    path_database[strlen(path_database) - 15] = '\0';
    strcpy(sim_db_init.path_proj_root, path_database);
    SimDB* sim_db = malloc(sizeof(SimDB));
    memcpy(sim_db, &sim_db_init, sizeof(SimDB));
    sim_db->column_names.size = 0;
    sim_db->column_names.array = NULL;

    if (store_metadata) {
        char time_started[80];
        sim_db_get_time_string(time_started);
        sim_db_update(sim_db, "time_started", time_started, true);
    }

    const size_t len_output = 3001;
    char output[len_output + 200];
    char command[4200];

    if (store_metadata && sim_db_is_a_git_project(sim_db->path_proj_root)) {
        char path_proj_root_backslashed[PATH_MAX + 1];
        strcpy(path_proj_root_backslashed, sim_db->path_proj_root);
        sim_db_backslash_unslashed_spaces(path_proj_root_backslashed);
        sprintf(command, "cd %s && git rev-parse HEAD",
                path_proj_root_backslashed);
        if (sim_db_run_shell_command(command, output, len_output) == 0) {
            sim_db_update(sim_db, "git_hash", output, true);
        }

        sprintf(command, "cd %s && git log -n --format=%%B HEAD",
                path_proj_root_backslashed);
        if (sim_db_run_shell_command(command, output, len_output) == 0) {
            char* escaped_string = sim_db_escape_quote_with_two_quotes(output);
            sim_db_update(sim_db, "commit_message", output, true);
            free(escaped_string);
        }

        sprintf(command, "cd %s && git diff HEAD --stat",
                path_proj_root_backslashed);
        if (sim_db_run_shell_command(command, output, len_output) == 0) {
            char* escaped_string = sim_db_escape_quote_with_two_quotes(output);
            sim_db_update(sim_db, "git_diff_stat", escaped_string, true);
            free(escaped_string);
        }

        sprintf(command, "cd %s && git diff HEAD", path_proj_root_backslashed);
        if (sim_db_run_shell_command(command, output, len_output) == 0) {
            if (strlen(output) >= len_output) {
                char warning[100];
                char output_with_warning[len_output + 200];
                sprintf(warning,
                        "WARNING: Diff limited to first %ld "
                        "characters.\n",
                        (long) len_output);
                strcpy(output_with_warning, warning);
                strcat(output_with_warning, output);
                strcat(output_with_warning, warning);
                char* escaped_string =
                        sim_db_escape_quote_with_two_quotes(output);
                sim_db_update(sim_db, "git_diff", escaped_string, true);
                free(escaped_string);
            } else {
                char* escaped_string =
                        sim_db_escape_quote_with_two_quotes(output);
                sim_db_update(sim_db, "git_diff", escaped_string, true);
                free(escaped_string);
            }
        }
    }
    sim_db->allow_timeouts = false;

    return sim_db;
}

/* MUST call sqlite3_finalize on return value. */
sqlite3_stmt* sim_db_select_prepare_step(SimDB* self, const char* column,
                                         int sqlite_return_type) {
    char query[256];
    sprintf(query, "SELECT %s FROM runs WHERE \"id\" = %d", column, self->id);
    sqlite3_stmt* stmt = NULL;
    int rc = sqlite3_prepare_v2(self->db, query, -1, &stmt, NULL);
    if (sim_db_busy_database(self, rc, __func__, __LINE__)) {
        sqlite3_finalize(stmt);
        return NULL;
    } else if (rc != SQLITE_OK) {
        fprintf(stderr,
                "Error in function %s at line no. %d.\nERROR: Could NOT "
                "prepare the SQLite3 query: '%s'\nSQLite3 error "
                "message:\n%s\n",
                __func__, __LINE__, query, sqlite3_errmsg(self->db));
        exit(EXIT_FAILURE);
    }
    rc = sqlite3_step(stmt);
    if (rc == SQLITE_ROW) {
        int type = sqlite3_column_type(stmt, 0);
        if (type != sqlite_return_type) {
            fprintf(stderr,
                    "Error in function %s at line no. %d.\nERROR: Column "
                    "%s in "
                    "sim_db's database is NOT correct type.\n",
                    __func__, __LINE__, column);
            exit(EXIT_FAILURE);
        }
    } else if (sim_db_busy_database(self, rc, __func__, __LINE__)) {
        sqlite3_finalize(stmt);
        return NULL;
    } else {
        fprintf(stderr,
                "Error in function %s at line no. %d.\nERROR: Could NOT "
                "read "
                "column=%s with id=%d form database.\nSQLite3 error "
                "message:\n%s\n",
                __func__, __LINE__, column, self->id, sqlite3_errmsg(self->db));
        exit(EXIT_FAILURE);
    }
    return stmt;
}

int sim_db_read_int(SimDB* self, const char* column) {
    sqlite3_stmt* stmt =
            sim_db_select_prepare_step(self, column, SQLITE_INTEGER);
    if (stmt == NULL) {
        return -1;
    }
    int result = sqlite3_column_int(stmt, 0);
    sqlite3_finalize(stmt);
    return result;
}

double sim_db_read_double(SimDB* self, const char* column) {
    sqlite3_stmt* stmt = sim_db_select_prepare_step(self, column, SQLITE_FLOAT);
    if (stmt == NULL) {
        return -1.0;
    }
    double result = sqlite3_column_double(stmt, 0);
    sqlite3_finalize(stmt);
    return result;
}

char* sim_db_read_string(SimDB* self, const char* column) {
    sqlite3_stmt* stmt = sim_db_select_prepare_step(self, column, SQLITE_TEXT);
    if (stmt == NULL) {
        return NULL;
    }
    char* text = (char*) sqlite3_column_text(stmt, 0);
    char* string = malloc((strlen(text) + 1) * sizeof(char));
    strcpy(string, text);
    sqlite3_finalize(stmt);
    sim_db_add_pointer_to_free(self, string);
    return string;
}

bool sim_db_read_bool(SimDB* self, const char* column) {
    char* bool_string = sim_db_read_string(self, column);
    if (strcmp(bool_string, "True") == 0) {
        sim_db_free(self, bool_string);
        return true;
    } else if (strcmp(bool_string, "False") == 0) {
        sim_db_free(self, bool_string);
        return false;
    } else if (bool_string == NULL) {
        return false;
    } else {
        fprintf(stderr,
                "Error in function %s at line no. %d.\nERROR: The value "
                "under "
                "column %s with id %d is NOT 'True' or 'False', but %s.\n",
                __func__, __LINE__, column, self->id, bool_string);
        exit(EXIT_FAILURE);
    }
}

SimDBIntVec sim_db_read_int_vec(SimDB* self, const char* column) {
    char* int_arr_string = sim_db_read_string(self, column);
    if (self->allow_timeouts && int_arr_string == NULL) {
        SimDBIntVec empty = {};
        return empty;
    }
    if (strstr(int_arr_string, "int[") != int_arr_string) {
        fprintf(stderr,
                "Error in function %s at line no. %d.\nERROR: The type "
                "under "
                "column=%s with id=%d is NOT int array.\n",
                __func__, __LINE__, column, self->id);
        exit(EXIT_FAILURE);
    }
    SimDBIntVec int_vec;
    int_vec.size = 5;
    int_vec.array = malloc(int_vec.size * sizeof(int));
    char number[100];
    size_t n_digits = 0;
    size_t n_numbers = 0;
    for (size_t i = 4; i < strlen(int_arr_string); i++) {
        if (int_arr_string[i] == ',' || int_arr_string[i] == ']') {
            number[n_digits] = '\0';
            if (n_numbers >= int_vec.size) {
                int* new_arr = malloc(2 * int_vec.size * sizeof(int));
                memcpy(new_arr, int_vec.array, int_vec.size * sizeof(int));
                int_vec.size *= 2;
                free(int_vec.array);
                int_vec.array = new_arr;
            }
            int_vec.array[n_numbers] = atoi(number);
            n_numbers++;
            n_digits = 0;
        } else {
            number[n_digits] = int_arr_string[i];
            n_digits++;
        }
    }
    int_vec.size = n_numbers;
    sim_db_free(self, int_arr_string);
    sim_db_add_pointer_to_free(self, int_vec.array);
    return int_vec;
}

SimDBDoubleVec sim_db_read_double_vec(SimDB* self, const char* column) {
    char* double_arr_string = sim_db_read_string(self, column);
    if (strstr(double_arr_string, "float[") != double_arr_string) {
        fprintf(stderr,
                "Error in function %s at line no. %d.\nERROR: The type "
                "under "
                "column=%s with id=%d is NOT double array.\n",
                __func__, __LINE__, column, self->id);
        exit(EXIT_FAILURE);
    }
    SimDBDoubleVec double_vec;
    double_vec.size = 5;
    double_vec.array = malloc(double_vec.size * sizeof(double));
    char number[100];
    size_t n_digits = 0;
    size_t n_numbers = 0;
    for (size_t i = 6; i < strlen(double_arr_string); i++) {
        if (double_arr_string[i] == ',' || double_arr_string[i] == ']') {
            number[n_digits] = '\0';
            if (n_numbers >= double_vec.size) {
                double* new_arr = malloc(2 * double_vec.size * sizeof(int));
                memcpy(new_arr, double_vec.array,
                       double_vec.size * sizeof(int));
                double_vec.size *= 2;
                free(double_vec.array);
                double_vec.array = new_arr;
            }
            double_vec.array[n_numbers] = atof(number);
            n_numbers++;
            n_digits = 0;
        } else {
            number[n_digits] = double_arr_string[i];
            n_digits++;
        }
    }
    double_vec.size = n_numbers;
    sim_db_free(self, double_arr_string);
    sim_db_add_pointer_to_free(self, double_vec.array);
    return double_vec;
}

SimDBStringVec sim_db_read_string_vec(SimDB* self, const char* column) {
    char* str_arr_string = sim_db_read_string(self, column);
    if (strstr(str_arr_string, "string[") != str_arr_string) {
        fprintf(stderr,
                "Error in function %s at line no. %d.\nERROR: The type "
                "under "
                "column=%s with id=%d is NOT string array.\n",
                __func__, __LINE__, column, self->id);
        exit(EXIT_FAILURE);
    }
    SimDBStringVec string_vec;
    string_vec.size = 5;
    string_vec.array = malloc(string_vec.size * sizeof(char*));
    char string[100];
    size_t n_char = 0;
    size_t n_strings = 0;
    for (size_t i = 7; i < strlen(str_arr_string); i++) {
        if (str_arr_string[i] == ',' || str_arr_string[i] == ']') {
            string[n_char] = '\0';
            if (n_strings >= string_vec.size) {
                char** new_arr = malloc(2 * string_vec.size * sizeof(char*));
                memcpy(new_arr, string_vec.array,
                       string_vec.size * sizeof(char*));
                string_vec.size *= 2;
                free(string_vec.array);
                string_vec.array = new_arr;
            }
            string_vec.array[n_strings] =
                    malloc((strlen(string) + 1) * sizeof(char));
            strcpy(string_vec.array[n_strings], string);
            n_strings++;
            n_char = 0;
            i++;
        } else {
            string[n_char] = str_arr_string[i];
            n_char++;
        }
    }
    string_vec.size = n_strings;
    sim_db_free(self, str_arr_string);
    for (size_t i = 0; i < n_strings; i++) {
        sim_db_add_pointer_to_free(self, string_vec.array[i]);
    }
    sim_db_add_pointer_to_free(self, string_vec.array);
    return string_vec;
}

SimDBBoolVec sim_db_read_bool_vec(SimDB* self, const char* column) {
    char* bool_arr_str = sim_db_read_string(self, column);
    if (strstr(bool_arr_str, "bool[") != bool_arr_str) {
        fprintf(stderr,
                "Error in function %s at line no. %d.\nERROR: The type "
                "under "
                "column=%s with id=%d is NOT double array.\n",
                __func__, __LINE__, column, self->id);
        exit(EXIT_FAILURE);
    }
    SimDBBoolVec bool_vec;
    bool_vec.size = 5;
    bool_vec.array = malloc(bool_vec.size * sizeof(bool));
    char bool_str[100];
    size_t n_char = 0;
    size_t n_bools = 0;
    for (size_t i = 5; i < strlen(bool_arr_str); i++) {
        if (bool_arr_str[i] == ',' || bool_arr_str[i] == ']') {
            bool_str[n_char] = '\0';
            if (n_bools >= bool_vec.size) {
                bool* new_arr = malloc(2 * bool_vec.size * sizeof(bool));
                memcpy(new_arr, bool_vec.array, bool_vec.size * sizeof(bool));
                bool_vec.size *= 2;
                free(bool_vec.array);
                bool_vec.array = new_arr;
            }
            if (strcmp(bool_str, "True") == 0) {
                bool_vec.array[n_bools] = true;
            } else if (strcmp(bool_str, "False") == 0) {
                bool_vec.array[n_bools] = false;
            } else {
                fprintf(stderr,
                        "Error in function %s at line no. %d.\nERROR: A value "
                        "in the array  under column %s with id %d is NOT "
                        "'True' or 'False', but %s.\n",
                        __func__, __LINE__, column, self->id, bool_str);
                exit(EXIT_FAILURE);
            }
            n_bools++;
            n_char = 0;
            i++;
        } else {
            bool_str[n_char] = bool_arr_str[i];
            n_char++;
        }
    }
    bool_vec.size = n_bools;
    sim_db_free(self, bool_arr_str);
    sim_db_add_pointer_to_free(self, bool_vec.array);
    return bool_vec;
}

void sim_db_free_column_names(SimDBStringVec column_names) {
    for (size_t i = 0; i < column_names.size; i++) {
        free(column_names.array[i]);
    }
    free(column_names.array);
}

void sim_db_update_column_names(SimDB* self) {
    char query[100];
    sprintf(query, "SELECT * FROM runs WHERE \"id\" = %d;", self->id);
    sqlite3_stmt* stmt = NULL;
    int rc = sqlite3_prepare_v2(self->db, query, -1, &stmt, NULL);
    if (sim_db_busy_database(self, rc, __func__, __LINE__)) {
        return;
    } else if (rc != SQLITE_OK) {
        fprintf(stderr, "id %d\n", self->id);
        fprintf(stderr,
                "Error in function %s at line no. %d.\nERROR: Could NOT "
                "prepare the SQLite3 query: '%s'\nSQLite3 error "
                "message:\n%s\n",
                __func__, __LINE__, query, sqlite3_errmsg(self->db));
        exit(EXIT_FAILURE);
    }
    rc = sqlite3_step(stmt);
    SimDBStringVec column_names;
    column_names.size = self->column_names.size + 5;
    column_names.array = (char**) malloc(column_names.size * sizeof(char*));
    if (rc == SQLITE_ROW) {
        size_t i = 0;
        char* column = (char*) sqlite3_column_name(stmt, i);
        while (column != NULL) {
            if (i >= column_names.size) {
                column_names.size *= 2;
                column_names.array = (char**) realloc(
                        column_names.array, column_names.size * sizeof(char*));
            }
            column_names.array[i] = malloc((strlen(column) + 1) * sizeof(char));
            strcpy(column_names.array[i], column);
            column = (char*) sqlite3_column_name(stmt, ++i);
        }
        column_names.size = i;
    } else if (sim_db_busy_database(self, rc, __func__, __LINE__)) {
        return;
    } else {
        fprintf(stderr,
                "Error in function %s at line no. %d.\nERROR: Could NOT read "
                "from database.\nSQLite3 error message:\n%s\n",
                __func__, __LINE__, sqlite3_errmsg(self->db));
        exit(EXIT_FAILURE);
    }
    sqlite3_finalize(stmt);

    sim_db_free_column_names(self->column_names);
    self->column_names = column_names;
}

bool sim_db_column_exists(SimDB* self, const char* column) {
    for (size_t i = 0; i < self->column_names.size; i++) {
        if (strcmp(column, self->column_names.array[i]) == 0) {
            return true;
        }
    }
    sim_db_update_column_names(self);
    for (size_t i = 0; i < self->column_names.size; i++) {
        if (strcmp(column, self->column_names.array[i]) == 0) {
            return true;
        }
    }
    return false;
}

void sim_db_add_column_if_not_exists(SimDB* self, const char* column,
                                     const char* type) {
    char* query = malloc(sizeof(char) * (strlen(column) + 100));
    sprintf(query, "ALTER TABLE runs ADD COLUMN \"%s\" %s", column, type);

    int rc = SQLITE_BUSY;
    time_t start_time = time(NULL);
    bool column_exists;
    while (rc == SQLITE_BUSY && time(NULL) < start_time + 5) {
        sqlite3_busy_timeout(self->db, 5000);
        column_exists = sim_db_column_exists(self, column);
        if (column_exists || self->have_timed_out) {
            rc = SQLITE_OK;
        } else {
            sqlite3_busy_timeout(self->db, 0);
            rc = sqlite3_exec(self->db, query, NULL, NULL, NULL);
            if (rc == SQLITE_ERROR) {
                char* errmsg = malloc((strlen(sqlite3_errmsg(self->db)) + 1)
                                      * sizeof(char));
                strcpy(errmsg, sqlite3_errmsg(self->db));
                if (strstr(errmsg, "duplicate column name:") == errmsg) {
                    rc = SQLITE_OK;
                }
                free(errmsg);
            }
        }
        sqlite3_busy_timeout(self->db, 5000);
    }
    free(query);
    if (rc != SQLITE_OK
        && !sim_db_busy_database(self, rc, __func__, __LINE__)) {
        fprintf(stderr,
                "Error in function %s at line no. %d.\nERROR: Could "
                "NOT perform the SQLite3 query: '%s'\nSQLite3 "
                "error "
                "message:\n%s\n",
                __func__, __LINE__, query, sqlite3_errmsg(self->db));
        exit(EXIT_FAILURE);
    }
}

void sim_db_write_int(SimDB* self, const char* column, int value,
                      bool only_if_empty) {
    sim_db_add_column_if_not_exists(self, column, "INTEGER");
    char string_value[100];
    sprintf(string_value, "%d", value);
    sim_db_update(self, column, string_value, only_if_empty);
}

void sim_db_write_double(SimDB* self, const char* column, double value,
                         bool only_if_empty) {
    sim_db_add_column_if_not_exists(self, column, "REAL");
    char string_value[100];
    sprintf(string_value, "%0.17g", value);
    sim_db_update(self, column, string_value, only_if_empty);
}

void sim_db_write_string(SimDB* self, const char* column, const char* value,
                         bool only_if_empty) {
    sim_db_add_column_if_not_exists(self, column, "TEXT");
    char* escaped_string = sim_db_escape_quote_with_two_quotes(value);
    sim_db_update(self, column, escaped_string, only_if_empty);
    free(escaped_string);
}

void sim_db_write_bool(SimDB* self, const char* column, bool value,
                       bool only_if_empty) {
    sim_db_add_column_if_not_exists(self, column, "TEXT");
    char string_value[6];
    if (value) {
        strcpy(string_value, "True");
    } else {
        strcpy(string_value, "False");
    }
    sim_db_update(self, column, string_value, only_if_empty);
}

void sim_db_write_int_array(SimDB* self, const char* column, int* arr,
                            size_t len, bool only_if_empty) {
    sim_db_add_column_if_not_exists(self, column, "TEXT");
    size_t len_string = 20;
    char* string_value = malloc((len_string + 1) * sizeof(char));
    strcpy(string_value, "int[");
    size_t n_chars = 4;
    char number[100];
    for (size_t i = 0; i < len; i++) {
        sprintf(number, "%d, ", arr[i]);
        n_chars += strlen(number);
        if (n_chars >= len_string) {
            len_string *= 2;
            string_value = (char*) realloc(string_value,
                                           (len_string + 1) * sizeof(char));
        }
        strcat(string_value, number);
    }
    if (len > 0) {
        string_value[n_chars - 2] = ']';
        string_value[n_chars - 1] = '\0';
    } else {
        strcat(string_value, "]");
    }
    sim_db_update(self, column, string_value, only_if_empty);
    free(string_value);
}

void sim_db_write_double_array(SimDB* self, const char* column, double* arr,
                               size_t len, bool only_if_empty) {
    sim_db_add_column_if_not_exists(self, column, "TEXT");
    size_t len_string = 20;
    char* string_value = malloc((len_string + 1) * sizeof(char));
    strcpy(string_value, "float[");
    size_t n_chars = 6;
    char number[100];
    for (size_t i = 0; i < len; i++) {
        sprintf(number, "%0.17g, ", arr[i]);
        n_chars += strlen(number);
        if (n_chars >= len_string) {
            len_string *= 2;
            string_value = (char*) realloc(string_value,
                                           (len_string + 1) * sizeof(char));
        }
        strcat(string_value, number);
    }
    if (len > 0) {
        string_value[n_chars - 2] = ']';
        string_value[n_chars - 1] = '\0';
    } else {
        strcat(string_value, "]");
    }
    sim_db_update(self, column, string_value, only_if_empty);
    free(string_value);
}

void sim_db_write_string_array(SimDB* self, const char* column, char** arr,
                               size_t len, bool only_if_empty) {
    sim_db_add_column_if_not_exists(self, column, "TEXT");
    size_t len_string = 80;
    char* string_value = malloc((len_string + 1) * sizeof(char*));
    strcpy(string_value, "string[");
    size_t n_chars = 7;
    for (size_t i = 0; i < len; i++) {
        n_chars += strlen(arr[i]) + 2;
        if (n_chars >= len_string) {
            len_string *= 2;
            string_value = (char*) realloc(string_value,
                                           (len_string + 1) * sizeof(char));
        }
        strcat(string_value, arr[i]);
        strcat(string_value, ", ");
    }
    if (len > 0) {
        string_value[n_chars - 2] = ']';
        string_value[n_chars - 1] = '\0';
    } else {
        strcat(string_value, "]");
    }
    sim_db_update(self, column, string_value, only_if_empty);
    free(string_value);
}

void sim_db_write_bool_array(SimDB* self, const char* column, bool* arr,
                             size_t len, bool only_if_empty) {
    sim_db_add_column_if_not_exists(self, column, "TEXT");
    size_t len_string = 80;
    char* string_value = malloc((len_string + 1) * sizeof(char*));
    strcpy(string_value, "bool[");
    size_t n_chars = 5;
    for (size_t i = 0; i < len; i++) {
        if (arr[i]) {
            n_chars += 6;
        } else {
            n_chars += 7;
        }
        if (n_chars >= len_string) {
            len_string *= 2;
            string_value = (char*) realloc(string_value,
                                           (len_string + 1) * sizeof(char));
        }
        if (arr[i]) {
            strcat(string_value, "True, ");
        } else {
            strcat(string_value, "False, ");
        }
    }
    if (len > 0) {
        string_value[n_chars - 2] = ']';
        string_value[n_chars - 1] = '\0';
    } else {
        strcat(string_value, "]");
    }
    sim_db_update(self, column, string_value, only_if_empty);
    free(string_value);
}

void sim_db_set_empty(SimDB* self, const char* column) {
    sim_db_update(self, column, NULL, false);
}

char* sim_db_unique_results_dir_abs_path(SimDB* self,
                                         const char* abs_path_dir) {
    char* path_results_dir;
    if (!sim_db_is_empty(self, "results_dir")) {
        path_results_dir = sim_db_read_string(self, "results_dir");
        if (strstr(path_results_dir, "results_dir_is_currently_made_by_")
            != path_results_dir) {
            return path_results_dir;
        }
    }

    char unique_thread_process_name[200];
    strcpy(unique_thread_process_name, "results_dir_is_currently_made_by_");
    sprintf(unique_thread_process_name + strlen(unique_thread_process_name),
            "%u_%p", getpid(), pthread_self());
    sim_db_write_string(self, "results_dir", unique_thread_process_name, true);

    if (strcmp(unique_thread_process_name,
               sim_db_read_string(self, "results_dir"))
        == 0) {
        char time_string[100];
        sim_db_get_time_string(time_string);
        char* name = sim_db_read_string(self, "name");
        char* results_dir = malloc((PATH_MAX + 1) * sizeof(char));
        if (strlen(abs_path_dir) > PATH_MAX) {
            fprintf(stderr,
                    "Error in function %s at line no. %d.\nERROR: "
                    "'abs_path_dir' can NOT be longer than %d "
                    "characters.\n",
                    __func__, __LINE__, PATH_MAX);
            exit(EXIT_FAILURE);
        }
        if (abs_path_dir[strlen(abs_path_dir) - 1] == '/') {
            sprintf(results_dir, "%s%s_%s_%d", abs_path_dir, time_string, name,
                    self->id);
        } else {
            sprintf(results_dir, "%s/%s_%s_%d", abs_path_dir, time_string, name,
                    self->id);
        }
        struct stat st;
        if (stat(results_dir, &st) == 0) {
            strcat(results_dir, "__no2");
            while (stat(results_dir, &st) == 0) {
                char* ending_num = strstr(results_dir, "__no") + 4;
                int new_num = atoi(ending_num) + 1;
                ending_num[0] = '\0';
                sprintf(results_dir, "%s%d", results_dir, new_num);
            }
        }

        if (mkdir(results_dir, 0700)) {
            fprintf(stderr,
                    "Error in function %s at line no. %d.\nERROR: Could "
                    "NOT "
                    "create subdirectory %s\n",
                    __func__, __LINE__, results_dir);
            exit(EXIT_FAILURE);
        }
        sim_db_add_pointer_to_free(self, results_dir);
        sim_db_write_string(self, "results_dir", results_dir, false);

        return results_dir;
    } else {
        char* results_dir = sim_db_read_string(self, "results_dir");
        while (strstr(results_dir, "results_dir_is_currently_made_by_")
               == results_dir) {
            sim_db_free(self, results_dir);
            results_dir = sim_db_read_string(self, "results_dir");
        }
        sim_db_add_pointer_to_free(self, results_dir);
        return results_dir;
    }
}

char* sim_db_unique_results_dir(SimDB* self, const char* path_to_dir) {
    char path_res_dir[PATH_MAX + 1];
    if (strlen(path_to_dir) >= 5 && strncmp(path_to_dir, "root/", 5) == 0) {
        path_to_dir += 5;
        if (strlen(path_to_dir) + strlen(path_to_dir) <= PATH_MAX) {
            strcpy(path_res_dir, self->path_proj_root);
            strcat(path_res_dir, "/");
            strcat(path_res_dir, path_to_dir);
        } else {
            fprintf(stderr,
                    "Error in function %s at line no. %d.\nERROR: "
                    "'path_to_dir' can NOT be longer than %d characters.\n",
                    __func__, __LINE__, PATH_MAX);
            exit(EXIT_FAILURE);
        }
    } else {
        if (strlen(path_to_dir) <= PATH_MAX) {
            sprintf(path_res_dir, "%s", path_to_dir);
        } else {
            fprintf(stderr,
                    "Error in function %s at line no. %d.\nERROR: "
                    "'path_to_dir' can NOT be longer than %d characters.\n",
                    __func__, __LINE__, PATH_MAX);
            exit(EXIT_FAILURE);
        }
    }

    char real_path_res_dir[PATH_MAX + 1];
    if (!realpath(path_res_dir, real_path_res_dir)) {
        fprintf(stderr, "ERROR: Could NOT make realpath of %s\n.",
                real_path_res_dir);
    }

    return sim_db_unique_results_dir_abs_path(self, real_path_res_dir);
}

void sim_db_update_sha1_executables(SimDB* self, char** paths_executables,
                                    size_t len, bool only_if_empty) {
    const size_t len_sha1 = 40;
    char sha1[len_sha1 + 1];
    memset(sha1, 0, len_sha1 * sizeof(char));
    char tmp[len_sha1 + 1];
    char command[4200];
    char path_exec[PATH_MAX + 1];
    for (size_t i = 0; i < len; i++) {
        strcpy(path_exec, paths_executables[i]);
        sim_db_backslash_unslashed_spaces(path_exec);
        sprintf(command, "git hash-object %s", path_exec);
        sim_db_run_shell_command(command, tmp, len_sha1);
        for (size_t j = 0; j < len_sha1; j++) {
            sha1[j] = sha1[j] ^ tmp[j];
        }
    }
    sha1[40] = '\0';
    sim_db_update(self, "sha1_executables", sha1, only_if_empty);
}

int sim_db_get_id(SimDB* self) { return self->id; }

char* sim_db_get_path_proj_root(SimDB* self) {
    char* path_proj_root =
            malloc(sizeof(char) * (strlen(self->path_proj_root) + 1));
    sim_db_add_pointer_to_free(self, path_proj_root);
    strcpy(path_proj_root, self->path_proj_root);
    return path_proj_root;
}

void sim_db_delete_from_database(SimDB* self) {
    char path_database[PATH_MAX + 1];
    strcpy(path_database, self->path_proj_root);
    int len_path_database = strlen(path_database);
    if (len_path_database > 0 && path_database[len_path_database - 1] == '/') {
        path_database[len_path_database - 1] = '\0';
    }
    strcat(path_database, "/.sim_db/sim.db");

    char query[80];
    sprintf(query, "DELETE FROM runs WHERE \"id\" = %d", self->id);
    int rc = sqlite3_exec(self->db, query, NULL, NULL, NULL);

    if (rc != SQLITE_OK
        && !sim_db_busy_database(self, rc, __func__, __LINE__)) {
        fprintf(stderr,
                "Error in function %s at line no. %d.\nERROR: Could NOT "
                "perform the SQLite3 query: %s\nSQLite3 error "
                "message:\n%s\n",
                __func__, __LINE__, query, sqlite3_errmsg(self->db));
        exit(EXIT_FAILURE);
    }
}

void sim_db_dtor(SimDB* self) {
    if (self->store_metadata) {
        double used_time = difftime(time(NULL), self->start_time);
        char used_time_string[100];
        sprintf(used_time_string, "%dh %dm %fs", (int) used_time / 3600,
                (int) used_time / 60, fmod(used_time, 60));
        self->allow_timeouts = true;
        sim_db_update(self, "used_walltime", used_time_string, true);
    }
    for (size_t i = 0; i < self->n_pointers; i++) {
        free(self->pointers_to_free[i]);
    }
    free(self->pointers_to_free);
    sim_db_free_column_names(self->column_names);
    sqlite3_close(self->db);
}

const char* sim_db_get_create_table_query() {
    return "CREATE TABLE IF NOT EXISTS runs (id INTEGER PRIMARY KEY, "
           "status TEXT, name TEXT, description TEXT, run_command TEXT, "
           "comment TEXT, results_dir TEXT, add_to_job_script TEXT, "
           "max_walltime TEXT, n_tasks INTEGER, job_id INTEGER, "
           "time_submitted TEXT, time_started TEXT, used_walltime TEXT, "
           "cpu_info TEXT, git_hash TEXT, commit_message TEXT, "
           "git_diff_stat TEXT, git_diff TEXT, sha1_executables TEXT, "
           "inital_parameters TEXT)";
}

SimDB* sim_db_add_empty_sim_without_search(const char* path_proj_root,
                                           bool store_metadata) {
    char path_database[PATH_MAX + 1];
    strcpy(path_database, path_proj_root);
    int len_path_database = strlen(path_database);
    if (len_path_database > 0 && path_database[len_path_database - 1] == '/') {
        path_database[len_path_database - 1] = '\0';
    }
    strcat(path_database, "/.sim_db/sim.db");
    sqlite3* db;
    int rc = sqlite3_open_v2(
            path_database, &db,
            SQLITE_OPEN_READWRITE | SQLITE_OPEN_CREATE | SQLITE_OPEN_FULLMUTEX,
            NULL);
    if (rc != SQLITE_OK) {
        fprintf(stderr,
                "Error in function %s at line no. %d.\nERROR: Can NOT open "
                "database '%s': %s\n",
                __func__, __LINE__, path_database, sqlite3_errmsg(db));
        exit(EXIT_FAILURE);
    }
    sqlite3_busy_timeout(db, 5000);
    rc = sqlite3_exec(db, sim_db_get_create_table_query(), NULL, NULL, NULL);
    if (rc == SQLITE_BUSY) {
        sqlite3_close(db);
        SimDB sim_db_init = {.db = NULL,
                             .id = -1,
                             .buffer_size_pointers = 0,
                             .pointers_to_free = NULL,
                             .n_pointers = 0,
                             .store_metadata = false,
                             .start_time = 0,
                             .allow_timeouts = true,
                             .have_timed_out = true};
        SimDB* sim_db = malloc(sizeof(SimDB));
        memcpy(sim_db, &sim_db_init, sizeof(SimDB));
        sim_db->column_names.size = 0;
        sim_db->column_names.array = NULL;
        return sim_db;
    } else if (rc != SQLITE_OK) {
        fprintf(stderr,
                "Error in function %s at line no. %d.\nERROR: Could NOT "
                "perform the SQLite3 query: %s\nSQLite3 error "
                "message:\n%s\n",
                __func__, __LINE__, sim_db_get_create_table_query(),
                sqlite3_errmsg(db));
        exit(EXIT_FAILURE);
    }
    rc = sqlite3_exec(db, "INSERT INTO runs DEFAULT VALUES", NULL, NULL, NULL);
    if (rc == SQLITE_BUSY) {
        sqlite3_close(db);
        SimDB sim_db_init = {.db = NULL,
                             .id = -1,
                             .buffer_size_pointers = 0,
                             .pointers_to_free = NULL,
                             .n_pointers = 0,
                             .store_metadata = false,
                             .start_time = 0,
                             .allow_timeouts = true,
                             .have_timed_out = true};
        SimDB* sim_db = malloc(sizeof(SimDB));
        memcpy(sim_db, &sim_db_init, sizeof(SimDB));
        sim_db->column_names.size = 0;
        sim_db->column_names.array = NULL;
        return sim_db;
    } else if (rc != SQLITE_OK) {
        fprintf(stderr,
                "Error in function %s at line no. %d.\nERROR: Could NOT "
                "perform the SQLite3 query: INSERT INTO runs DEFAULT "
                "VALUES\nSQLite3 error message:\n%s\n",
                __func__, __LINE__, sqlite3_errmsg(db));
        exit(EXIT_FAILURE);
    }
    int id = (int) sqlite3_last_insert_rowid(db);
    sqlite3_close(db);

    return sim_db_ctor_without_search(path_proj_root, id, store_metadata);
}

SimDB* sim_db_add_empty_sim(bool store_metadata) {
    char path_proj_root[PATH_MAX + 1];
    sim_db_find_path_proj_root(path_proj_root, PATH_MAX + 1);
    return sim_db_add_empty_sim_without_search(path_proj_root, store_metadata);
}
