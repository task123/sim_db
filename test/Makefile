CC = cc
CXX = c++
CFLAGS_DEBUG = -std=c99 -g -Wall -Wextra -Wfloat-equal
CFLAGS_RELEASE = -std=c99 -O3 -DNDEBUG
CXXFLAGS_DEBUG = -g -Wall -Wextra 
CXXFLAGS_RELEASE = -O3 -DNDEBUG
CFLAGS = $(CFLAGS_RELEASE)
CXXFLAGS = $(CXXFLAGS_RELEASE)
LDFLAGS = -L../lib -I../include -lm -lpthread -ldl

PATH_SIM_DB := $(if $(PATH_SIM_DB), $(PATH_SIM_DB), "..")

export CC CXX CFLAGS CXXFLAGS

.PHONY: all c_program_updated cpp_program_updated clean clean_except_third_party clean_etp

all:
	$(MAKE) c_program_updated
	$(MAKE) cpp_program_updated

c_program_updated:
	$(MAKE) -C ../lib libsimdbc.a
	$(MAKE) c_program
	
cpp_program_updated:
	$(MAKE) -C ../lib libsimdbcpp.a
	$(MAKE) cpp_program

# Use target c_program_updated instead as it check libsimdbc.a's dependencies.
c_program: program.c ../lib/libsimdbc.a
	$(CC) $(CFLAGS) $(LDFLAGS) -o c_program program.c -lsimdbc

# Use target cpp_program_updated instead as it check libsimdbcpp.a's dependencies.
cpp_program: program.cpp ../lib/libsimdbcpp.a
	$(CXX) $(CXXFLAGS) $(LDFLAGS) -o cpp_program program.cpp -lsimdbcpp

c_program_run: c_program_updated
	./c_program --id ${ID} --path_sim_db ${PATH_SIM_DB}

cpp_program_run: cpp_program_updated
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
