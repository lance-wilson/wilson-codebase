/*
 * Lance Wilson
 *
 * Purpose: To read in data from a data file containing names and phone numbers, and determine if the name included on the command line is in the file.
 *
 * Input: File called hw5.data, in the format string long-int.
 *
 * Output: Whether the input name is in the address book, and where.
 *
 */

#include "hw5-main.h"

int main(int argv, char **argc)
{
    int num_lines;
    FILE *infile;
    struct _data *phone_book;

    // Warn user if there is no name that was searched for.
    if (argv < 2)
    {
        printf("*******************************************\n");
        printf("* You must include a name to search for.  *\n");
        printf("*******************************************\n");

        exit(0);
    }

    // Scan the file to determine its size.
    num_lines = SCAN(&infile);

    // Load the data into the phone book.
    phone_book = LOAD(infile, num_lines);

    // Search the phone book for the input name.
    SEARCH(phone_book, argc[1], num_lines);

    // Free malloc'd memory.
    FREE(phone_book, num_lines);

    return 0;
}
