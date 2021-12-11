/* Lance Wilson */

#include "./hw12-B-LanceWilson.h"

void traverse_inorder(_node *tree)
{
    if (tree->left != NULL)
        traverse_inorder(tree->left);
    printf("%d\n", tree->val);
    if (tree->right != NULL)
        traverse_inorder(tree->right);
}
