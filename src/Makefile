CFLAGS_RELEASE=-O3 -DNDEBUG
CXXFLAGS_RELEASE=-O3 -DNDEBUG
CFLAGS := $(if $(CFLAGS), $(CFLAGS), $(CFLAGS_RELEASE))
CXXFLAGS := $(if $(CXXFLAGS), $(CXXFLAGS), $(CXXFLAGS_RELEASE))

CC := $(if $(CC), $(CC), cc)
CXX := $(if $(CXX), $(CXX), c++)

export CC CXX CFLAGS CXXFLAGS

LIB_OUTPUR_DIR=../build
INCLUDE_DIR=../include
SQLITE3_DIR=../third_party/sqlite3

.PHONY: all libs clib cpplib clean clean_except_third_party clean_etp

all:
	$(MAKE) libs

libs:
	$(MAKE) clib
	$(MAKE) cpplib

clib: 
	$(MAKE) $(LIB_OUTPUR_DIR)/libsimdbc.a

cpplib:  
	$(MAKE) $(LIB_OUTPUR_DIR)/libsimdbcpp.a

$(LIB_OUTPUR_DIR)/libsimdbc.a: $(LIB_OUTPUR_DIR) sim_db.c.o $(SQLITE3_DIR)/sqlite3.o
	ar -r $@ sim_db.c.o $(SQLITE3_DIR)/sqlite3.o

$(LIB_OUTPUR_DIR)/libsimdbcpp.a: $(LIB_OUTPUR_DIR) sim_db.cpp.o sim_db.c.o $(SQLITE3_DIR)/sqlite3.o
	ar -r $@ sim_db.cpp.o sim_db.c.o $(SQLITE3_DIR)/sqlite3.o

sim_db.c.o: sim_db.c $(INCLUDE_DIR)/sim_db.h
	$(CC) $(CFLAGS) -c -o $@ sim_db.c -I$(INCLUDE_DIR) -I$(SQLITE3_DIR)

sim_db.cpp.o: sim_db.cpp $(INCLUDE_DIR)/sim_db.hpp $(INCLUDE_DIR)/sim_db.h
	$(CXX) $(CXXFLAGS) -c -o $@ sim_db.cpp -I$(INCLUDE_DIR) -I$(SQLITE3_DIR)

$(SQLITE3_DIR)/sqlite3.o:
	$(MAKE) -C $(SQLITE3_DIR)/ sqlite3.o

$(LIB_OUTPUR_DIR):
	mkdir -p $@

clean:
	$(MAKE) clean_except_third_party
	$(MAKE) -C $(SQLITE3_DIR) clean

clean_except_third_party:
	rm -f $(LIB_OUTPUR_DIR)/libsimdbc.a
	rm -f $(LIB_OUTPUR_DIR)/libsimdbcpp.a
	rm -f sim_db.c.o
	rm -f sim_db.cpp.o

clean_etp:
	$(MAKE) clean_except_third_party
