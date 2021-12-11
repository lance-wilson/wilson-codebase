/*
 * Lance Wilson
 *
 * Purpose: To create a double linked list based on names and action codes in a text file, and print the list both from head to tail (alphabetical order) and tail to head (reverse alphabetical order).
 *
 * Input: A file containing a list of names, and a code whether to add or delete that name.
 *
 * Output: The names in the list in alphabetical and reverse-alphabetical order.
 *
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct node { 
    char name[42];
    struct node *next, *prev;
};

void add_name(struct node *(*head), struct node *(*tail), char input_name[])
{
    struct node *current, *previous;
    current = NULL;
    previous = NULL;

    struct node *new_node = (struct node *)malloc(sizeof(struct node));
    if (new_node == NULL)
    {
        printf("Could not allocate memory\n");
        exit(0);
    }

    strcpy(new_node->name, input_name);
    new_node->next = NULL;
    new_node->prev = NULL;

    // If the list empty, the new node will be both the head and the tail.
    if ((*head) == NULL)
    {
        (*head) = new_node;
        (*tail) = new_node;
    }
    else // If the list exists:
    {
        // First case: the new node belongs at the beginning of the list;
        //             set the new node to be the head.
        if (strcmp(new_node->name, (*head)->name) < 0)
        {
            new_node->next = (*head);
            (*head)->prev = new_node;
            (*head) = new_node;
        }
        // Second case: the new node belongs at the end of the list;
        //              set the new node to be the tail.
        else if (strcmp(new_node->name, (*tail)->name) > 0)
        {
            (*tail)->next = new_node;
            new_node->prev = (*tail);
            (*tail) = new_node;
        }
        // Third case: the new node belongs somewhere between the head and tail;
        //             perform an insertion sort to add.
        else if (strcmp(new_node->name, (*head)->name) > 0 && strcmp(new_node->name, (*tail)->name) < 0)
        {
            current = (*head);
            // Loop through the list until the "current" node is alphabetically after the new node. This will mean that the new node fits between nodes previous and current.
            while (strcmp(new_node->name, current->name) > 0)
            {
                previous = current;
                current = current->next;
            }

            // If the new node's value is equal to the current's value, skip adding the node to the list; otherwise, add it into the list.
            if (strcmp(new_node->name, current->name) != 0)
            {
                new_node->prev = previous;
                new_node->next = current;
                current->prev = new_node;
                previous->next = new_node;
            }
        }
    }

    // Don't need to free these because the values they point to are in the list.
    current = NULL;
    previous = NULL;
    new_node = NULL;

    return;
}

void delete_name(struct node *(*head), struct node *(*tail), char input_name[])
{
    struct node *to_delete, *previous, *current, *next_node;
    to_delete  = NULL;
    previous = NULL;
    current = NULL;
    next_node = NULL;

    // Only try to remove the value if there are nodes in the list.
    if ((*head) != NULL)
    {
        // First case: the node to be deleted is the head of the list.
        if (strcmp(input_name, (*head)->name) == 0)
        {
            to_delete = (*head);
            (*head) = (*head)->next;
            (*head)->prev = NULL;

            to_delete->next = NULL;
            free(to_delete);
            to_delete = NULL;
        }
        // Second case: the node to be deleted is the tail of the list.
        else if (strcmp(input_name, (*tail)->name) == 0)
        {
            to_delete = (*tail);
            (*tail) = (*tail)->prev;
            (*tail)->next = NULL;

            to_delete->prev = NULL;
            free(to_delete);
            to_delete = NULL;
        }
        // Third case: the node to delete (if it exists) is somewhere between the head and tail.
        else if (strcmp(input_name, (*head)->name) > 0 && strcmp(input_name, (*tail)->name) < 0)
        {
            current = (*head);
            // Loop through the list until the "current" node is alphabetically after the new node. This will mean that the deleted node, if it is in the list, is equal to current.
            while (strcmp(input_name, current->name) > 0)
            {
                previous = current;
                current = current->next;
            }

            // If the deleted node's value is equal to the current's value, delete that node from the list; otherwise, it is not in the list and doesn't need to be deleted.
            if (strcmp(input_name, current->name) == 0)
            {
                to_delete = current;
                next_node = current->next;
                previous->next = next_node;
                next_node->prev = previous;

                // Free the node to be deleted.
                to_delete->next = NULL;
                to_delete->prev = NULL;
                free(to_delete);
                to_delete = NULL;
            }
        }
        // If the node that was to be deleted was before the head or after the tail (i.e. it was not in the list), there is no case, so that name is skipped.
    }

    return;
}

void display_list_forward(struct node *head)
{
    struct node *current = NULL;
    current = head;

    printf("Print list in alphabetical order (from head to tail):\n");

    while (current) {
        printf("%s\n", current->name);
        current = current->next ;
    }
    // Current is null once the while loop is finished.

    return;
}

void display_list_back(struct node *tail)
{
    struct node *current = NULL;
    current = tail;

    printf("Print list in reverse alphabetical order (from tail to head):\n");

    while (current) {
        printf("%s\n", current->name);
        current = current->prev ;
    }
    // Current is null once the while loop is finished.

    return;
}

void free_list(struct node *(*head), struct node *(*tail))
{
    // Start at the head.
    struct node *current = (*head);

    while ((*head))
    {
        // Move the head to the next element in the list.
        (*head) = current->next;
        if ((*head))
        {
            (*head)->prev = NULL;
        }
        current->next = NULL;
        // Free the current element.
        free(current);
        // Move current to point at the new head.
        current = (*head);
    }

    (*tail) = NULL;

    return;
}

int main()
{
    int search, i;
    char op_code;
    char input_name[42];
    struct node *head, *tail;
    head = NULL;
    tail = NULL;
    FILE *stream;

    stream = fopen("hw8.data", "r");
    if (stream == NULL)
    {
        printf("File could not be opened.\n");
        exit(0);
    }

    while (!feof(stream))
    {
        fscanf(stream, "%s %c", input_name, &op_code);

        if (op_code == 'a')
        {
            add_name(&head, &tail, input_name);
        }
        else if (op_code == 'd')
        {
            delete_name(&head, &tail, input_name);
        }
    }

    display_list_forward(head);
    printf("\n");
    display_list_back(tail);

    free_list(&head, &tail);

    return 0;
}
