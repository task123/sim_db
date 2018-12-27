CC = cc
CXX = c++
CFLAGS_DEBUG = -std=c99 -Wall -Wextra
CXXFLAGS_DEBUG = -Wall -Wextra 
CFLAGS_RELEASE = -std=c99 -O3 -DNDEBUG
CXXFLAGS_RELEASE = -O3 -DNDEBUG
CFLAGS = $(CFLAGS_DEBUG)
CXXFLAGS = $(CXXFLAGS_DEBUG)
LDFLAGS = -lm -lpthread -ldl

PATH_SIM_DB := $(if $(PATH_SIM_DB), $(PATH_SIM_DB), "..")

export CC CXX CFLAGS CXXFLAGS

.PHONY: all c_program_updated cpp_program_updated clean clean_except_third_party clean_etp

LIB_OUTPUT_DIR=../build

all:
	$(MAKE) c_program_updated
	$(MAKE) cpp_program_updated
	$(MAKE) c_mtap_updated

c_program_updated:
	$(MAKE) -C ../src clib
	$(MAKE) c_program
	
cpp_program_updated:
	$(MAKE) -C ../src cpplib
	$(MAKE) cpp_program

c_mtap_updated:
	$(MAKE) c_program_updated
	$(MAKE) c_mtap

# Use target c_program_updated instead as it check libsimdbc.a's dependencies.
c_program: program.c $(LIB_OUTPUT_DIR)/libsimdbc.a
	$(CC) $(CFLAGS) -o c_program -I../include program.c -L$(LIB_OUTPUT_DIR) -lsimdbc  

# Use target cpp_program_updated instead as it check libsimdbcpp.a's dependencies.
cpp_program: program.cpp $(LIB_OUTPUT_DIR)/libsimdbcpp.a
	$(CXX) $(CXXFLAGS) -o cpp_program -I../include program.cpp -L$(LIB_OUTPUT_DIR) -lsimdbcpp 

# Use target c_mtap_updated instead as it check libsimdbc.a's dependencies.
c_mtap: multithreading_and_processing.c $(LIB_OUTPUT_DIR)/libsimdbc.a
	$(CC) $(CFLAGS) -o c_mtap multithreading_and_processing.c -I../include -L$(LIB_OUTPUT_DIR) -lsimdbc 

c_program_run: c_program_updated
	./c_program --id ${ID} --path_proj_root ${PATH_SIM_DB}

cpp_program_run: cpp_program_updated
	./cpp_program --id ${ID} --path_proj_root ${PATH_SIM_DB}

c_mtap_run: c_mtap_updated
	./c_mtap

clean:
	rm -f c_program
	rm -f cpp_program
	rm -f c_mtap
	rm -fr c_program.dSYM
	rm -fr cpp_program.dSYM
	rm -fr c_mtap.dSYM
	rm -fr results/*
	rm -fr build/
	$(MAKE) -C ../src clean

clean_except_third_party:
	rm -f c_program
	rm -f cpp_program
	rm -f c_mtap
	rm -fr c_program.dSYM
	rm -fr cpp_program.dSYM
	rm -fr c_mtap.dSYM
	rm -fr results/*
	rm -fr build/
	$(MAKE) -C ../src clean_except_third_party

clean_etp:
	$(MAKE) clean_except_third_party
