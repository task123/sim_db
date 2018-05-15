CC = gcc
CPP = g++
CFLAGS = -lsqlite3
CPPFLAGS = -lsqlite3 -std=c++11

build_c_example: example_program.c ../sim_db.c ../sim_db.h
	${CC} ${CFLAGS} -o c_example example_program.c ../sim_db.c

build_cpp_example: example_program.cpp ../sim_db.cpp ../sim_db.hpp ../sim_db.c ../sim_db.h
	${CPP} ${CPPFLAGS} -o cpp_example example_program.cpp ../sim_db.cpp -xc++ ../sim_db.c

run_c_example: build_c_example # $ make run_c_program ID='id_number'
	./c_example --id ${ID} --path_sim_db ".."

run_cpp_example: build_cpp_example # $ make run_cpp_program ID='id_number'
	./cpp_example --id ${ID} --path_sim_db ".."

clean:
	rm -f c_example
	rm -f cpp_example
	rm -r results/*
