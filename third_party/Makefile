BUILD_DIR = ../build/third_party

CFLAGS = -O2 -DNDEBUG
CC := $(if $(CC), $(CC), cc)

$(BUILD_DIR)/sqlite3.o: sqlite3.c sqlite3.h
	@echo "Compiling SQLITE3..."
	@echo "(May take 10-30 seconds.)"
	$(CC) $(CFLAGS) -c -o $@ sqlite3.c 

.PHONY: clean
clean:
	rm -f $(BUILD_DIR)/sqlite3.o
