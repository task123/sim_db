CC = cc
CXX = c++
FC = gfortran
CFLAGS_RELEASE = -std=c99 -O3 -DNDEBUG
CFLAGS_DEBUG = -std=c99 -Wall
CXXFLAGS_RELEASE = -O3 -DNDEBUG
CXXFLAGS_DEBUG = -Wall
CFLAGS = $(CFLAGS_RELEASE)
CXXFLAGS = $(CXXFLAGS_RELEASE)

export CC CXX FC CFLAGS CXXFLAGS

.PHONY: all install include add_to_path libs clib cpplib build_dist upload_pypi clean clean_except_third_party clean_etp

all:
	$(MAKE) libs

install:
	$(MAKE) libs
	python setup.py install

include:
	$(MAKE) add_to_path
	$(MAKE) libs

add_to_path:
	python sim_db/src_command_line_tool/add_command_line_tool_to_path.py

libs:
	$(MAKE) -C src libs

clib:
	$(MAKE) -C src clib

cpplib:
	$(MAKE) -C src cpplib

build_dist:
	python setup.py sdist bdist_wheel

upload_pypi:
	twine upload dist/*

clean:
	rm -fr build
	rm -fr dist
	rm -fr sim_db.egg-info
	$(MAKE) -C src clean
	$(MAKE) -C tests clean
	$(MAKE) -C examples clean

clean_except_third_party:
	rm -fr build
	rm -fr dist
	rm -fr sim_db.egg-info
	$(MAKE) -C src clean_except_third_party
	$(MAKE) -C tests clean_except_third_party
	$(MAKE) -C examples clean_except_third_party

clean_etp:
	$(MAKE) clean_except_third_party
