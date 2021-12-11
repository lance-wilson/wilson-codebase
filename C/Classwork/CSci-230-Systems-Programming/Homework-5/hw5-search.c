#include "hw5-search.h"

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
