// calc.c
//
// Purpose: Calculates the average and maximum of two numbers entered by the user, and prints out
//          the solutions.
//
// Input: Two User-defined numbers
//
// Output: Print out of average and maximum number
//
// Compile: gcc -c my_math.c
//          gcc -o calc calc.c my_math.o
//
// Syntax: ./calc
//
// Requires my_math.h header and my_math.c source file
//
// Written: Lance Wilson, Apr 2016
//
#include <stdio.h>
#include "my_math.h"

int main()
{
    float num1, num2;  // Numbers

    // Ask for first number as input
    printf("Enter the first number:\n");
    scanf("%f", &num1);

    // Ask for second number as input
    printf("Enter the second number:\n");
    scanf("%f", &num2);

    // Calculate the average of the inputs
    avg(num1, num2);

    // Find the maximum number of the inputs
    max(num1, num2);

}  // End of main

