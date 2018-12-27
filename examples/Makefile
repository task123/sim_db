# This Makefile is deliberately verbose to more easily be able to see exactly 
# what needs to be compiled and which flags need to be passed. 
# Don't be intimidated by the length of this file, it is just verbose and don't
# do anything particularly complicated.

CC = cc
CXX = c++

CFLAGS = -O0 -Wall -Wextra
CXXFLAGS = -O0 -Wall -Wextra

export CC CXX CFLAGS CXXFLAGS

all:
	$(MAKE) minimal_c_example_updated
	$(MAKE) minimal_cpp_example_updated
	$(MAKE) extensive_c_example_updated
	$(MAKE) extensive_cpp_example_updated

minimal_c_example_updated: 
	$(MAKE) -C ../src clib # Compile sim_db's C library.
	$(MAKE) minimal_c_example

minimal_cpp_example_updated: 
	$(MAKE) -C ../src cpplib # Compile sim_db's C++ library.
	$(MAKE) minimal_cpp_example

extensive_c_example_updated: 
	$(MAKE) -C ../src clib # Compile sim_db's C library.
	$(MAKE) extensive_c_example

extensive_cpp_example_updated:
	$(MAKE) -C ../src cpplib # Compile sim_db's C++ library. 
	$(MAKE) extensive_cpp_example 

# Use target minimal_c_example_updated instead as it check libsimdbc.a's dependencies.
minimal_c_example: minimal_example.c ../build/libsimdbc.a
	$(CC) -o minimal_c_example minimal_example.c -I../include -L../build -lsimdbc

# Use target minimal_c_example_updated instead as it check libsimdbcpp.a's dependencies.
minimal_cpp_example: minimal_example.cpp ../build/libsimdbcpp.a
	$(CXX) -std=c++11 -o minimal_cpp_example minimal_example.cpp -I../include -L../build -lsimdbcpp

# Use target extensive_c_example_updated instead as it check libsimdbc.a's dependencies.
extensive_c_example: extensive_example.c ../build/libsimdbc.a
	$(CC) -o extensive_c_example extensive_example.c -I../include -L../build -lsimdbc

# Use target extensive_c_example_updated instead as it check libsimdbcpp.a's dependencies.
extensive_cpp_example: extensive_example.cpp ../build/libsimdbcpp.a
	$(CXX) -std=c++11 -o extensive_cpp_example extensive_example.cpp -I../include -L../build -lsimdbcpp

minimal_c_example_without_lib: minimal_example.cpp ../src/sim_db.c ../include/sim_db.h
	$(CC) -o minimal_c_example minimal_example.c ../src/sim_db.c ../third_party/sqlite3/sqlite3.c -I../include/

minimal_cpp_example_without_lib: minimal_example.cpp ../src/sim_db.cpp ../include/sim_db.hpp ../src/sim_db.c ../include/sim_db.h
	$(CC) -c -o sim_db.o ../src/sim_db.c  -I../include
	$(CC) -c -o sqlite3.o ../third_party/sqlite3/sqlite3.c
	$(CXX) -std=c++11 -o minimal_cpp_example minimal_example.cpp ../src/sim_db.cpp -I../include sim_db.o sqlite3.o 
	rm -f sim_db.o sqlite3.o

# $ make minimal_c_example_run ID='ID'
minimal_c_example_run: minimal_c_example_updated
	./minimal_c_example --id ${ID}

# $ make minimal_cpp_example_run ID='ID'
minimal_cpp_program_run: minimal_cpp_example_updated
	./minimal_cpp_example --id ${ID}

clean:
	rm -f minimal_c_example
	rm -f minimal_cpp_example
	rm -f extensive_c_example
	rm -f extensive_cpp_example
	rm -fr results/*
	rm -fr build
	$(MAKE) -C ../src clean

clean_except_third_party:
	rm -f minimal_c_example
	rm -f minimal_cpp_example
	rm -f extensive_c_example
	rm -f extensive_cpp_example
	rm -fr results/*
	rm -fr build
	$(MAKE) -C ../src clean_except_third_party

clean_etp:
	$(MAKE) clean_except_third_party
