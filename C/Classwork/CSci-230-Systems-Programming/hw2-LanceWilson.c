/*
 * Lance Wilson
 *
 * Purpose: to alphabetically merge three word list files.
 *
 * Input: Three files called american0.txt, american1.txt, and american2.txt.
 *
 * Output: An alphabetized text file called words.txt.
 *
 * Compile: gcc -o hw2-LanceWilson hw2-LanceWilson.c
 *
 */
#include <stdio.h>
#include <stdlib.h>

int main()
{
    // Returned status for the system command.
    int return_value;

    // Take the three files, sort them, and then output to words.txt.
    return_value = system("cat american0.txt american1.txt american2.txt | sort > words.txt");

    return 0;
}
