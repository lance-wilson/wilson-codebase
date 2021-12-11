#include "hw5-load.h"

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
