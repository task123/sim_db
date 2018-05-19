CC = cc
CPP = c++

c_example: example_program.c libsimdbc
	$(MAKE) libsimdbc # Compile sim_db's C library.
	$(CC) -o c_example example_program.c -I../include -L../lib -lsimdbc

cpp_example: example_program.cpp libsimdbcpp
	$(MAKE) libsimdbcpp # Compile sim_db's C++ library. 
	$(CPP) -std=c++11 -o cpp_example example_program.cpp -I../include -L../lib -lsimdbcpp

libsimdbc: 
	$(MAKE) -C ../lib libsimdbc.a

libsimdbcpp: 
	$(MAKE) -C ../lib libsimdbcpp.a

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

clean_example:
	rm -f c_example
	rm -f cpp_example
