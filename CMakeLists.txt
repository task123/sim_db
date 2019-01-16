cmake_minimum_required(VERSION 3.1.0)

project(sim_db VERSION 0.2.4)

add_subdirectory(src)
add_subdirectory(examples EXCLUDE_FROM_ALL)
add_subdirectory(tests EXCLUDE_FROM_ALL)

include(CMakePackageConfigHelpers)
write_basic_package_version_file("${CMAKE_BINARY_DIR}/sim_dbConfigVersion.cmake"
    VERSION ${sim_db_VERSION}
    COMPATIBILITY AnyNewerVersion
)

install(FILES "${PROJECT_SOURCE_DIR}/cmake/sim_dbConfig.cmake" "${CMAKE_BINARY_DIR}/sim_dbConfigVersion.cmake"
    DESTINATION lib/cmake/sim_db
)
