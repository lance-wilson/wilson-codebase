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

void traverse_inorder(_node *tree);
