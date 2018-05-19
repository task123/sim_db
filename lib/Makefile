CPP = c++
BUILD_DIR = ../build
SOURCE_DIR = ../src
INCLUDE_DIR = ../include

CFLAGS_RELEASE = -O3 -DNDEBUG -Wall -Wextra
CPPFLAGS_RELEASE = -O3 -DNDEBUG -Wall -Wextra
CFLAGS := $(if $(CFLAGS), $(CFLAGS), $(CFLAGS_RELEASE))
CPPFLAGS := $(if $(CPPFLAGS), $(CPPFLAGS), $(CPPFLAGS_RELEASE))

.PHONY: all clean clean_except_third_party

all:
	$(MAKE) libsimdbc.a
	$(MAKE) libsimdbcpp.a

libsimdbc.a: $(BUILD_DIR)/sim_db.o $(BUILD_DIR)/third_party/sqlite3.o
	ar -rc $@ $^

libsimdbcpp.a: $(BUILD_DIR)/sim_db_cpp.o $(BUILD_DIR)/sim_db.o $(BUILD_DIR)/third_party/sqlite3.o
	ar -rc $@ $^

$(BUILD_DIR)/sim_db.o: $(SOURCE_DIR)/sim_db.c $(INCLUDE_DIR)/sim_db.h
	$(CC) $(CFLAGS) -c -o $@ $(SOURCE_DIR)/sim_db.c

$(BUILD_DIR)/sim_db_cpp.o: $(SOURCE_DIR)/sim_db.cpp $(INCLUDE_DIR)/sim_db.hpp
	$(CPP) $(CPPFLAGS) -c -o $@ $(SOURCE_DIR)/sim_db.cpp

$(BUILD_DIR)/third_party/sqlite3.o:
	$(MAKE) -C ../third_party/ $@

clean:
	rm -f libsimdbc.a
	rm -f libsimdbcpp.a
	rm -f $(BUILD_DIR)/sim_db.o
	rm -f $(BUILD_DIR)/sim_db_cpp.o
	$(MAKE) -C ../third_party/ clean

clean_except_third_party:
	rm -f libsimdbc.a
	rm -f libsimdbcpp.a
	rm -f $(BUILD_DIR)/sim_db.o
	rm -f $(BUILD_DIR)/sim_db_cpp.o
