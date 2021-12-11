/* Lance Wilson */

#include "./hw12-C-LanceWilson.h"

void traverse_postorder(_node *tree)
{
    if (tree->left != NULL)
        traverse_postorder(tree->left);
    if (tree->right != NULL)
        traverse_postorder(tree->right);
    printf("%d\n", tree->val);
}
