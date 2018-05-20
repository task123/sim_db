CC = cc
CXX = c++
CFLAGS_DEBUG = -std=c99 -g -Wall -Wextra -Wfloat-equal
CFLAGS_RELEASE = -std=c99 -O3 -DNDEBUG
CXXFLAGS_DEBUG = -g -Wall -Wextra 
CXXFLAGS_RELEASE = -O3 -DNDEBUG
CFLAGS = $(CFLAGS_RELEASE)
CXXFLAGS = $(CXXFLAGS_RELEASE)
LDFLAGS = -L../lib -I../include -lm -lpthread

PATH_SIM_DB := $(if $(PATH_SIM_DB), $(PATH_SIM_DB), "..")

export CC CXX CFLAGS CXXFLAGS

.PHONY: all libsimdbc libsimdbcpp clean clean_except_third_party

all: c_program cpp_program
	$(MAKE) c_program
	$(MAKE) cpp_program

c_program: program.c libsimdbc
	$(MAKE) libsimdbc
	$(CC) $(CFLAGS) $(LDFLAGS) -o c_program program.c -lsimdbc

cpp_program: program.cpp libsimdbcpp
	$(MAKE) libsimdbcpp
	$(CXX) $(CXXFLAGS) $(LDFLAGS) -o cpp_program program.cpp -lsimdbcpp

libsimdbc: 
	$(MAKE) -C ../lib libsimdbc.a

libsimdbcpp: 
	$(MAKE) -C ../lib libsimdbcpp.a

c_program_run: c_program
	./c_program --id ${ID} --path_sim_db ${PATH_SIM_DB}

cpp_program_run: cpp_program
	./cpp_program --id ${ID} --path_sim_db ${PATH_SIM_DB}

clean:
	rm -f c_program
	rm -f cpp_program
	rm -fr c_program.dSYM
	rm -fr cpp_program.dSYM
	$(MAKE) -C ../lib clean

clean_except_third_party:
	rm -f c_program
	rm -f cpp_program
	rm -fr c_program.dSYM
	rm -fr cpp_program.dSYM
	$(MAKE) -C ../lib clean_except_third_party

clean_etp:
	$(MAKE) clean_except_third_party
