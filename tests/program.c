/// Testing 'sim_db' for C, that is 'sim_db.h' and 'sim_db.c'.
///
/// Read in parameters from database, write parameters to database, make unique
/// subdirectory for results and save 'results.txt' in this directory.

#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include "../sim_db.h"

int main(int argc, char** argv) {
    SimDB* sim_db = sim_db_ctor(argc, argv);

    int param1 = sim_db_read_int(sim_db, "param1");
    printf("%d\n", param1);
    sim_db_write_int(sim_db, "new_param1", param1);
    printf("%d\n", sim_db_read_int(sim_db, "new_param1"));

    double param2 = sim_db_read_double(sim_db, "param2");
    printf("%f\n", param2);
    sim_db_write_double(sim_db, "new_param2", param2);
    printf("%f\n", sim_db_read_double(sim_db, "new_param2"));

    char* param3 = sim_db_read_string(sim_db, "param3");
    printf("%s\n", param3);
    sim_db_write_string(sim_db, "new_param3", param3);
    printf("%s\n", sim_db_read_string(sim_db, "new_param3"));

    bool param4 = sim_db_read_bool(sim_db, "param4");
    printf("%d\n", param4);
    sim_db_write_bool(sim_db, "new_param4", param4);
    printf("%d\n", sim_db_read_bool(sim_db, "new_param4"));

    SimDBIntVec int_vec = sim_db_read_int_vec(sim_db, "param5");
    for (int i = 0; i < int_vec.size; i++) {
        printf("%d\n", int_vec.array[i]);
    }
    sim_db_write_int_array(sim_db, "new_param5", int_vec.array, int_vec.size);
    int_vec = sim_db_read_int_vec(sim_db, "new_param5");
    for (int i = 0; i < int_vec.size; i++) {
        printf("%d\n", int_vec.array[i]);
    }

    SimDBDoubleVec double_vec = sim_db_read_double_vec(sim_db, "param6");
    for (int i = 0; i < double_vec.size; i++) {
        printf("%f\n", double_vec.array[i]);
    }
    sim_db_write_double_array(sim_db, "new_param6", double_vec.array,
                              double_vec.size);
    double_vec = sim_db_read_double_vec(sim_db, "new_param6");
    for (int i = 0; i < double_vec.size; i++) {
        printf("%f\n", double_vec.array[i]);
    }

    SimDBStringVec string_vec = sim_db_read_string_vec(sim_db, "param7");
    for (int i = 0; i < string_vec.size; i++) {
        printf("%s\n", string_vec.array[i]);
    }
    sim_db_write_string_array(sim_db, "new_param7", string_vec.array,
                              string_vec.size);
    string_vec = sim_db_read_string_vec(sim_db, "new_param7");
    for (int i = 0; i < string_vec.size; i++) {
        printf("%s\n", string_vec.array[i]);
    }

    SimDBBoolVec bool_vec = sim_db_read_bool_vec(sim_db, "param8");
    for (int i = 0; i < bool_vec.size; i++) {
        printf("%d\n", bool_vec.array[i]);
    }
    sim_db_write_bool_array(sim_db, "new_param8", bool_vec.array,
                            bool_vec.size);
    bool_vec = sim_db_read_bool_vec(sim_db, "new_param8");
    for (int i = 0; i < bool_vec.size; i++) {
        printf("%d\n", bool_vec.array[i]);
    }

    char path_test_dir[4097];
    getcwd(path_test_dir, 4096);
    strcat(path_test_dir, "/");
    strcat(path_test_dir, __FILE__);
    char* file_rel_sim_db = "/program.c";
    char* test_dir = strstr(path_test_dir, file_rel_sim_db);
    test_dir[0] = '\0';
    strcat(path_test_dir, "/results/");
    char* filename_result = strcat(
            sim_db_make_subdir_result(sim_db, path_test_dir), "/results.txt");
    FILE* result_file = fopen(filename_result, "w");
    for (int i = 0; i < double_vec.size; i++) {
        fprintf(result_file, "%f\n", double_vec.array[i]);
    }
    fclose(result_file);

    sim_db_dtor(sim_db);
}
