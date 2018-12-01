// Copyright (C) 2018 Håkon Austlid Taskén <hakon.tasken@gmail.com>
// Licensed under the MIT License.

#define _XOPEN_SOURCE 500

#include "../include/sim_db.h"
#include <ctype.h>
#include <limits.h>
#include <math.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <time.h>
#include <unistd.h>
#include "../third_party/sqlite3/sqlite3.h"

#ifndef PATH_MAX
#define PATH_MAX
#endif

struct SimDB {
    sqlite3* db;
    int id;
    char path_proj_root[PATH_MAX + 1];
    bool store_metadata;
    time_t start_time;
    void** pointers_to_free;
    size_t n_pointers;
    size_t buffer_size_pointers;
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

// Return EXIT_SUCCESS if pointer is found in SimDB.pointers_to_free and freed
int sim_db_free(SimDB* self, void* pointer) {
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
    return EXIT_SUCCESS;
}

void backslash_unslashed_spaces(char path[PATH_MAX + 1]) {
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

void sim_db_update(SimDB* self, const char* column, const char* value) {
    char* query = (char*) malloc(sizeof(char)
                                 * (strlen(column) + strlen(value) + 80));
    sprintf(query, "UPDATE runs SET '%s' = '%s' WHERE id = %d", column, value,
            self->id);
    int rc = sqlite3_exec(self->db, query, NULL, NULL, NULL);
    free(query);
    if (rc != SQLITE_OK) {
        fprintf(stderr,
                "Error in function %s at line %d.\nERROR: Could NOT perform "
                "the SQLite3 query: '%s'\n",
                __func__, __LINE__, query);
        exit(1);
    }
}

// Return EXIT_SUCCESS if file can be opened
int sim_db_run_shell_command(const char* command, char* output,
                             size_t len_output) {
    FILE* file;
    file = popen(command, "r");
    size_t i = 0;
    int c;
    if (file) {
        while ((c = getc(file)) != EOF && i <= len_output) {
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

bool is_a_git_project(char path_dot_sim_db_parent_dir[PATH_MAX + 1]) {
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
    char* escaped_string =
            (char*) malloc(2 * (strlen(string) + 1) * sizeof(char));
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
                        "Error in function %s at line %d.\nERROR: "
                        "'--path_proj_root' can NOT be longer than %d.\n",
                        __func__, __LINE__, PATH_MAX);
                exit(1);
            }
        }
        if (is_id_found && is_path_proj_root_found) {
            break;
        }
    }
    if (!is_id_found) {
        fprintf(stderr,
                "Error in function %s at line %d.\nERROR: '--id ID' or '-i "
                "ID' MUST be passed as command line arguments.\n",
                __func__, __LINE__);
        exit(1);
    }
    if (!is_path_proj_root_found) {
        if (getcwd(path_proj_root, sizeof(char) * (PATH_MAX + 1))) {
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
                        "Error in function %s at line %d.\nERROR: Could "
                        "NOT find '.sim_db/settings.txt' in this or any "
                        "parents directories.\nRun '$ init' in the "
                        "project's root directory.\n",
                        __func__, __LINE__);
                exit(1);
            }
        } else {
            fprintf(stderr,
                    "Error in function %s at line %d.\nERROR: getcwd() did "
                    "NOT work.",
                    __func__, __LINE__);
        }
    }

    SimDB* sim_db = sim_db_ctor_with_id(path_proj_root, id, store_metadata);

    if (store_metadata) {
        int len_path_proj_root = strlen(path_proj_root);
        if (len_path_proj_root > 0
            && path_proj_root[len_path_proj_root - 1] == '/') {
            path_proj_root[len_path_proj_root - 1] = '\0';
        }
        if (is_a_git_project(path_proj_root)) {
            char* program_name[1];
            program_name[0] = argv[0];
            sim_db_update_sha1_executables(sim_db, program_name, 1);
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

SimDB* sim_db_ctor_with_id(const char* path_proj_root, int id,
                           bool store_metadata) {
    char path_database[PATH_MAX + 1];
    int len_path_proj_root = strlen(path_proj_root);
    if (len_path_proj_root <= PATH_MAX) {
        strcpy(path_database, path_proj_root);
    } else {
        fprintf(stderr,
                "Error in function %s at line %d.\nERROR: 'path_proj_root' "
                "can NOT be longer than %d.\n",
                __func__, __LINE__, PATH_MAX);
        exit(1);
    }
    sqlite3* db;
    if (len_path_proj_root > 0
        && path_database[len_path_proj_root - 1] == '/') {
        path_database[len_path_proj_root - 1] = '\0';
    }
    strcat(path_database, "/.sim_db/sim.db");
    int rc = sqlite3_open(path_database, &db);
    if (rc != SQLITE_OK) {
        fprintf(stderr,
                "Error in function %s at line %d.\nERROR: Can NOT open "
                "database '%s': %s\n",
                __func__, __LINE__, path_database, sqlite3_errmsg(db));
        exit(1);
    }

    SimDB* sim_db = (SimDB*) malloc(sizeof(struct SimDB));
    sim_db->db = db;
    sim_db->id = id;
    path_database[strlen(path_database) - 15] = '\0';
    strcpy(sim_db->path_proj_root, path_database);
    sim_db->store_metadata = store_metadata;
    sim_db->start_time = time(NULL);
    sim_db->buffer_size_pointers = 5;
    sim_db->pointers_to_free =
            (void**) malloc(sim_db->buffer_size_pointers * sizeof(void*));
    sim_db->n_pointers = 0;

    if (store_metadata) {
        char time_started[80];
        sim_db_get_time_string(time_started);
        sim_db_update(sim_db, "time_started", time_started);
    }

    const size_t len_output = 3000;
    char output[len_output + 200];
    char command[4200];

    if (store_metadata && is_a_git_project(sim_db->path_proj_root)) {
        char path_proj_root_backslashed[PATH_MAX + 1];
        strcpy(path_proj_root_backslashed, sim_db->path_proj_root);
        backslash_unslashed_spaces(path_proj_root_backslashed);
        sprintf(command, "cd %s && git rev-parse HEAD",
                path_proj_root_backslashed);
        if (sim_db_run_shell_command(command, output, len_output) == 0) {
            sim_db_update(sim_db, "git_hash", output);
        }

        sprintf(command, "cd %s && git log -n --format=%%B HEAD",
                path_proj_root_backslashed);
        if (sim_db_run_shell_command(command, output, len_output) == 0) {
            char* escaped_string = sim_db_escape_quote_with_two_quotes(output);
            sim_db_update(sim_db, "commit_message", output);
            free(escaped_string);
        }

        sprintf(command, "cd %s && git diff HEAD --stat",
                path_proj_root_backslashed);
        if (sim_db_run_shell_command(command, output, len_output) == 0) {
            char* escaped_string = sim_db_escape_quote_with_two_quotes(output);
            sim_db_update(sim_db, "git_diff_stat", escaped_string);
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
                sim_db_update(sim_db, "git_diff", escaped_string);
                free(escaped_string);
            } else {
                char* escaped_string =
                        sim_db_escape_quote_with_two_quotes(output);
                sim_db_update(sim_db, "git_diff", escaped_string);
                free(escaped_string);
            }
        }
    }

    return sim_db;
}

int sim_db_read_int(SimDB* self, const char* column) {
    char query[256];
    sprintf(query, "SELECT %s FROM runs WHERE id = %d", column, self->id);
    sqlite3_stmt* stmt = NULL;
    int rc = sqlite3_prepare_v2(self->db, query, -1, &stmt, NULL);
    if (rc != SQLITE_OK) {
        fprintf(stderr,
                "Error in function %s at line %d.\nERROR: Could NOT "
                "perform the SQLite3 query: '%s'\n",
                __func__, __LINE__, query);
        exit(1);
    }
    rc = sqlite3_step(stmt);
    int result = -1;
    if (rc == SQLITE_ROW) {
        int type = sqlite3_column_type(stmt, 0);
        if (type != SQLITE_INTEGER) {
            fprintf(stderr,
                    "Error in function %s at line %d.\nERROR: Column %s is "
                    "NOT an int.\n",
                    __func__, __LINE__, column);
            exit(1);
        }
        result = sqlite3_column_int(stmt, 0);
    } else {
        fprintf(stderr,
                "Error in function %s at line %d.\nERROR: Could NOT read "
                "column=%s with id=%d form database.\n",
                __func__, __LINE__, column, self->id);
        exit(1);
    }
    sqlite3_finalize(stmt);
    return result;
}

double sim_db_read_double(SimDB* self, const char* column) {
    char query[256];
    sprintf(query, "SELECT %s FROM runs WHERE id = %d", column, self->id);
    sqlite3_stmt* stmt = NULL;
    int rc = sqlite3_prepare_v2(self->db, query, -1, &stmt, NULL);
    if (rc != SQLITE_OK) {
        fprintf(stderr,
                "Error in function %s at line %d.\nERROR: Could NOT "
                "perform the SQLite3 query: '%s'\n",
                __func__, __LINE__, query);
        exit(1);
    }
    rc = sqlite3_step(stmt);
    double result = -1.0;
    if (rc == SQLITE_ROW) {
        int type = sqlite3_column_type(stmt, 0);
        if (type != SQLITE_FLOAT) {
            fprintf(stderr,
                    "Error in function %s at line %d.\nERROR: Column %s is "
                    "NOT a float.\n",
                    __func__, __LINE__, column);
            exit(1);
        }
        result = sqlite3_column_double(stmt, 0);
    } else {
        fprintf(stderr,
                "Error in function %s at line %d.\nERROR: Could NOT read "
                "column=%s with id=%d form database.\n",
                __func__, __LINE__, column, self->id);
        exit(1);
    }
    sqlite3_finalize(stmt);
    return result;
}

char* sim_db_read_string(SimDB* self, const char* column) {
    char query[256];
    sprintf(query, "SELECT %s FROM runs WHERE id = %d", column, self->id);
    sqlite3_stmt* stmt = NULL;
    int rc = sqlite3_prepare_v2(self->db, query, -1, &stmt, NULL);
    if (rc != SQLITE_OK) {
        fprintf(stderr,
                "Error in function %s at line %d.\nERROR: Could NOT "
                "perform the SQLite3 query: '%s'\n",
                __func__, __LINE__, query);
        exit(1);
    }
    rc = sqlite3_step(stmt);
    char* text;
    if (rc == SQLITE_ROW) {
        int type = sqlite3_column_type(stmt, 0);
        if (type != SQLITE_TEXT) {
            fprintf(stderr,
                    "Error in function %s at line %d.\nERROR: Column %s is "
                    "NOT a string.\n",
                    __func__, __LINE__, column);
            exit(1);
        }
        text = (char*) sqlite3_column_text(stmt, 0);
    } else {
        fprintf(stderr,
                "Error in function %s at line %d.\nERROR: Could NOT read "
                "column=%s with id=%d for database.\n",
                __func__, __LINE__, column, self->id);
        exit(1);
    }
    char* string = (char*) malloc((strlen(text) + 1) * sizeof(char));
    strcpy(string, text);
    sqlite3_finalize(stmt);
    sim_db_add_pointer_to_free(self, string);
    return string;
}

bool sim_db_read_bool(SimDB* self, const char* column) {
    char* bool_string = sim_db_read_string(self, column);
    if (strcmp(bool_string, "True") == 0) {
        return true;
    } else if (strcmp(bool_string, "False") == 0) {
        return false;
    } else {
        fprintf(stderr,
                "Error in function %s at line %d.\nERROR: The value under "
                "column %s with id %d is NOT 'True' or 'False', but %s.\n",
                __func__, __LINE__, column, self->id, bool_string);
        exit(1);
    }
}

SimDBIntVec sim_db_read_int_vec(SimDB* self, const char* column) {
    char* int_arr_string = sim_db_read_string(self, column);
    if (strstr(int_arr_string, "int[") != int_arr_string) {
        fprintf(stderr,
                "Error in function %s at line %d.\nERROR: The type under "
                "column=%s with id=%d is NOT int array.\n",
                __func__, __LINE__, column, self->id);
        exit(1);
    }
    SimDBIntVec int_vec;
    int_vec.size = 5;
    int_vec.array = (int*) malloc(int_vec.size * sizeof(int));
    char number[100];
    size_t n_digits = 0;
    size_t n_numbers = 0;
    for (size_t i = 4; i < strlen(int_arr_string); i++) {
        if (int_arr_string[i] == ',' || int_arr_string[i] == ']') {
            number[n_digits] = '\0';
            if (n_numbers >= int_vec.size) {
                int* new_arr = (int*) malloc(2 * int_vec.size * sizeof(int));
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
    sim_db_add_pointer_to_free(self, int_vec.array);
    return int_vec;
}

SimDBDoubleVec sim_db_read_double_vec(SimDB* self, const char* column) {
    char* double_arr_string = sim_db_read_string(self, column);
    if (strstr(double_arr_string, "float[") != double_arr_string) {
        fprintf(stderr,
                "Error in function %s at line %d.\nERROR: The type under "
                "column=%s with id=%d is NOT double array.\n",
                __func__, __LINE__, column, self->id);
        exit(1);
    }
    SimDBDoubleVec double_vec;
    double_vec.size = 5;
    double_vec.array = (double*) malloc(double_vec.size * sizeof(double));
    char number[100];
    size_t n_digits = 0;
    size_t n_numbers = 0;
    for (size_t i = 6; i < strlen(double_arr_string); i++) {
        if (double_arr_string[i] == ',' || double_arr_string[i] == ']') {
            number[n_digits] = '\0';
            if (n_numbers >= double_vec.size) {
                double* new_arr =
                        (double*) malloc(2 * double_vec.size * sizeof(int));
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
    sim_db_add_pointer_to_free(self, double_vec.array);
    return double_vec;
}

SimDBStringVec sim_db_read_string_vec(SimDB* self, const char* column) {
    char* str_arr_string = sim_db_read_string(self, column);
    if (strstr(str_arr_string, "string[") != str_arr_string) {
        fprintf(stderr,
                "Error in function %s at line %d.\nERROR: The type under "
                "column=%s with id=%d is NOT string array.\n",
                __func__, __LINE__, column, self->id);
        exit(1);
    }
    SimDBStringVec string_vec;
    string_vec.size = 5;
    string_vec.array = (char**) malloc(string_vec.size * sizeof(char*));
    char string[100];
    size_t n_char = 0;
    size_t n_strings = 0;
    for (size_t i = 7; i < strlen(str_arr_string); i++) {
        if (str_arr_string[i] == ',' || str_arr_string[i] == ']') {
            string[n_char] = '\0';
            if (n_strings >= string_vec.size) {
                char** new_arr =
                        (char**) malloc(2 * string_vec.size * sizeof(char*));
                memcpy(new_arr, string_vec.array,
                       string_vec.size * sizeof(char*));
                string_vec.size *= 2;
                free(string_vec.array);
                string_vec.array = new_arr;
            }
            string_vec.array[n_strings] =
                    (char*) malloc((strlen(string) + 1) * sizeof(char));
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
                "Error in function %s at line %d.\nERROR: The type under "
                "column=%s with id=%d is NOT double array.\n",
                __func__, __LINE__, column, self->id);
        exit(1);
    }
    SimDBBoolVec bool_vec;
    bool_vec.size = 5;
    bool_vec.array = (bool*) malloc(bool_vec.size * sizeof(bool));
    char bool_str[100];
    size_t n_char = 0;
    size_t n_bools = 0;
    for (size_t i = 5; i < strlen(bool_arr_str); i++) {
        if (bool_arr_str[i] == ',' || bool_arr_str[i] == ']') {
            bool_str[n_char] = '\0';
            if (n_bools >= bool_vec.size) {
                bool* new_arr =
                        (bool*) malloc(2 * bool_vec.size * sizeof(bool));
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
                        "Error in function %s at line %d.\nERROR: A value "
                        "in the array  under column %s with id %d is NOT "
                        "'True' or 'False', but %s.\n",
                        __func__, __LINE__, column, self->id, bool_str);
                exit(1);
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
    sim_db_add_pointer_to_free(self, bool_vec.array);
    return bool_vec;
}

SimDBStringVec sim_db_get_column_names(SimDB* self) {
    /*sim_db_free_column_names NEEDS to be called to free return value.*/
    char query[256];
    sprintf(query, "SELECT * FROM runs WHERE id = %d;", self->id);
    sqlite3_stmt* stmt = NULL;
    int rc = sqlite3_prepare_v2(self->db, query, -1, &stmt, NULL);
    if (rc != SQLITE_OK) {
        fprintf(stderr,
                "Error in function %s at line %d.\nERROR: Could NOT "
                "perform the SQLite3 query: '%s'\n",
                __func__, __LINE__, query);
        exit(1);
    }
    rc = sqlite3_step(stmt);
    SimDBStringVec column_names;
    column_names.size = 5;
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
            column_names.array[i] =
                    (char*) malloc((strlen(column) + 1) * sizeof(char));
            strcpy(column_names.array[i], column);
            column = (char*) sqlite3_column_name(stmt, ++i);
        }
        column_names.size = i;
    } else {
        fprintf(stderr,
                "Error in function %s at line %d.\nERROR: Could NOT read "
                "from database\n",
                __func__, __LINE__);
        exit(1);
    }
    sqlite3_finalize(stmt);

    return column_names;
}

void sim_db_free_column_names(SimDBStringVec column_names) {
    for (size_t i = 0; i < column_names.size; i++) {
        free(column_names.array[i]);
    }
    free(column_names.array);
}

bool sim_db_column_exists(SimDB* self, const char* column) {
    SimDBStringVec columns = sim_db_get_column_names(self);
    for (size_t i = 0; i < columns.size; i++) {
        if (strcmp(column, columns.array[i]) == 0) {
            sim_db_free_column_names(columns);
            return true;
        }
    }
    sim_db_free_column_names(columns);
    return false;
}

void sim_db_add_column_if_not_exists(SimDB* self, const char* column,
                                     const char* type) {
    if (!sim_db_column_exists(self, column)) {
        char query[256];
        sprintf(query, "ALTER TABLE runs ADD COLUMN '%s' %s", column, type);
        int rc = sqlite3_exec(self->db, query, NULL, NULL, NULL);
        if (rc != SQLITE_OK) {
            fprintf(stderr,
                    "Error in function %s at line %d.\nERROR: Could "
                    "NOT "
                    "perform the SQLite3 query: '%s'\n",
                    __func__, __LINE__, query);
            exit(1);
        }
    }
}

void sim_db_write_int(SimDB* self, const char* column, int value) {
    sim_db_add_column_if_not_exists(self, column, "INTEGER");
    char string_value[100];
    sprintf(string_value, "%d", value);
    sim_db_update(self, column, string_value);
}

void sim_db_write_double(SimDB* self, const char* column, double value) {
    sim_db_add_column_if_not_exists(self, column, "REAL");
    char string_value[100];
    sprintf(string_value, "%0.17g", value);
    sim_db_update(self, column, string_value);
}

void sim_db_write_string(SimDB* self, const char* column, const char* value) {
    sim_db_add_column_if_not_exists(self, column, "TEXT");
    char* escaped_string = sim_db_escape_quote_with_two_quotes(value);
    sim_db_update(self, column, escaped_string);
    free(escaped_string);
}

void sim_db_write_bool(SimDB* self, const char* column, bool value) {
    sim_db_add_column_if_not_exists(self, column, "TEXT");
    char string_value[6];
    if (value) {
        strcpy(string_value, "True");
    } else {
        strcpy(string_value, "False");
    }
    sim_db_update(self, column, string_value);
}

void sim_db_write_int_array(SimDB* self, const char* column, int* arr,
                            size_t len) {
    sim_db_add_column_if_not_exists(self, column, "TEXT");
    size_t len_string = 20;
    char* string_value = (char*) malloc((len_string + 1) * sizeof(char));
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
    sim_db_update(self, column, string_value);
    free(string_value);
}

void sim_db_write_double_array(SimDB* self, const char* column, double* arr,
                               size_t len) {
    sim_db_add_column_if_not_exists(self, column, "TEXT");
    size_t len_string = 20;
    char* string_value = (char*) malloc((len_string + 1) * sizeof(char));
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
    sim_db_update(self, column, string_value);
    free(string_value);
}

void sim_db_write_string_array(SimDB* self, const char* column, char** arr,
                               size_t len) {
    sim_db_add_column_if_not_exists(self, column, "TEXT");
    size_t len_string = 80;
    char* string_value = (char*) malloc((len_string + 1) * sizeof(char*));
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
    sim_db_update(self, column, string_value);
    free(string_value);
}

void sim_db_write_bool_array(SimDB* self, const char* column, bool* arr,
                             size_t len) {
    sim_db_add_column_if_not_exists(self, column, "TEXT");
    size_t len_string = 80;
    char* string_value = (char*) malloc((len_string + 1) * sizeof(char*));
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
    sim_db_update(self, column, string_value);
    free(string_value);
}

char* sim_db_make_unique_subdir_abs_path(SimDB* self,
                                         const char* abs_path_to_results_dir) {
    char time_string[100];
    sim_db_get_time_string(time_string);
    char* name = sim_db_read_string(self, "name");
    char* name_subdir = (char*) malloc((PATH_MAX + 1) * sizeof(char));
    if (strlen(abs_path_to_results_dir) > PATH_MAX) {
        fprintf(stderr,
                "Error in function %s at line %d.\nERROR: "
                "'abs_path_to_results_dir' can NOT be longer than %d "
                "characters.\n",
                __func__, __LINE__, PATH_MAX);
        exit(1);
    }
    if (abs_path_to_results_dir[strlen(abs_path_to_results_dir) - 1] == '/') {
        sprintf(name_subdir, "%s%s_%s_%d", abs_path_to_results_dir, time_string,
                name, self->id);
    } else {
        sprintf(name_subdir, "%s/%s_%s_%d", abs_path_to_results_dir,
                time_string, name, self->id);
    }
    struct stat st;
    if (stat(name_subdir, &st) == 0) {
        strcat(name_subdir, "__no2");
        while (stat(name_subdir, &st) == 0) {
            char* ending_num = strstr(name_subdir, "__no") + 4;
            int new_num = atoi(ending_num) + 1;
            ending_num[0] = '\0';
            sprintf(name_subdir, "%s%d", name_subdir, new_num);
        }
    }
    if (mkdir(name_subdir, 0700)) {
        fprintf(stderr,
                "Error in function %s at line %d.\nERROR: Could NOT "
                "create "
                "subdirectory %s\n",
                __func__, __LINE__, name_subdir);
        exit(1);
    }
    sim_db_add_pointer_to_free(self, name_subdir);

    if (self->store_metadata) {
        sim_db_write_string(self, "results_dir", name_subdir);
    }

    return name_subdir;
}

char* sim_db_make_unique_subdir(SimDB* self, const char* path_to_results_dir) {
    char path_res_dir[PATH_MAX + 1];
    if (strlen(path_to_results_dir) >= 5
        && strncmp(path_to_results_dir, "root/", 5) == 0) {
        path_to_results_dir += 5;
        if (strlen(path_to_results_dir) + strlen(path_to_results_dir)
            <= PATH_MAX) {
            strcpy(path_res_dir, self->path_proj_root);
            strcat(path_res_dir, "/");
            strcat(path_res_dir, path_to_results_dir);
        } else {
            fprintf(stderr,
                    "Error in function %s at line %d.\nERROR: "
                    "'path_to_results_dir' can NOT be longer than %d "
                    "characters.\n",
                    __func__, __LINE__, PATH_MAX);
            exit(1);
        }
    } else {
        if (strlen(path_to_results_dir) <= PATH_MAX) {
            sprintf(path_res_dir, "%s", path_to_results_dir);
        } else {
            fprintf(stderr,
                    "Error in function %s at line %d.\nERROR: "
                    "'path_to_results_dir' can NOT be longer than %d "
                    "characters.\n",
                    __func__, __LINE__, PATH_MAX);
            exit(1);
        }
    }

    char real_path_res_dir[PATH_MAX + 1];
    if (!realpath(path_res_dir, real_path_res_dir)) {
        fprintf(stderr, "ERROR: Could NOT make realpath of %s\n.",
                real_path_res_dir);
    }

    return sim_db_make_unique_subdir_abs_path(self, real_path_res_dir);
}

void sim_db_update_sha1_executables(SimDB* self, char** paths_executables,
                                    size_t len) {
    const size_t len_sha1 = 40;
    char sha1[len_sha1 + 1];
    memset(sha1, 0, len_sha1 * sizeof(char));
    char tmp[len_sha1 + 1];
    char command[4200];
    char path_exec[PATH_MAX + 1];
    for (size_t i = 0; i < len; i++) {
        strcpy(path_exec, paths_executables[i]);
        backslash_unslashed_spaces(path_exec);
        sprintf(command, "git hash-object %s", path_exec);
        sim_db_run_shell_command(command, tmp, len_sha1);
        for (size_t j = 0; j < len_sha1; j++) {
            sha1[j] = sha1[j] ^ tmp[j];
        }
    }
    sha1[40] = '\0';
    sim_db_update(self, "sha1_executables", sha1);
}

int sim_db_get_id(SimDB* self) { return self->id; }

char* sim_db_get_path_proj_root(SimDB* self) {
    char* path_proj_root =
            (char*) malloc(sizeof(char) * (strlen(self->path_proj_root) + 1));
    sim_db_add_pointer_to_free(self, path_proj_root);
    strcpy(path_proj_root, self->path_proj_root);
    return path_proj_root;
}

void sim_db_dtor(SimDB* self) {
    if (self->store_metadata) {
        double used_time = difftime(time(NULL), self->start_time);
        char used_time_string[100];
        sprintf(used_time_string, "%dh %dm %fs", (int) used_time / 3600,
                (int) used_time / 60, fmod(used_time, 60));
        sim_db_update(self, "used_walltime", used_time_string);
    }
    for (size_t i = 0; i < self->n_pointers; i++) {
        free(self->pointers_to_free[i]);
    }
    free(self->pointers_to_free);
    sqlite3_close(self->db);
}

const char* get_create_table_query() {
    return "CREATE TABLE IF NOT EXISTS runs (id INTEGER PRIMARY KEY, "
           "status TEXT, name TEXT, description TEXT, run_command "
           "TEXT, "
           "comment TEXT, results_dir TEXT, add_to_job_script TEXT, "
           "max_walltime TEXT, n_tasks INTEGER, job_id INTEGER, "
           "time_submitted TEXT, time_started TEXT, used_walltime "
           "TEXT, "
           "cpu_info TEXT, git_hash TEXT, commit_message TEXT, "
           "git_diff_stat TEXT, git_diff TEXT, sha1_executables TEXT)";
}

int add_empty_sim(const char* path_proj_root) {
    char path_database[PATH_MAX + 1];
    strcpy(path_database, path_proj_root);
    int len_path_database = strlen(path_database);
    if (len_path_database > 0 && path_database[len_path_database - 1] == '/') {
        path_database[len_path_database - 1] = '\0';
    }
    strcat(path_database, "/.sim_db/sim.db");
    sqlite3* db;
    int rc = sqlite3_open(path_database, &db);
    if (rc != SQLITE_OK) {
        fprintf(stderr,
                "Error in function %s at line %d.\nERROR: Can NOT open "
                "database '%s': %s\n",
                __func__, __LINE__, path_database, sqlite3_errmsg(db));
        exit(1);
    }
    rc = sqlite3_exec(db, get_create_table_query(), NULL, NULL, NULL);
    if (rc != SQLITE_OK) {
        fprintf(stderr,
                "Error in function %s at line %d.\nERROR: Could NOT "
                "perform the SQLite3 query: %s\n",
                __func__, __LINE__, get_create_table_query());
        exit(1);
    }
    rc = sqlite3_exec(db, "INSERT INTO runs DEFAULT VALUES", NULL, NULL, NULL);
    if (rc != SQLITE_OK) {
        fprintf(stderr,
                "Error in function %s at line %d.\nERROR: Could NOT "
                "perform the SQLite3 query: INSERT INTO runs DEFAULT "
                "VALUES\n",
                __func__, __LINE__);
        exit(1);
    }
    int id = (int) sqlite3_last_insert_rowid(db);
    sqlite3_close(db);

    return id;
}

void delete_sim(const char* path_proj_root, int id) {
    char path_database[PATH_MAX + 1];
    strcpy(path_database, path_proj_root);
    int len_path_database = strlen(path_database);
    if (len_path_database > 0 && path_database[len_path_database - 1] == '/') {
        path_database[len_path_database - 1] = '\0';
    }
    strcat(path_database, "/.sim_db/sim.db");
    sqlite3* db;
    int rc = sqlite3_open(path_database, &db);
    if (rc != SQLITE_OK) {
        fprintf(stderr,
                "Error in function %s at line %d.\nERROR: Can NOT open "
                "database '%s': %s\n",
                __func__, __LINE__, path_database, sqlite3_errmsg(db));
        exit(1);
    }

    char query[80];
    sprintf(query, "DELETE FROM runs WHERE id = %d", id);
    rc = sqlite3_exec(db, query, NULL, NULL, NULL);
    if (rc != SQLITE_OK) {
        fprintf(stderr,
                "Error in function %s at line %d.\nERROR: Could NOT "
                "perform the SQLite3 query: %s\n",
                __func__, __LINE__, query);
        exit(1);
    }
    sqlite3_close(db);
}
