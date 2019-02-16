set(INCLUDE_DIR ${PROJECT_SOURCE_DIR}/include)
set(SQLITE_DIR ${PROJECT_SOURCE_DIR}/third_party/sqlite3)

find_package(Threads REQUIRED)

add_library(simdbc 
            sim_db.c 
            ${SQLITE_DIR}/sqlite3.c
)
target_link_libraries(simdbc Threads::Threads ${CMAKE_DL_LIBS} m)
target_include_directories(simdbc 
    PUBLIC 
        $<BUILD_INTERFACE:${INCLUDE_DIR}>
        $<INSTALL_INTERFACE:include>
    PRIVATE
        $<BUILD_INTERFACE:${SQLITE_DIR}>
)
set_target_properties(simdbc 
    PROPERTIES 
        ARCHIVE_OUTPUT_DIRECTORY ${PROJECT_BINARY_DIR}
        LIBRARY_OUTPUT_DIRECTORY ${PROJECT_BINARY_DIR}
        C_STANDARD 99
)
set(simdbc_REQUIRED_HEADERS ${INCLUDE_DIR}/sim_db.h)


add_library(simdbcpp 
            sim_db.cpp 
            sim_db.c 
            ${SQLITE_DIR}/sqlite3.c
)
target_link_libraries(simdbcpp Threads::Threads ${CMAKE_DL_LIBS} m)
target_include_directories(simdbcpp 
    PUBLIC 
        $<BUILD_INTERFACE:${INCLUDE_DIR}>
        $<INSTALL_INTERFACE:include>
    PRIVATE
        $<BUILD_INTERFACE:${SQLITE_DIR}>
)
set_target_properties(simdbcpp 
    PROPERTIES 
        ARCHIVE_OUTPUT_DIRECTORY ${PROJECT_BINARY_DIR}
        LIBRARY_OUTPUT_DIRECTORY ${PROJECT_BINARY_DIR}
)
set(simdbcpp_REQUIRED_HEADERS ${INCLUDE_DIR}/sim_db.hpp ${INCLUDE_DIR}/sim_db.h)


install(TARGETS simdbc simdbcpp
    EXPORT sim_dbTargets
    LIBRARY DESTINATION lib/sim_db
    ARCHIVE DESTINATION lib/sim_db
    RUNTIME DESTINATION bin/sim_db
)

install(FILES ${simdbc_REQUIRED_HEADERS} ${simdbcpp_REQUIRED_HEADERS}
  DESTINATION include
)


if(${CMAKE_Fortran_COMPILER_LOADED})
    message("fortran loaded")
    add_library(simdbf
                class_sim_db.f90
                sim_db_c_interface.f90
                sim_db.c
                ${SQLITE_DIR}/sqlite3.c
    )
    target_link_libraries(simdbf simdbc Threads::Threads ${CMAKE_DL_LIBS} m)            
    set_target_properties(simdbf
        PROPERTIES 
            ARCHIVE_OUTPUT_DIRECTORY ${PROJECT_BINARY_DIR}
            LIBRARY_OUTPUT_DIRECTORY ${PROJECT_BINARY_DIR}
            Fortran_MODULE_DIRECTORY ${PROJECT_BINARY_DIR}
    )
    target_include_directories(simdbf
        PUBLIC
            $<BUILD_INTERFACE:${PROJECT_BINARY_DIR}>
            $<INSTALL_INTERFACE:include>
    )
    set(simdbf_REQUIRED_MODULES 
        ${PROJECT_BINARY_DIR}/sim_db_c_interface.mod 
        ${PROJECT_BINARY_DIR}/class_sim_db.mod
    )


    install(TARGETS simdbf
        EXPORT sim_dbTargets
        LIBRARY DESTINATION lib/sim_db
        ARCHIVE DESTINATION lib/sim_db
        RUNTIME DESTINATION bin/sim_db
    )

    install(FILES ${simdbf_REQUIRED_MODULES}
      DESTINATION include
    )
endif()


install(EXPORT sim_dbTargets
    NAMESPACE sim_db::
    DESTINATION lib/cmake/sim_db
)
