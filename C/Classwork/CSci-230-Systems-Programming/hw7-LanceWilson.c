/*
 * Lance Wilson
 *
 * Purpose: To search through a pointer-based linked-list and find if a number is in that list.
 *
 * Input: User input of a value to search for.
 *
 * Output: The values in the list in ascending order, and a pair of the value to search for, and the value that was found (is -1 if no value was found).
 *
 */

#include <stdio.h>
#include <stdlib.h>

struct node { 
    int data;
    struct node *next;
};

typedef struct node link;

link *searchList(int value, link *head)
{
    // Loop through each node. If the value is found, return the value.
    while (head)
    {
        if (head->data == value)
        {
            return head;
        }
        // Since the last value was set to -1, -1 will be returned if the value wasn't found in the list.
        if (head->next == NULL)
        {
            return head;
        }
        head = head->next;
    }
}

void FreeLinked(struct node *(*head)) // Call as (*head)
{
    // Start at the head.
    link *current = (*head);
    while ((*head))
    {
        // Move the head to the next element in the list.
        (*head) = current->next;
        // Free the current element.
        free(current);
        // Move current to point at the new head.
        current = (*head);
    }

    return;
}

int main()
{
    int search, i;
    struct node *head, *current, *previous;
    head = NULL;
    current = NULL;
    previous = NULL;

    head = (struct node *) malloc(sizeof(struct node));
    if (head == NULL)
    {
        printf("Could not allocate memory\n");
        exit(0);
    }

    // Fake node to streamline for loop and make printing easier.
    head->data = -1;
    head->next = NULL;

    previous = head;

    // Add the "real" data nodes to the list.
    for (i = 0; i < 9; i++)
    {
        current = (struct node *) malloc(sizeof(struct node));
        if (current == NULL)
        {
            printf("Could not allocate memory\n");
            exit(0);
        }
        current->data = i;
        current->next = NULL;
        previous->next = current;
        previous = current;
    }

    // Add another fake node to the end.
    current = (link *) malloc(sizeof(link));
    if (current == NULL)
    {
        printf("Could not allocate memory\n");
        exit(0);
    }
    current->data = -1;
    current->next = NULL;
    previous->next = current;
    // Remove the reference of previous to any node in the list so that it can't point to non-existant data later (note this isn't losing the data, since the node pointed to by previous is still in the list).
    previous = NULL;

    // Reset current to head for printing.
    current = head;

    while (current) {
        printf("%d\n", current->data);
        current = current->next ;
    }
    // Current is null once the while loop is finished.

    // Ask for value to search for.
    printf("Enter a value to search for:\n");
    scanf("%d", &search);

    // Print Value to be searched, and what the function found (the second value will be -1 if the value isn't found in the list).
    printf("[%d %d]\n", search, searchList(search, head)->data);

    FreeLinked(&head);

    return 0;
}
