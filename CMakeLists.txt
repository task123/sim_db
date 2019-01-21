cmake_minimum_required(VERSION 3.1.0)

project(sim_db VERSION 0.2.5)

# Add sanitizer for debug mode if the compiler is GCC or Clang.
set(WHICH_SANITIZER "address") # address, thread or memory
set(SANITIZER_FLAGS "-fno-omit-frame-pointer -fsanitize=${WHICH_SANITIZER} -fsanitize=undefined")
if(("${CMAKE_CXX_COMPILER_ID}" STREQUAL "GNU" 
     AND ${CMAKE_CXX_COMPILER_VERSION} GREATER_EQUAL "5.1")
   OR ("${CMAKE_CXX_COMPILER_ID}" STREQUAL "Clang" 
     AND ${CMAKE_CXX_COMPILER_VERSION} GREATER_EQUAL "3.1"))
    set (CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} ${SANITIZER_FLAGS}")
    set (CMAKE_LINKER_FLAGS_DEBUG "${CMAKE_LINKER_FLAGS_DEBUG} ${SANITIZER_FLAGS}")
endif()
if(("${CMAKE_C_COMPILER_ID}" STREQUAL "GNU" 
     AND ${CMAKE_C_COMPILER_VERSION} GREATER_EQUAL "5.1")
   OR ("${CMAKE_C_COMPILER_ID}" STREQUAL "Clang" 
     AND ${CMAKE_C_COMPILER_VERSION} GREATER_EQUAL "3.1"))
    set (CMAKE_C_FLAGS_DEBUG "${CMAKE_C_FLAGS_DEBUG} ${SANITIZER_FLAGS}")
    set (CMAKE_LINKER_FLAGS_DEBUG "${CMAKE_LINKER_FLAGS_DEBUG} ${SANITIZER_FLAGS}")
endif()

add_subdirectory(src)
add_subdirectory(examples EXCLUDE_FROM_ALL)
add_subdirectory(tests EXCLUDE_FROM_ALL)

include(CMakePackageConfigHelpers)
write_basic_package_version_file("${CMAKE_BINARY_DIR}/sim_dbConfigVersion.cmake"
    VERSION ${sim_db_VERSION}
    COMPATIBILITY AnyNewerVersion
)

install(
    FILES 
        "${PROJECT_SOURCE_DIR}/cmake/sim_dbConfig.cmake" 
        "${CMAKE_BINARY_DIR}/sim_dbConfigVersion.cmake"
    DESTINATION 
        lib/cmake/sim_db
)
