cmake_minimum_required(VERSION 3.0.0)

project(sim_db)

add_library(simdbc 
            src_c_and_cpp/sim_db.c 
            third_party/sqlite3/sqlite3.c)
target_include_directories(simdbc PUBLIC include)

add_library(simdbcpp 
            src_c_and_cpp/sim_db.cpp 
            src_c_and_cpp/sim_db.c 
            third_party/sqlite3/sqlite3.c)
target_include_directories(simdbcpp PUBLIC include)

install(TARGETS simdbc simdbcpp
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib
    INCLUDES DESTINATION include)
