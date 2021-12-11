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
#include <dlfcn.h>

#ifndef _linker_
#define _linker_
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
#endif

int main()
{
    _node *root, *current;
    struct listNode *head;
    int input_num;
    root = NULL;
    head = NULL;
    void *handle;
    FILE *stream;

    void (*traverse_preorder)(_node *tree);
    void (*traverse_inorder)(_node *tree);
    void (*traverse_postorder)(_node *tree);
    void (*add_to_list)(struct listNode *(*head), _node *item);
    void (*insert)(_node *(*tree), struct listNode *(*head), _node *item);
    void (*display_list_forward)(struct listNode *head);
    void (*free_list)(struct listNode *(*head));

    handle = dlopen("./hw12-lib-LanceWilson.so", RTLD_LAZY);
    if (!handle)
    {
        dlerror();
    }

    stream = fopen("hw9.data", "r");
    if (stream == NULL)
    {
        printf("File could not be opened.\n");
        exit(0);
    }

    insert = dlsym(handle, "insert");

    while (!feof(stream))
    {
        current = (_node *)malloc(sizeof(_node));
        current->left = current->right = NULL;
        fscanf(stream, "%d", &input_num);
        current->val = input_num;
        (*insert)(&root, &head, current);
    }

    traverse_inorder = dlsym(handle, "traverse_inorder");
    traverse_preorder = dlsym(handle, "traverse_preorder");
    traverse_postorder = dlsym(handle, "traverse_postorder");
    display_list_forward = dlsym(handle, "display_list_forward");

    printf("In order:\n");
    (*traverse_inorder)(root);
    printf("\n\n");
    printf("Pre-order:\n");
    (*traverse_preorder)(root);
    printf("\n\n");
    printf("Post-order:\n");
    (*traverse_postorder)(root);
    printf("\n\n");
    printf("Linked list:\n");
    (*display_list_forward)(head);

    free_list = dlsym(handle, "free_list");
    (*free_list)(&head);

    dlclose(handle);

    return 0;
}
