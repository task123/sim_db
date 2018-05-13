CC = gcc
CPP = g++
CFLAGS = -lsqlite3
CPPFLAGS = -lsqlite3 -std=c++11

build_c_program: program.c ../sim_db.c ../sim_db.h
	${CC} ${CFLAGS} -o c_program program.c ../sim_db.c

build_cpp_program: program.cpp ../sim_db.cpp ../sim_db.hpp ../sim_db.c ../sim_db.h
	${CPP} ${CPPFLAGS} -o cpp_program program.cpp ../sim_db.cpp -xc++ ../sim_db.c

run_c_program: build_c_program
	./c_program --id ${ID}

run_cpp_program: build_cpp_program
	./cpp_program --id ${ID}

clean:
	rm -f c_program
	rm -f cpp_program
