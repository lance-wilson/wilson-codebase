CC=gcc
CFLAGS=-c -Wall

all: hw5-main.o hw5-scan.o hw5-load.o hw5-search.o hw5-free.o
	$(CC) hw5-main.o hw5-scan.o hw5-load.o hw5-search.o hw5-free.o -o hw5
hw5-main.o: hw5-main.c
	$(CC) $(CFLAGS) hw5-main.c 
hw5-scan.o: hw5-scan.c
	$(CC) $(CFLAGS) hw5-scan.c 
hw5-load.o: hw5-load.c
	$(CC) $(CFLAGS) hw5-load.c 
hw5-search.o: hw5-search.c
	$(CC) $(CFLAGS) hw5-search.c 
hw5-free.o: hw5-free.c
	$(CC) $(CFLAGS) hw5-free.c
clean:
	rm hw5 *.o
