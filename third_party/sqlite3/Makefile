CFLAGS = -std=c99 -O2 -DNDEBUG
CC := $(if $(CC), $(CC), cc)

sqlite3.o: sqlite3.c sqlite3.h
	@echo "Compiling SQLite3..."
	@echo "(May take 10-30 seconds.)"
	$(CC) $(CFLAGS) -c -o $@ sqlite3.c 

.PHONY: clean
clean:
	rm -f sqlite3.o
