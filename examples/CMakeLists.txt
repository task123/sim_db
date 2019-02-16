# Must be run as a subdirectory from CMakeLists.txt in root directory. 

add_executable(minimal_c_example minimal_example.c)
target_link_libraries(minimal_c_example simdbc)
set_target_properties(minimal_c_example 
    PROPERTIES 
        RUNTIME_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/examples/build
)

add_executable(minimal_cpp_example minimal_example.cpp)
target_link_libraries(minimal_cpp_example simdbcpp)
set_target_properties(minimal_cpp_example 
    PROPERTIES 
        RUNTIME_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/examples/build
        CXX_STANDARD 11
)

if(${CMAKE_Fortran_COMPILER_LOADED})
    add_executable(minimal_fortran_example minimal_example.f90)
    target_link_libraries(minimal_fortran_example simdbf)
    set_target_properties(minimal_fortran_example
        PROPERTIES
            RUNTIME_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/examples/build
    )
endif()

add_executable(extensive_c_example extensive_example.c)
target_link_libraries(extensive_c_example simdbc)
set_target_properties(extensive_c_example 
    PROPERTIES 
        RUNTIME_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/examples/build
)

add_executable(extensive_cpp_example extensive_example.cpp)
target_link_libraries(extensive_cpp_example simdbcpp)
set_target_properties(extensive_cpp_example 
    PROPERTIES 
        RUNTIME_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/examples/build
        CXX_STANDARD 11
)

if(${CMAKE_Fortran_COMPILER_LOADED})
    add_executable(extensive_fortran_example extensive_example.f90)
    target_link_libraries(extensive_fortran_example simdbf)
    set_target_properties(extensive_fortran_example
        PROPERTIES
            RUNTIME_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/examples/build
    )
endif()
