/*
 * Lance Wilson
 *
 * Purpose: to sort the contents of a file of unknown size either high-to-low or low-to-high by the value of either the integers or floating point values.
 *
 * Input: File called hw3.data, in the format string float int string.
 *
 * Output: Sorted values of the data depending on the user menu selection.
 *
 * Compile: gcc -o hw3-LanceWilson hw3-LanceWilson.c
 *
 */

#include <stdio.h>
#include <stdlib.h>

// Prototype of struct Data so that it can be used in all the functions (takes up no space in memory).
struct Data
{
    char type[42];
    float displacement;
    int mileage;
    char color[42];
};

struct Data * file_func(struct Data *arr_of_struct, int *lines)
{
    int i;
    char str1[42], str2[42];
    float flo;
    int integer;
    FILE *infile;
    struct Data thisline;

    infile = fopen("hw3.data", "r");
    if (infile == NULL)
    {
        printf("File could not be opened.\n");
        exit(0);
    }

    *lines = 0;
    while (1)
    {
        fscanf(infile, "%s %f %d %s", str1, &flo, &integer, str2);
        if (feof(infile)) break;
        (*lines)++;
    }

    // Return to the beginning of the file.
    rewind(infile);

    arr_of_struct = calloc(*lines, sizeof(struct Data));

    for (i = 0; i < *lines; i++)
    {
        fscanf(infile, "%s %f %d %s", arr_of_struct[i].type, &arr_of_struct[i].displacement, &arr_of_struct[i].mileage, arr_of_struct[i].color);
    }

    fclose(infile);

    return arr_of_struct;
}

// Utilizes bubble sort.
void sort_by_float(struct Data *arr_of_struct, int *array_length)
{
    int j, k;
    for (j = 0; j < *array_length - 1; j++)
    {
        for (k = 0; k < *array_length-j-1; k++)
        {
            if (arr_of_struct[k].displacement < arr_of_struct[k+1].displacement)
            {
                struct Data temp = arr_of_struct[k];
                arr_of_struct[k] = arr_of_struct[k+1];
                arr_of_struct[k+1] = temp;
            }
        }
    }
}

// Utilizes bubble sort.
void sort_by_int(struct Data *arr_of_struct, int *array_length)
{
    int j, k;
    for (j = 0; j < *array_length - 1; j++)
    {
        for (k = 0; k < *array_length-j-1; k++)
        {
            if (arr_of_struct[k].mileage < arr_of_struct[k+1].mileage)
            {
                struct Data temp = arr_of_struct[k];
                arr_of_struct[k] = arr_of_struct[k+1];
                arr_of_struct[k+1] = temp;
            }
        }
    }
}

void high_low_print(struct Data *arr_of_struct, int *array_length)
{
    int m;

    for (m = 0; m < *array_length; m++)
    {
        printf("%s %f %d %s\n", arr_of_struct[m].type, arr_of_struct[m].displacement, arr_of_struct[m].mileage, arr_of_struct[m].color);
    }
}

void low_high_print(struct Data *arr_of_struct, int *array_length)
{
    int n;

    for (n = *array_length - 1; n >= 0; n--)
    {
        printf("%s %f %d %s\n", arr_of_struct[n].type, arr_of_struct[n].displacement, arr_of_struct[n].mileage, arr_of_struct[n].color);
    }
}

int main()
{
    int menu = 0;
    do
    {
        printf("Menu (Select by typing a number)\n");
        printf("1. Sort data by the float value & print high to low\n");
        printf("2. Sort data by the float value & print low to high\n");
        printf("3. Sort data by the int value & print high to low\n");
        printf("4. Sort data by the int value & print low to high\n");
        printf("5. Exit\n");

        scanf("%d", &menu);

        // Pointer to array of structures.
        struct Data *arr_of_struct;
        int *array_length;

        if (menu != 5)
        {
            array_length = malloc(sizeof(int));
            *array_length = 0;

            // Open file if the user didn't exit.
            arr_of_struct = file_func(arr_of_struct, array_length);
        }

        if (menu == 1 || menu == 2)
        {
            // Sort high to low by floats.
            sort_by_float(arr_of_struct, array_length);
        }
        else if (menu == 3 || menu == 4)
        {
            // Sort high to low by ints.
            sort_by_int(arr_of_struct, array_length);
        }

        if (menu == 1 || menu == 3)
        {
            // Print high to low.
            high_low_print(arr_of_struct, array_length);
        }
        else if (menu == 2 || menu == 4)
        {
            // Print low to high.
            low_high_print(arr_of_struct, array_length);
        }

        if (menu != 5)
        {
            free(arr_of_struct);
            free(array_length);
        }

    } while (menu != 5);

    return 0;
}
