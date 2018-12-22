# Creates the sim_db libraries simdbc and simdbcpp for C and C++ respectfully.

cmake_minimum_required(VERSION 3.0.0)

project(sim_db VERSION 0.1.3)

if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release)
endif()

set(CMAKE_C_FLAGS_RELEASE "-O3 -DNDEBUG")
set(CMAKE_CXX_FLAGS_RELEASE "-O3 -DNDEBUG")

add_subdirectory(src)

include(CMakePackageConfigHelpers)
write_basic_package_version_file("${CMAKE_BINARY_DIR}/sim_dbConfigVersion.cmake"
    VERSION ${sim_db_VERSION}
    COMPATIBILITY AnyNewerVersion
)

install(FILES "${PROJECT_SOURCE_DIR}/cmake/sim_dbConfig.cmake" "${CMAKE_BINARY_DIR}/sim_dbConfigVersion.cmake"
    DESTINATION lib/cmake/sim_db
)
