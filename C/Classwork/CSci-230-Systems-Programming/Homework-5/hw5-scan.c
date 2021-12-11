#include "hw5-scan.h"

int SCAN(FILE *(*stream))
{
    int lines = 0;
    size_t len;
    char *line_ptr = NULL;
    ssize_t read;

    *stream = fopen("hw5.data", "r");
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
