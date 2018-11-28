CC = cc
CXX = c++
CFLAGS_RELEASE = -std=c99 -O3 -DNDEBUG
CFLAGS_DEBUG = -std=c99 -g -Wall -Wextra
CXXFLAGS_RELEASE = -O3 -DNDEBUG
CXXFLAGS_DEBUG = -g -Wall -Wextra
CFLAGS = $(CFLAGS_RELEASE)
CXXFLAGS = $(CXXFLAGS_RELEASE)

export CC CXX CFLAGS CXXFLAGS

.PHONY: all command_line_tool libsimdb libsimdbcpp clean clean_except_third_party

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

clean:
	rm -fr build
	rm -fr dist
	rm -fr sim_db.egg-info
	$(MAKE) -C lib clean
	$(MAKE) -C test clean
	$(MAKE) -C example clean

clean_except_third_party:
	rm -fr build
	rm -fr dist
	rm -fr sim_db.egg-info
	$(MAKE) -C lib clean_except_third_party
	$(MAKE) -C test clean_except_third_party
	$(MAKE) -C example clean_except_third_party

clean_etp:
	$(MAKE) clean_except_third_party
