CC = cc
CXX = c++
CFLAGS_RELEASE = -O3 -DNDEBUG
CFLAGS_DEBUG = -std=c99 -Wall -Wextra
CXXFLAGS_RELEASE = -O3 -DNDEBUG
CXXFLAGS_DEBUG = -Wall -Wextra
CFLAGS = $(CFLAGS_DEBUG)
CXXFLAGS = $(CXXFLAGS_DEBUG)

export CC CXX CFLAGS CXXFLAGS

.PHONY: all install include add_to_path libs libsimdb libsimdbcpp clean clean_except_third_party clean_etp

all:
	$(MAKE) install 

install:
	$(MAKE) libs
	python setup.py install

include:
	$(MAKE) add_to_path
	$(MAKE) libs

add_to_path:
	python sim_db/src_command_line_tool/add_command_line_tool_to_path.py

libs:
	$(MAKE) libsimdbc
	$(MAKE) libsimdbcpp

libsimdbc:
	$(MAKE) -C lib libsimdbc.a

libsimdbcpp:
	$(MAKE) -C lib libsimdbcpp.a

build_dist:
	python setup.py sdist bdist_wheel

clean:
	rm -fr build
	rm -fr dist
	rm -fr sim_db.egg-info
	$(MAKE) -C lib clean
	$(MAKE) -C tests clean
	$(MAKE) -C examples clean

clean_except_third_party:
	rm -fr build
	rm -fr dist
	rm -fr sim_db.egg-info
	$(MAKE) -C lib clean_except_third_party
	$(MAKE) -C tests clean_except_third_party
	$(MAKE) -C examples clean_except_third_party

clean_etp:
	$(MAKE) clean_except_third_party
