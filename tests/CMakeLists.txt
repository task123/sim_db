# Must be run as a subdirectory from CMakeLists.txt in root directory. 

include_directories(${PROJECT_SOURCE_DIR}/include)
link_directories(${CMAKE_BINDARY_DIR})

add_executable(c_program program.c)
target_link_libraries(c_program simdbc)
set_target_properties(c_program 
    PROPERTIES 
        RUNTIME_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/tests/build
)

add_executable(cpp_program program.cpp)
target_link_libraries(cpp_program simdbcpp)
set_target_properties(cpp_program 
    PROPERTIES 
        RUNTIME_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/tests/build
)

if(${CMAKE_Fortran_COMPILER_LOADED})
    add_executable(fortran_program program.f90)
    target_link_libraries(fortran_program simdbf)
    set_target_properties(fortran_program
        PROPERTIES
            RUNTIME_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/tests/build
    )
endif()

find_package(Threads REQUIRED)

add_executable(c_mtap multithreading_and_processing.c)
target_link_libraries(c_mtap simdbc Threads::Threads)
set_target_properties(c_mtap 
    PROPERTIES 
        RUNTIME_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/tests/build
)
