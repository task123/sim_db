CC = cc
CXX = c++

all:
	$(MAKE) c_example_updated
	$(MAKE) extensive_cpp_example_updated

c_example_updated: 
	$(MAKE) -C ../lib libsimdbc.a # Compile sim_db's C library.
	$(MAKE) c_example

extensive_cpp_example_updated:
	$(MAKE) -C ../lib libsimdbcpp.a # Compile sim_db's C++ library. 
	$(MAKE) extensive_cpp_example 

# Use target c_example_updated instead as it check libsimdbc.a's dependencies.
c_example: example_program.c ../lib/libsimdbc.a
	$(CC) -o c_example example_program.c -I../Include -L../lib -lsimdbc -lm -lpthread -ldl

# Use target cpp_example_updated instead as it check libsimdbcpp.a's dependencies.
extensive_cpp_example: extensive_example.cpp ../lib/libsimdbcpp.a
	$(CXX) -std=c++11 -o extensive_cpp_example extensive_example.cpp -I../Include -L../lib -lsimdbcpp -lm -lpthread -ldl

c_example_without_lib: example_program.cpp ../src/sim_db.c ../include/sim_db.h
	$(CC) -o c_example example_program.c ../src/sim_db.c ../third_party/sqlite3/sqlite3.c -I../include/ -lm -lpthread -ldl

cpp_example_without_lib: example_program.cpp ../src/sim_db.cpp ../include/sim_db.hpp ../src/sim_db.c ../include/sim_db.h
	$(CC) -c -o sim_db.o ../src/sim_db.c 
	$(CC) -c -o sqlite3.o ../third_party/sqlite3/sqlite3.c
	$(CXX) -std=c++11 -o cpp_example example_program.cpp ../src/sim_db.cpp -I../include sim_db.o sqlite3.o -lm -lpthread -ldl
	rm -f sim_db.o sqlite3.o

c_example_run: c_example_updated
	./c_example --id ${ID} --path_sim_db ".."

cpp_program_run: cpp_example_updated
	./cpp_example --id ${ID} --path_sim_db ".."

clean:
	rm -f c_example
	rm -f cpp_example
	rm -fr results/*
	$(MAKE) -C ../lib clean

clean_except_third_party:
	rm -f c_example
	rm -f cpp_example
	rm -fr results/*
	$(MAKE) -C ../lib clean_except_third_party

clean_etp:
	$(MAKE) clean_except_third_party
