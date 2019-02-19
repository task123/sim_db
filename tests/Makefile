CC = cc
CXX = c++
FC = gfortran
CFLAGS_DEBUG = -std=c99 -Wall -fno-omit-frame-pointer -fsanitize=address -fsanitize=undefined
CXXFLAGS_DEBUG = -Wall -fno-omit-frame-pointer -fsanitize=address -fsanitize=undefined
CFLAGS_RELEASE = -std=c99 -O3 -DNDEBUG
CXXFLAGS_RELEASE = -O3 -DNDEBUG 
FFLAGS_DEBUG = -std=f2008 -Wall -fsanitize=address -fsanitize=undefined
FFLAGS_RELEASE = -std=f2008 -O3
CFLAGS = $(CFLAGS_RELEASE)
CXXFLAGS = $(CXXFLAGS_RELEASE)
FFLAGS =  $(FFLAGS_RELEASE)
LDFLAGS = -lm -lpthread -ldl

PATH_SIM_DB := $(if $(PATH_SIM_DB), $(PATH_SIM_DB), "..")

export CC CXX FC CFLAGS CXXFLAGS FFLAGS

.PHONY: all c_program_updated cpp_program_updated fortran_program_updated c_mtap_updated clean clean_except_third_party clean_etp

LIB_OUTPUT_DIR=../build

all:
	$(MAKE) c_program_updated
	$(MAKE) cpp_program_updated
	$(MAKE) fortran_program_updated
	$(MAKE) c_mtap_updated

c_program_updated:
	$(MAKE) -C ../src clib
	$(MAKE) c_program
	
cpp_program_updated:
	$(MAKE) -C ../src cpplib
	$(MAKE) cpp_program
	
fortran_program_updated:
	$(MAKE) -C ../src flib
	$(MAKE) fortran_program

c_mtap_updated:
	$(MAKE) c_program_updated
	$(MAKE) c_mtap

# Use target c_program_updated instead as it check libsimdbc.a's dependencies.
c_program: program.c $(LIB_OUTPUT_DIR)/libsimdbc.a
	$(CC) $(CFLAGS) -o c_program -I../include program.c -L$(LIB_OUTPUT_DIR) -lsimdbc $(LDFLAGS)

# Use target cpp_program_updated instead as it check libsimdbcpp.a's dependencies.
cpp_program: program.cpp $(LIB_OUTPUT_DIR)/libsimdbcpp.a
	$(CXX) $(CXXFLAGS) -o cpp_program -I../include program.cpp -L$(LIB_OUTPUT_DIR) -lsimdbcpp $(LDFLAGS)

# Use target cpp_program_updated instead as it check libsimdbcpp.a's dependencies.
fortran_program: program.f90 $(LIB_OUTPUT_DIR)/libsimdbf.a
	$(FC) $(FFLAGS) -o fortran_program -I$(LIB_OUTPUT_DIR) program.f90 -L$(LIB_OUTPUT_DIR) -lsimdbf $(LDFLAGS)

# Use target c_mtap_updated instead as it check libsimdbc.a's dependencies.
c_mtap: multithreading_and_processing.c $(LIB_OUTPUT_DIR)/libsimdbc.a
	$(CC) $(CFLAGS) -o c_mtap multithreading_and_processing.c -I../include -L$(LIB_OUTPUT_DIR) -lsimdbc $(LDFLAGS) 

c_program_run: c_program_updated
	./c_program --id ${ID} --path_proj_root ${PATH_SIM_DB}

cpp_program_run: cpp_program_updated
	./cpp_program --id ${ID} --path_proj_root ${PATH_SIM_DB}

c_mtap_run: c_mtap_updated
	./c_mtap

clean:
	$(MAKE) clean_except_third_party
	$(MAKE) -C ../src clean

clean_except_third_party:
	rm -f c_program
	rm -f cpp_program
	rm -f fortran_program
	rm -f c_mtap
	rm -fr c_program.dSYM
	rm -fr cpp_program.dSYM
	rm -fr fortran_program.dSYM
	rm -fr c_mtap.dSYM
	rm -fr results/*
	rm -fr build/
	$(MAKE) -C ../src clean_except_third_party

clean_etp:
	$(MAKE) clean_except_third_party
