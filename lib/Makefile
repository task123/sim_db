CFLAGS_RELEASE = -std=c99 -O2 -DNDEBUG
CXXFLAGS_RELEASE = -O3 -DNDEBUG
CFLAGS := $(if $(CFLAGS), $(CFLAGS), $(CFLAGS_RELEASE))
CXXFLAGS := $(if $(CXXFLAGS), $(CXXFLAGS), $(CXXFLAGS_RELEASE))

CC := $(if $(CC), $(CC), cc)
CXX := $(if $(CXX), $(CXX), c++)

.PHONY: all libsimdbc libsimdbcpp clean clean_except_third_party clean_etp

all:
	$(MAKE) libsimdbc.a
	$(MAKE) libsimdbcpp.a

libsimdbc.a: ../src_c_and_cpp/sim_db.o ../third_party/sqlite3/sqlite3.o
	ar -rc libsimdbc.a $^ 

libsimdbcpp.a: ../src_c_and_cpp/sim_db_cpp.o ../src_c_and_cpp/sim_db.o ../third_party/sqlite3/sqlite3.o
	ar -rc libsimdbcpp.a $^

../src_c_and_cpp/sim_db.o: ../src_c_and_cpp/sim_db.c ../include/sim_db.h
	$(CC) $(CFLAGS) -c -o $@ ../src_c_and_cpp/sim_db.c

../src_c_and_cpp/sim_db_cpp.o: ../src_c_and_cpp/sim_db.cpp ../include/sim_db.hpp ../include/sim_db.h
	$(CXX) $(CXXFLAGS) -c -o $@ ../src_c_and_cpp/sim_db.cpp

../third_party/sqlite3/sqlite3.o:
	$(MAKE) -C ../third_party/sqlite3/ sqlite3.o

clean:
	$(MAKE) clean_except_third_party
	$(MAKE) -C ../third_party/sqlite3 clean

clean_except_third_party:
	rm -f libsimdbc.a
	rm -f libsimdbcpp.a
	rm -f ../src_c_and_cpp/sim_db.o
	rm -f ../src_c_and_cpp/sim_db_cpp.o

clean_etp:
	$(MAKE) clean_except_third_party
