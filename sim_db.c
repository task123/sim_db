// Copyright (C) 2018 Håkon Austlid Taskén <hakon.tasken@gmail.com>
// Licensed under the MIT License.

#include "sim_db.h"
#include <ctype.h>
#include <math.h>
#include <sqlite3.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <time.h>
#include <unistd.h>

struct SimDB {
    sqlite3* db;
    int id;
    time_t start_time;
    void** pointers_to_free;
    size_t n_pointers;
    size_t buffer_size_pointers;
};

char* get_path_sim_db() {
    char path_sim_db[4097];
    getcwd(path_sim_db, sizeof(path_sim_db));
    strcat(path_sim_db, "/");
    strcat(path_sim_db, __FILE__);
    int position_last_slash = -1;
    char* result;
    for (int i = strlen(path_sim_db) - 1; i >= 0; i--) {
        if (path_sim_db[i] == '/') {
            path_sim_db[i] = '\0';
            result = (char*) malloc((strlen(path_sim_db) + 1) * sizeof(char));
            strcpy(result, path_sim_db);
            break;
        }
    }
    return result;
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
}

void sim_db_update(SimDB* self, const char* column, const char* value) {
    char query[256];
    sprintf(query, "UPDATE runs SET '%s' = '%s' WHERE id = %d", column, value,
            self->id);
    int rc = sqlite3_exec(self->db, query, NULL, NULL, NULL);
    if (rc != SQLITE_OK) {
        fprintf(stderr, "Could NOT perform the SQLite3 query: '%s'\n", query);
        exit(1);
    }
}

// Return 0 if file can be opened
int sim_db_run_shell_command(const char* command, char* output,
                             size_t len_output) {
    FILE* file;
    file = popen(command, "r");
    int i = 0;
    char c;
    if (file) {
        while ((c = getc(file)) != EOF && i <= len_output) output[i++] = c;
        fclose(file);
        output[i] = '\0';
    } else {
        pclose(file);
        return 1;
    }
    pclose(file);
    return 0;
}

SimDB* sim_db_ctor(int argc, char** argv) {
    int id = -1;
    bool is_found = false;
    int i = 0;
    for (; i < argc - 1; i++) {
        if ((strcmp(argv[i], "--id") == 0) || (strcmp(argv[i], "-i") == 0)) {
            is_found = true;
            id = atoi(argv[i + 1]);
            break;
        }
    }
    if (!is_found || (id == 0 && (strcmp(argv[i + 1], "0") != 0))) {
        fprintf(stderr,
                "ERROR: '--id ID' or '-i ID' MUST be passed as "
                "command line arguments.\n");
        exit(1);
    }
    SimDB* sim_db = sim_db_ctor_with_id(id);
    if (argc > 0) {
        char* program_name[1];
        program_name[0] = argv[0];
        sim_db_update_sha1_executables(sim_db, program_name, 1);
    }
    return sim_db;
}

SimDB* sim_db_ctor_with_id(int id) {
    sqlite3* db;
    char path_sim_db[4097];
    strcpy(path_sim_db, strcat(get_path_sim_db(), "/sim.db"));
    int rc = sqlite3_open(path_sim_db, &db);
    if (rc != SQLITE_OK) {
        fprintf(stderr, "Can NOT open database '%s': %s\n", get_path_sim_db(),
                sqlite3_errmsg(db));
        exit(1);
    }

    SimDB* sim_db = (SimDB*) malloc(sizeof(struct SimDB));
    sim_db->db = db;
    sim_db->id = id;
    sim_db->start_time = time(NULL);
    sim_db->buffer_size_pointers = 5;
    sim_db->pointers_to_free =
            (void**) malloc(sim_db->buffer_size_pointers * sizeof(void*));
    sim_db->n_pointers = 0;

    char time_started[80];
    sim_db_get_time_string(time_started);
    sim_db_update(sim_db, "time_started", time_started);

    const size_t len_output = 3000;
    char output[len_output + 200];
    char command[4200];
    sprintf(command, "cd %s/.. && git rev-parse HEAD", get_path_sim_db());
    if (sim_db_run_shell_command(command, output, len_output) == 0) {
        sim_db_update(sim_db, "git_hash", output);
    }

    sprintf(command, "cd %s/.. && git log -n --format=%%B HEAD",
            get_path_sim_db());
    if (sim_db_run_shell_command(command, output, len_output) == 0) {
        sim_db_update(sim_db, "commit_message", output);
    }

    sprintf(command, "cd %s/.. && git diff HEAD --stat", get_path_sim_db());
    if (sim_db_run_shell_command(command, output, len_output) == 0) {
        sim_db_update(sim_db, "git_diff_stat", output);
    }

    sprintf(command, "cd %s/.. && git diff HEAD", get_path_sim_db());
    if (sim_db_run_shell_command(command, output, len_output) == 0) {
        if (strlen(output) >= len_output) {
            char warning[len_output + 200];
            sprintf(warning,
                    "WARNING: Diff limited to first %ld "
                    "characters.\n",
                    (long) len_output);
            strcat(warning, "\n");
            strcat(warning, output);
            strcpy(output, warning);
            strcat(output, "\n\n");
            strcat(output, warning);
        }
        sim_db_update(sim_db, "git_diff", output);
    }

    return sim_db;
}

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

