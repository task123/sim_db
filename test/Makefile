CC = cc
CPP = c++
CFLAGS_DEBUG = -g -Wall -Wextra -Wfloat-equal
CFLAGS_RELEASE = -O3 -Wall -Wextra
CPPFLAGS_DEBUG = -std=c++11 -g -Wall -Wextra 
CPPFLAGS_RELEASE = -std=c++11 -O3 -Wall -Wextra
CFLAGS = $(CFLAGS_RELEASE)
CPPFLAGS = $(CPPFLAGS_RELEASE)
LDFLAGS = -L../lib -I../include

PATH_SIM_DB := $(if $(PATH_SIM_DB), $(PATH_SIM_DB), "..")

export CC CPP CFLAGS CPPFLAGS

.PHONY: all libsimdbc libsimdbcpp clean clean_except_third_party

all: c_program cpp_program
	$(MAKE) c_program
	$(MAKE) cpp_program

c_program: program.c libsimdbc
	$(MAKE) libsimdbc
	$(CC) $(CFLAGS) $(LDFLAGS) -o c_program program.c -lsimdbc

cpp_program: program.cpp libsimdbcpp
	$(MAKE) libsimdbcpp
	$(CPP) $(CPPFLAGS) $(LDFLAGS) -o cpp_program program.cpp -lsimdbcpp

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
