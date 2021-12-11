/*
 * Lance Wilson
 *
 * Purpose: To read in data from a data file containing names and phone numbers, and determine if the name included on the command line is in the file.
 *
 * Input: File called hw5.data, in the format string long-int.
 *
 * Output: Whether the input name is in the address book, and where.
 *
 * Compile: gcc -o hw4-LanceWilson hw4-LanceWilson.c
 *
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct _data {                                 
   char *name;
   long number;
};

int SCAN(FILE *(*stream))
{
    int lines = 0;
    size_t len;
    char *line_ptr = NULL;
    ssize_t read;

    *stream = fopen("hw4.data", "r");
    if (*stream == NULL)
    {
        printf("File could not be opened.\n");
        exit(0);
    }

    while (1)
    {
        read = getline(&line_ptr, &len, *stream);
        if (feof(*stream)) break;
        lines++;
    }

    return lines;
}

struct _data *LOAD(FILE *stream, int size)
{
    int i;
    struct _data *book;
    char *line = NULL;
    size_t len;
    ssize_t read;
    char *name_token;
    char *phone_number_str;
    long phone_number;

    // Return to the beginning of the file.
    rewind(stream);

    if ((book = (struct _data*)calloc(size, sizeof(struct _data))) == NULL)
    {
        printf("ERROR - Could not allocate memory.\n");
        exit(0);
    }
    //book = calloc(size, sizeof(struct _data));

    for (i = 0; i < size; i++)
    {
        // Read in the line (let getline choose the size, since *line is NULL and len isn't specified).
        read = getline(&line, &len, stream);
        // Split the string on a space and get the first token.
        name_token = strtok(line, " ");
        // Get the second token of the same string.
        phone_number_str = strtok(NULL, " ");
        // Convert the second token to a long int.
        phone_number = atoi(phone_number_str);

        // Allocate space for the name in the phone book structure.
        //book[i].name = malloc(strlen(name_token)+1);
        if ((book[i].name = (char*)calloc(strlen(name_token)+1, sizeof(char))) == NULL)
        {
            printf("ERROR - Could not allocate memory.\n");
            exit(0);
        }
        // Copy the name from name_token into the structure.
        strcpy(book[i].name, name_token);
        book[i].number = phone_number;
    }

    free(line);
    fclose(stream);

    return book;
}


void SEARCH(struct _data *BlackBox, char *name, int size)
{
    int j;
    int name_not_found = 1;

    for (j = 0; j < size; j++)
    {
        if (!strcmp(BlackBox[j].name, name))
        {
            printf("*******************************************\n");
            printf("The name was found at the %d entry.\n", j);
            printf("*******************************************\n");

            name_not_found = 0;
        }
    }

    if (name_not_found)
    {
        printf("*******************************************\n");
        printf("The name was NOT found.\n");
        printf("*******************************************\n");
    }
}

void FREE(struct _data *BlackBox, int size)
{
    int i;
    for (i = 0; i < size; i++)
    {
        free(BlackBox[i].name);
    }
    free(BlackBox);
}

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