int sim_db_read_int(SimDB* self, const char* column) {
    char query[256];
    sprintf(query, "SELECT %s FROM runs WHERE id = %d", column, self->id);
    sqlite3_stmt* stmt = NULL;
    int rc = sqlite3_prepare_v2(self->db, query, -1, &stmt, NULL);
    if (rc != SQLITE_OK) {
        fprintf(stderr, "Could NOT perform the SQLite3 query: '%s'\n", query);
        exit(1);
    }
    rc = sqlite3_step(stmt);
    int result = -1;
    if (rc == SQLITE_ROW) {
        int type = sqlite3_column_type(stmt, 0);
        if (type != SQLITE_INTEGER) {
            fprintf(stderr, "ERROR: Column %s is NOT an int.\n", column);
            exit(1);
        }
        result = sqlite3_column_int(stmt, 0);
    } else {
        fprintf(stderr, "Could NOT read column=%s with id=%d for database.\n",
                column, self->id);
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
        fprintf(stderr, "Could NOT perform the SQLite3 query: '%s'\n", query);
        exit(1);
    }
    rc = sqlite3_step(stmt);
    double result = -1.0;
    if (rc == SQLITE_ROW) {
        int type = sqlite3_column_type(stmt, 0);
        if (type != SQLITE_FLOAT) {
            fprintf(stderr, "ERROR: Column %s is NOT a float.\n", column);
            exit(1);
        }
        result = sqlite3_column_double(stmt, 0);
    } else {
        fprintf(stderr, "Could NOT read column=%s with id=%d for database.\n",
                column, self->id);
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
        fprintf(stderr, "Could NOT perform the SQLite3 query: '%s'\n", query);
        exit(1);
    }
    rc = sqlite3_step(stmt);
    char* text;
    if (rc == SQLITE_ROW) {
        int type = sqlite3_column_type(stmt, 0);
        if (type != SQLITE_TEXT) {
            fprintf(stderr, "ERROR: Column %s is NOT a string.\n", column);
            exit(1);
        }
        text = (char*) sqlite3_column_text(stmt, 0);
    } else {
        fprintf(stderr, "Could NOT read column=%s with id=%d for database.\n",
                column, self->id);
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
                "ERROR: The value under column %s with id %d is NOT "
                "'True' or 'False', but %s.\n",
                column, self->id, bool_string);
        exit(1);
    }
}

SimDBIntVec sim_db_read_int_vec(SimDB* self, const char* column) {
    char* int_arr_string = sim_db_read_string(self, column);
    if (strstr(int_arr_string, "int[") != int_arr_string) {
        fprintf(stderr,
                "ERROR: The type under column=%s with id=%d is NOT "
                "int array.\n",
                column, self->id);
        exit(1);
    }
    SimDBIntVec int_vec;
    int_vec.size = 5;
    int_vec.array = (int*) malloc(int_vec.size * sizeof(int));
    char number[100];
    size_t n_digits = 0;
    size_t n_numbers = 0;
    for (int i = 4; i < strlen(int_arr_string); i++) {
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
                "ERROR: The type under column=%s with id=%d is NOT "
                "double array.\n",
                column, self->id);
        exit(1);
    }
    SimDBDoubleVec double_vec;
    double_vec.size = 5;
    double_vec.array = (double*) malloc(double_vec.size * sizeof(double));
    char number[100];
    size_t n_digits = 0;
    size_t n_numbers = 0;
    for (int i = 6; i < strlen(double_arr_string); i++) {
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
                "ERROR: The type under column=%s with id=%d is NOT "
                "string array.\n",
                column, self->id);
        exit(1);
    }
    SimDBStringVec string_vec;
    string_vec.size = 5;
    string_vec.array = (char**) malloc(string_vec.size * sizeof(char*));
    char string[100];
    int n_char = 0;
    int n_strings = 0;
    for (int i = 7; i < strlen(str_arr_string); i++) {
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
    for (int i = 0; i < n_strings; i++) {
        sim_db_add_pointer_to_free(self, string_vec.array[i]);
    }
    sim_db_add_pointer_to_free(self, string_vec.array);
    return string_vec;
}

