/*
 * Lance Wilson
 *
 * Purpose: To load in code that can be used for an injection an prevent it from taking advantage of buffer overflow.
 *
 * Input: A file containing code that can be used for an injection.
 *
 * Output: A print out of the buffer address, the input data, and the contents of the buffer.
 *
 * Compile:  gcc -m64 hw11-LanceWilson.c -o hw11-LanceWilson -z execstack -fno-stack-protector
 *
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main()
{
    char buffer[256];
    FILE *stream;
    size_t len;
    char *line_ptr = NULL;

    stream = fopen("hw11.data", "r");
    if (stream == NULL)
    {
        printf("File could not be opened.\n");
        exit(0);
    }

    getline(&line_ptr, &len, stream);

    fclose(stream);

    strncpy(buffer, line_ptr, 255);
    buffer[255] = '\0';

    printf("Buffer Address: %p\n\n", buffer);

    printf("File Contents: %s\n", line_ptr);

    free(line_ptr);
    line_ptr = NULL;

    printf("Buffer Contents: %s\n", buffer);

    return 0;
}
