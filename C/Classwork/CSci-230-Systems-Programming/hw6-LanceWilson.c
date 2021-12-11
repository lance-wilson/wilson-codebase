/*
 * Lance Wilson
 *
 * Purpose: To read in data from a data file containing a paragraph and determine which words appear the most often.
 *
 * Input: File called hw6.data, in the form of a paragraph.
 *
 * Output: A list of the top ten most frequent words.
 *
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

struct _data {                                 
   char word[50];
   int occurrence;
};

int SCAN(FILE *(*stream), char* filename)
{
    int lines = 0;
    char str1[50];

    *stream = fopen(filename, "r");
    if (*stream == NULL)
    {
        printf("File could not be opened.\n");
        exit(0);
    }

    while (1)
    {
        fscanf(*stream, "%s", str1);
        if (feof(*stream)) break;
        lines++;
    }

    return lines;
}

struct _data *LOAD(FILE *stream, int size)
{
    int i, j, letter;
    struct _data *tag_cloud;
    char str1[50];

    // Return to the beginning of the file.
    rewind(stream);

    tag_cloud = (struct _data*)calloc(size, sizeof(struct _data));

    if (tag_cloud == NULL)
    {
        printf("ERROR - Could not allocate memory.\n");
        exit(0);
    }

    for (i = 0; i < size; i++)
    {
        // Read in the word.
        fscanf(stream, "%s", str1);
        // Remove punctuation.
        for (letter = 0; letter < strlen(str1); letter++)
        {
            // If looking at the last character of the string, and it's punctuation, set it to the null character.
            if (ispunct(str1[letter]) && str1[letter+1] == '\0')
            {
                str1[letter] = '\0';
            }
            // If the character is punctuation and it's not the last of the string, delete the punctuation character by shifting the other characters to the left.
            if (ispunct(str1[letter]) && str1[letter+1] != '\0')
            {
                for (j = letter; j < strlen(str1); j++)
                {
                    str1[j] = str1[j+1];
                }
                // If the next character is also punctuation this character is now the last character of the string, decrement letter so that the loop will re-run on this character to make sure it is valid.
                if (ispunct(str1[letter+1]) || str1[letter+1] == '\0')
                {
                    letter--;
                }
            }

            // Convert the letter to lowercase.
            str1[letter] = tolower(str1[letter]);
        }

        strcpy(tag_cloud[i].word, str1);
        tag_cloud[i].occurrence = 1;
    }

    fclose(stream);

    return tag_cloud;
}

// Go through the list of words, and for each word, run through the rest of the words and check for string equality. If they are the same, the current word's occurrence count will be incremented, while the matching word is set to zero, so that on future iterations it will not be checked again.
void WORDCOUNT(struct _data *tag_cloud, int size)
{
    int j, k;

    for (j = 0; j < size; j++)
    {
        if (tag_cloud[j].occurrence != 0)
        {
            for (k = j+1; k < size; k++)
            {
                // Check if each word is equal.
                if (!strcmp(tag_cloud[j].word, tag_cloud[k].word))
                {
                    tag_cloud[j].occurrence++;
                    tag_cloud[k].occurrence = 0;
                }
            }
        }
    }
}

// Sort the words by the number of occurrences, largest to smallest, using the bubble sort.
void WORDSORT(struct _data *tag_cloud, int size)
{
    int i, j, k;
    for (j = 0; j < size - 1; j++)
    {
        for (k = 0; k < size-j-1; k++)
        {
            if (tag_cloud[k].occurrence < tag_cloud[k+1].occurrence)
            {
                struct _data temp = tag_cloud[k];
                tag_cloud[k] = tag_cloud[k+1];
                tag_cloud[k+1] = temp;
            }
        }
    }

    // Print the ten most frequent words and how many times they occur.
    for (i = 0; i < 10; i++)
    {
        printf("%s\t%d\n", tag_cloud[i].word, tag_cloud[i].occurrence);
    }
}

void FREE(struct _data *tag_cloud)
{
    free(tag_cloud);
    tag_cloud = NULL;
}

int main(int argv, char **argc)
{
    int num_lines;
    FILE *infile;
    struct _data *tag_cloud;

    // Warn user if there is no name that was searched for.
    if (argv < 2)
    {
        printf("*******************************************\n");
        printf("* You must include a file name to open.   *\n");
        printf("*******************************************\n");

        exit(0);
    }

    // Scan the file to determine its size.
    num_lines = SCAN(&infile, argc[1]);

    // Load the words into a structure.
    tag_cloud = LOAD(infile, num_lines);

    // Determine which words are most frequent.
    WORDCOUNT(tag_cloud, num_lines);

    // Sort the words by which are most frequent, print the ten most common.
    WORDSORT(tag_cloud, num_lines);

    // Free calloc'd memory.
    FREE(tag_cloud);

    return 0;
}
