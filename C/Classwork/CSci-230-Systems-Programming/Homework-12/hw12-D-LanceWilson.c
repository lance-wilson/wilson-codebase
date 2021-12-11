/* Lance Wilson */

#include "./hw12-D-LanceWilson.h"

void add_to_list(struct listNode *(*head), _node *item)
{
    struct listNode *current, *previous;
    current = NULL;
    previous = NULL;

    // Must make a new node to store the address of item and the address of the next node of the list.
    struct listNode *new_node = (struct listNode *)malloc(sizeof(struct listNode));
    if (new_node == NULL)
    {
        printf("Could not allocate memory\n");
        exit(0);
    }

    new_node->value = item;
    new_node->next = NULL;

    // If the list empty, the new node will be the head.
    if ((*head) == NULL)
    {
        (*head) = new_node;
    }
    else // If the list exists:
    {
        current = (*head);
        while (current)
        {
            previous = current;
            current = current->next;
        }

        previous->next = new_node;
    }

    // Don't need to free these right now because the values they point to are in the list.
    //current = NULL;
    previous = NULL;
    new_node = NULL;

    return;
}

void insert(_node *(*tree), struct listNode *(*head), _node *item)
{
    if(!(*tree))
    {
        *tree = item;
        add_to_list(&(*head), item);
        return;
    }
    if (item->val < (*tree)->val)
        insert(&(*tree)->left, &(*head), item);
    if (item->val > (*tree)->val)
        insert(&(*tree)->right, &(*head), item);
}

void display_list_forward(struct listNode *head)
{
    struct listNode *current = NULL;
    current = head;

    printf("Print list in alphabetical order (from head to tail):\n");

    while (current) {
        printf("%d\n", current->value->val);
        current = current->next ;
    }
    // Current is null once the while loop is finished.

    return;
}

void free_list(struct listNode *(*head))
{
    // Start at the head.
    struct listNode *current = (*head);

    while ((*head))
    {
        // Move the head to the next element in the list.
        (*head) = current->next;
        current->next = NULL;
        // Free the value in the tree that current points to.
        free(current->value);
        // Free the current element.
        free(current);
        // Move current to point at the new head.
        current = (*head);
    }

    return;
}
