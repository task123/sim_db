CC = cc
CPP = c++
CFLAGS_RELEASE = -O3 -DNDEBUG -Wall -Wextra
CFLAGS_DEBUG = -g -Wall -Wextra 
CPPFLAGS_RELEASE = -O3 -DNDEBUG -Wall -Wextra
CPPFLAGS_DEBUG = -g -Wall -Wextra
CFLAGS = $(CFLAGS_RELEASE)
CPPFLAGS = $(CPPFLAGS_RELEASE)

export CC CPP CFLAGS CPPFLAGS

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
