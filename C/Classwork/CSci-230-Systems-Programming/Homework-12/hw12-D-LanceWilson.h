/* Lance Wilson */

#include <stdio.h>
#include <stdlib.h>

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

void add_to_list(struct listNode *(*head), _node *item);

void insert(_node *(*tree), struct listNode *(*head), _node *item);

void display_list_forward(struct listNode *head);

void free_list(struct listNode *(*head));
