/* Lance Wilson */

#include "./hw12-A-LanceWilson.h"

void traverse_preorder(_node *tree)
{
    printf("%d\n", tree->val);
    if (tree->left != NULL)
        traverse_preorder(tree->left);
    if (tree->right != NULL)
        traverse_preorder(tree->right);
}
