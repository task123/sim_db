BUILD_DIR = ../build
SOURCE_DIR = ../src
INCLUDE_DIR = ../include

CFLAGS_RELEASE = -std=c99 -O3 -DNDEBUG
CXXFLAGS_RELEASE = -O3 -DNDEBUG
CFLAGS := $(if $(CFLAGS), $(CFLAGS), $(CFLAGS_RELEASE))
CXXFLAGS := $(if $(CXXFLAGS), $(CXXFLAGS), $(CXXFLAGS_RELEASE))

CC := $(if $(CC), $(CC), cc)
CXX := $(if $(CXX), $(CXX), c++)

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
	$(CXX) $(CXXFLAGS) -c -o $@ $(SOURCE_DIR)/sim_db.cpp

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
