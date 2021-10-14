// my_math.c
//
// Purpose: Calculates the average and maximum of two input numbers, and prints out
//          the solutions.
//
// Input: None
//
// Output: None
//
// Compile: gcc -c my_math.c
//
// Requires my_math.h header and my_math.c source file
//
// Written: Lance Wilson, Apr 2016
//
#include <stdio.h>
#include "my_math.h"

// Calculate the average of two numbers
void avg(float num1, float num2)
{
    // Calculate average
    float avg = (num1 + num2)/2;

    printf("Average: %.2f\n", avg);
}  // End of avg

// Calculate the maximum of two numbers
void max(float num1, float num2)
{
    float max;
    // Find max
    if (num1 > num2)
    {
        max = num1;
    }
    else
    {
        max = num2;
    }

    printf("Max: %.2f\n", max);
} // End of max