SimDBBoolVec sim_db_read_bool_vec(SimDB* self, const char* column) {
    char* bool_arr_str = sim_db_read_string(self, column);
    if (strstr(bool_arr_str, "bool[") != bool_arr_str) {
        fprintf(stderr,
                "ERROR: The type under column=%s with id=%d is NOT "
                "double array.\n",
                column, self->id);
        exit(1);
    }
    SimDBBoolVec bool_vec;
    bool_vec.size = 5;
    bool_vec.array = (bool*) malloc(bool_vec.size * sizeof(bool));
    char bool_str[100];
    size_t n_char = 0;
    size_t n_bools = 0;
    for (int i = 5; i < strlen(bool_arr_str); i++) {
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
                        "ERROR: A value in the array  under column "
                        "%s with id %d is NOT 'True' or 'False', but %s.\n",
                        column, self->id, bool_str);
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
    char query[256];
    sprintf(query, "SELECT * FROM runs WHERE id = %d;", self->id);
    sqlite3_stmt* stmt = NULL;
    int rc = sqlite3_prepare_v2(self->db, query, -1, &stmt, NULL);
    if (rc != SQLITE_OK) {
        fprintf(stderr, "Could NOT perform the SQLite3 query: '%s'\n", query);
        exit(1);
    }
    rc = sqlite3_step(stmt);
    SimDBStringVec column_names;
    column_names.size = 5;
    column_names.array = (char**) malloc(column_names.size * sizeof(char*));
    if (rc == SQLITE_ROW) {
        int i = 0;
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
        fprintf(stderr, "Could NOT read from database\n");
        exit(1);
    }
    sqlite3_finalize(stmt);
    for (int i = 0; i < column_names.size; i++) {
        sim_db_add_pointer_to_free(self, column_names.array[i]);
    }
    sim_db_add_pointer_to_free(self, column_names.array);

    return column_names;
}

void sim_db_add_column_if_not_exists(SimDB* self, const char* column,
                                     const char* type) {
    SimDBStringVec column_names = sim_db_get_column_names(self);
    bool column_exists = false;
    for (int i = 0; i < column_names.size; i++) {
        if (strcmp(column_names.array[i], column) == 0) {
            column_exists = true;
            break;
        }
    }
    if (!column_exists) {
        char query[256];
        sprintf(query, "ALTER TABLE runs ADD COLUMN '%s' %s", column, type);
        int rc = sqlite3_exec(self->db, query, NULL, NULL, NULL);
        if (rc != SQLITE_OK) {
            fprintf(stderr, "Could NOT perform the SQLite3 query: '%s'\n",
                    query);
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
    sim_db_update(self, column, value);
}

void sim_db_write_bool(SimDB* self, const char* column, bool value) {
    sim_db_add_column_if_not_exists(self, column, "TEXT");
    char string_value[100];
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
    for (int i = 0; i < len; i++) {
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
    for (int i = 0; i < len; i++) {
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
    for (int i = 0; i < len; i++) {
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
    for (int i = 0; i < len; i++) {
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

char* sim_db_make_subdir_result(SimDB* self,
                                const char* name_result_directory) {
    char time_string[100];
    sim_db_get_time_string(time_string);
    char* name = sim_db_read_string(self, "name");
    char* name_subdir = (char*) malloc(4097 * sizeof(char));
    sprintf(name_subdir, "%s/%s_%s_%d", name_result_directory, time_string,
            name, self->id);
    if (mkdir(name_subdir, 0700) == -1) {
        fprintf(stderr, "ERROR: Could NOT create subdirectory %s\n",
                name_subdir);
        exit(1);
    }
    sim_db_add_pointer_to_free(self, name_subdir);

    return name_subdir;
}

void sim_db_update_sha1_executables(SimDB* self, char** paths_executables,
                                    size_t len) {
    const size_t len_sha1 = 100;
    char sha1[len_sha1 + 1];
    memset(sha1, 0, len_sha1 * sizeof(char));
    char tmp[len_sha1 + 1];
    for (int i = 0; i < len; i++) {
        char command[4200];
        sprintf(command, "git hash-object %s", paths_executables[i]);
        sim_db_run_shell_command(command, tmp, len_sha1);
        for (int j = 0; j < len_sha1; j++) {
            sha1[j] = sha1[j] ^ tmp[j];
        }
    }
    sim_db_update(self, "sha1_executables", sha1);
}

void sim_db_dtor(SimDB* self) {
    double used_time = difftime(time(NULL), self->start_time);
    char used_time_string[100];
    sprintf(used_time_string, "%dh %dm %fs", (int) used_time / 3600,
            (int) used_time / 60, fmod(used_time, 60));
    sim_db_update(self, "used_walltime", used_time_string);
    for (int i = 0; i < self->n_pointers; i++) {
        free(self->pointers_to_free[i]);
    }
    free(self->pointers_to_free);
    sqlite3_close(self->db);
}
