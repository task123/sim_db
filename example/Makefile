# This Makefile is deliberately verbose to more easily be able to see exactly 
# what needs to be compiled and which flags need to be passed. 
# Don't be intimidated by the length of this file, it is just verbose and don't
# do anything particularly complicated.

CC = cc
CXX = c++

all:
	$(MAKE) minimal_c_example_updated
	$(MAKE) minimal_cpp_example_updated
	$(MAKE) extensive_c_example_updated
	$(MAKE) extensive_cpp_example_updated

minimal_c_example_updated: 
	$(MAKE) -C ../lib libsimdbc.a # Compile sim_db's C library.
	$(MAKE) minimal_c_example

minimal_cpp_example_updated: 
	$(MAKE) -C ../lib libsimdbcpp.a # Compile sim_db's C++ library.
	$(MAKE) minimal_cpp_example

extensive_c_example_updated: 
	$(MAKE) -C ../lib libsimdbc.a # Compile sim_db's C library.
	$(MAKE) extensive_c_example

extensive_cpp_example_updated:
	$(MAKE) -C ../lib libsimdbcpp.a # Compile sim_db's C++ library. 
	$(MAKE) extensive_cpp_example 

# Use target minimal_c_example_updated instead as it check libsimdbc.a's dependencies.
minimal_c_example: minimal_example.c ../lib/libsimdbc.a
	$(CC) -o minimal_c_example minimal_example.c -I../Include -L../lib -lsimdbc -lm -lpthread -ldl

# Use target minimal_c_example_updated instead as it check libsimdbcpp.a's dependencies.
minimal_cpp_example: minimal_example.cpp ../lib/libsimdbcpp.a
	$(CXX) -std=c++11 -o minimal_cpp_example minimal_example.cpp -I../Include -L../lib -lsimdbcpp -lm -lpthread -ldl

# Use target extensive_c_example_updated instead as it check libsimdbc.a's dependencies.
extensive_c_example: extensive_example.c ../lib/libsimdbc.a
	$(CC) -o extensive_c_example extensive_example.c -I../Include -L../lib -lsimdbc -lm -lpthread -ldl

# Use target extensive_c_example_updated instead as it check libsimdbcpp.a's dependencies.
extensive_cpp_example: extensive_example.cpp ../lib/libsimdbcpp.a
	$(CXX) -std=c++11 -o extensive_cpp_example extensive_example.cpp -I../Include -L../lib -lsimdbcpp -lm -lpthread -ldl

minimal_c_example_without_lib: minimal_example.cpp ../src/sim_db.c ../include/sim_db.h
	$(CC) -o minimal_c_example minimal_example.c ../src/sim_db.c ../third_party/sqlite3/sqlite3.c -I../include/ -lm -lpthread -ldl

minimal_cpp_example_without_lib: minimal_example.cpp ../src/sim_db.cpp ../include/sim_db.hpp ../src/sim_db.c ../include/sim_db.h
	$(CC) -c -o sim_db.o ../src/sim_db.c 
	$(CC) -c -o sqlite3.o ../third_party/sqlite3/sqlite3.c
	$(CXX) -std=c++11 -o minimal_cpp_example minimal_example.cpp ../src/sim_db.cpp -I../include sim_db.o sqlite3.o -lm -lpthread -ldl
	rm -f sim_db.o sqlite3.o

# $ make minimal_c_example_run ID='ID'
minimal_c_example_run: minimal_c_example_updated
	./minimal_c_example --id ${ID} --path_sim_db ".."

# $ make minimal_cpp_example_run ID='ID'
minimal_cpp_program_run: minimal_cpp_example_updated
	./minimal_cpp_example --id ${ID} --path_sim_db ".."

clean:
	rm -f minimal_c_example
	rm -f minimal_cpp_example
	rm -f extensive_c_example
	rm -f extensive_cpp_example
	rm -fr results/*
	$(MAKE) -C ../lib clean

clean_except_third_party:
	rm -f minimal_c_example
	rm -f minimal_cpp_example
	rm -f extensive_c_example
	rm -f extensive_cpp_example
	rm -fr results/*
	$(MAKE) -C ../lib clean_except_third_party

clean_etp:
	$(MAKE) clean_except_third_party
