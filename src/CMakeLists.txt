set(INCLUDE_DIR ${PROJECT_SOURCE_DIR}/include)
set(SQLITE_DIR ${PROJECT_SOURCE_DIR}/third_party/sqlite3)


add_library(simdbc 
            sim_db.c 
            ${SQLITE_DIR}/sqlite3.c
)
target_include_directories(simdbc 
    PUBLIC 
        $<BUILD_INTERFACE:${INCLUDE_DIR}>
        $<INSTALL_INTERFACE:include>
)
set(simdbc_REQUIRED_HEADERS ${INCLUDE_DIR}/sim_db.h)


add_library(simdbcpp 
            sim_db.cpp 
            sim_db.c 
            ${SQLITE_DIR}/sqlite3.c
)
target_include_directories(simdbcpp 
    PUBLIC 
        $<BUILD_INTERFACE:${INCLUDE_DIR}>
        $<INSTALL_INTERFACE:include>
)
set(simdbcpp_REQUIRED_HEADERS ${INCLUDE_DIR}/sim_db.hpp ${INCLUDE_DIR}/sim_db.hpp)


install(TARGETS simdbc simdbcpp
    EXPORT sim_dbTargets
    LIBRARY DESTINATION lib/sim_db
    ARCHIVE DESTINATION lib/sim_db
    RUNTIME DESTINATION bin/sim_db
)

install(FILES ${simdbc_REQUIRED_HEADERS} ${simdbcpp_REQUIRED_HEADERS}
  DESTINATION include
)

install(EXPORT sim_dbTargets
    NAMESPACE sim_db::
    DESTINATION lib/cmake/sim_db
)
