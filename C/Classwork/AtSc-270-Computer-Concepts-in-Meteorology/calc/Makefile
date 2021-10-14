#
# Makefile for compiling the calc.c program, linking the my_math.c file
#
# Syntax: make
#
# Written: Lance Wilson, April 2016
#

all: calc

# Create calc.o
calc.o: calc.c
	gcc -c calc.c

# Create my_math.o
my_math.o: my_math.c
	gcc -c my_math.c

# Create calc executable file
calc: calc.o my_math.o
	gcc -o calc calc.o my_math.o
