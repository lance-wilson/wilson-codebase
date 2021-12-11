/*
 * Lance Wilson
 *
 * Purpose: To create a binary tree based on integers provided in a file, and print out the numbers in the order they were inserted (linked list order), and in pre-, in-, and post-order of the tree.
 *
 * Input: A file containing a set of non-repeating integers (one per line).
 *
 * Output: The integers printed out in pre-, in-, and post-order, as well as the linked list order (the order in which they were inserted).
 *
 */

#include <stdio.h>
#include <stdlib.h>

struct myTree {
    int val;
    struct myTree *left, *right;
};

struct listNode
{
    struct myTree *value;
    struct listNode *next;
};

typedef struct myTree _node;

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

void traverse_inorder(_node *tree)
{
    if (tree->left != NULL)
        traverse_inorder(tree->left);
    printf("%d\n", tree->val);
    if (tree->right != NULL)
        traverse_inorder(tree->right);
}

void traverse_preorder(_node *tree)
{
    printf("%d\n", tree->val);
    if (tree->left != NULL)
        traverse_preorder(tree->left);
    if (tree->right != NULL)
        traverse_preorder(tree->right);
}

void traverse_postorder(_node *tree)
{
    if (tree->left != NULL)
        traverse_postorder(tree->left);
    if (tree->right != NULL)
        traverse_postorder(tree->right);
    printf("%d\n", tree->val);
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

int main()
{
    _node *root, *current;
    struct listNode *head;
    int input_num;
    root = NULL;
    head = NULL;
    FILE *stream;

    stream = fopen("hw9.data", "r");
    if (stream == NULL)
    {
        printf("File could not be opened.\n");
        exit(0);
    }

    while (!feof(stream))
    {
        current = (_node *)malloc(sizeof(_node));
        current->left = current->right = NULL;
        fscanf(stream, "%d", &input_num);
        current->val = input_num;
        insert(&root, &head, current);
    }

    printf("In order:\n");
    traverse_inorder(root);
    printf("\n\n");
    printf("Pre-order:\n");
    traverse_preorder(root);
    printf("\n\n");
    printf("Post-order:\n");
    traverse_postorder(root);
    printf("\n\n");
    printf("Linked list:\n");
    display_list_forward(head);

    free_list(&head);

    return 0;
}
