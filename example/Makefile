CC = cc
CXX = c++

c_example: example_program.c libsimdbc
	$(MAKE) libsimdbc # Compile sim_db's C library.
	$(CC) -o c_example example_program.c -I../Include -L../lib -lsimdbc -lm -lpthread

cpp_example: example_program.cpp libsimdbcpp
	$(MAKE) libsimdbcpp # Compile sim_db's C++ library. 
	$(CXX) -std=c++11 -o cpp_example example_program.cpp -I../Include -L../lib -lsimdbcpp -lm -lpthread

libsimdbc: 
	$(MAKE) -C ../lib libsimdbc.a

libsimdbcpp: 
	$(MAKE) -C ../lib libsimdbcpp.a

c_example_without_lib: example_program.cpp ../src/sim_db.c ../include/sim_db.h
	$(CC) -o c_example example_program.c ../src/sim_db.c ../third_party/sqlite3.c -I../include/ -lm -lpthread

cpp_example_without_lib: example_program.cpp ../src/sim_db.cpp ../include/sim_db.hpp ../src/sim_db.c ../include/sim_db.h
	$(CC) -c -o sim_db.o ../src/sim_db.c 
	$(CC) -c -o sqlite3.o ../third_party/sqlite3.c
	$(CXX) -std=c++11 -o cpp_example example_program.cpp ../src/sim_db.cpp -I../include sim_db.o sqlite3.o -lm -lpthread
	rm -f sim_db.o sqlite3.o

c_example_run: c_example
	./c_example --id ${ID} --path_sim_db ".."

cpp_program_run: cpp_example
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

clean_example:
	rm -f c_example
	rm -f cpp_example
