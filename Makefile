CC = cc
CXX = c++
CFLAGS_RELEASE = -O3 -DNDEBUG
CFLAGS_DEBUG = -g -Wall -Wextra
CXXFLAGS_RELEASE = -O3 -DNDEBUG
CXXFLAGS_DEBUG = -g -Wall -Wextra
CFLAGS = $(CFLAGS_RELEASE)
CXXFLAGS = $(CXXFLAGS_RELEASE)

export CC CXX CFLAGS CXXFLAGS

.PHONY: all generate_commands libsimdb libsimdbcpp clean clean_except_third_party

all:
	$(MAKE) generate_commands
	$(MAKE) libsimdbc
	$(MAKE) libsimdbcpp

generate_commands:
	python src/generate_commands.py

libsimdbc:
	$(MAKE) -C lib libsimdbc.a

libsimdbcpp:
	$(MAKE) -C lib libsimdbcpp.a

clean:
	$(MAKE) -C lib clean
	$(MAKE) -C test clean
	$(MAKE) -C example clean

clean_except_third_party:
	$(MAKE) -C lib clean_except_third_party
	$(MAKE) -C test clean_except_third_party
	$(MAKE) -C example clean_except_third_party

clean_etp:
	$(MAKE) clean_except_third_party
