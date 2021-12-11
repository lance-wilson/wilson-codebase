/*
 * Lance Wilson
 *
 * Purpose: To take in a poem and a codex list, and use the codex to translate the poem and correct its spelling.
 *
 * Input: A file containing a poem, and a codex file containing the translation for the misspelled words.
 *
 * Output: A print out of the corrected poem.
 *
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

struct node {
  char *word;
  struct node *next;
};

struct codex {
  char *word1;
  char *word2;
  struct codex *next;
};

void add_to_list(struct node *(*head), char *(*new_word))
{
    struct node *current, *previous;
    char *added_word;
    current = NULL;
    previous = NULL;

    // Must make a new node to store the address of item and the address of the next node of the list.
    struct node *new_node = (struct node *)malloc(sizeof(struct node));
    if (new_node == NULL)
    {
        printf("Could not allocate memory\n");
        exit(0);
    }

    // Create a new word so that we can keep track of the memory address of this string after exiting the function (and free line_ptr).
    added_word = (char *)malloc(sizeof((*new_word)));
    if (added_word == NULL)
    {
        printf("ERROR - Could not allocate memory.\n");
        exit(0);
    }
    strcpy(added_word, (*new_word));

    new_node->word = added_word;
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
    current = NULL;
    previous = NULL;
    new_node = NULL;

    return;
}

void add_to_codex(struct codex *(*head), char *(*new_word1), char *(*new_word2))
{
    struct codex *current, *previous;
    char *added_word1, *added_word2;
    current = NULL;
    previous = NULL;

    // Must make a new node to store the address of item and the address of the next node of the list.
    struct codex *new_node = (struct codex *)malloc(sizeof(struct codex));
    if (new_node == NULL)
    {
        printf("Could not allocate memory\n");
        exit(0);
    }

    // Create a new word so that we can keep track of the memory address of this string after exiting the function (and free line_ptr).
    added_word1 = (char *)malloc(sizeof((*new_word1)));
    if (added_word1 == NULL)
    {
        printf("ERROR - Could not allocate memory.\n");
        exit(0);
    }
    strcpy(added_word1, (*new_word1));

    added_word2 = (char *)malloc(sizeof((*new_word2)));
    if (added_word2 == NULL)
    {
        printf("ERROR - Could not allocate memory.\n");
        exit(0);
    }
    strcpy(added_word2, (*new_word2));

    new_node->word1 = added_word1;
    new_node->word2 = added_word2;
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
    current = NULL;
    previous = NULL;
    new_node = NULL;

    return;
}

void load_poem(struct node *(*head))
{
    int i;
    int num_lines = 0;
    char *this_word, *added_word;
    size_t len;
    char *line_ptr = NULL;
    ssize_t read;
    FILE *stream;

    stream = fopen("hw10data.txt", "r");
    if (stream == NULL)
    {
        printf("File could not be opened.\n");
        exit(0);
    }

    // Determine the number of lines in the file.
    while (1)
    {
        line_ptr = NULL;
        read = getline(&line_ptr, &len, stream);
        if (feof(stream)) break;
        num_lines++;

        free(line_ptr);
        line_ptr = NULL;
    }

    // Return to the beginning of the file.
    rewind(stream);

    for (i = 0; i < num_lines; i++)
    {
        // Read in the line (let getline choose the size, since *line is NULL and len isn't specified).
        read = getline(&line_ptr, &len, stream);

        this_word = strtok(line_ptr, " ");

        while (this_word != NULL)
        {
            add_to_list(&(*head), &this_word);
            this_word = strtok(NULL, " ");
        }

        free(line_ptr);
        line_ptr = NULL;
    }

    fclose(stream);

    return;
}

void load_codex(struct codex *(*head))
{
    int i;
    int num_lines = 0;
    char *this_word1, *this_word2, *added_word1, *added_word2;
    size_t len;
    char *line_ptr = NULL;
    ssize_t read;
    FILE *stream;

    stream = fopen("hw10codex.txt", "r");
    if (stream == NULL)
    {
        printf("File could not be opened.\n");
        exit(0);
    }

    // Determine the number of lines in the file.
    while (1)
    {
        read = getline(&line_ptr, &len, stream);
        if (feof(stream)) break;
        num_lines++;

        free(line_ptr);
        line_ptr = NULL;
    }

    // Return to the beginning of the file.
    rewind(stream);

    for (i = 0; i < num_lines; i++)
    {
        // Read in the line (let getline choose the size, since *line_ptr is NULL and len isn't specified).
        read = getline(&line_ptr, &len, stream);

        this_word1 = strtok(line_ptr, " ");
        this_word2 = strtok(NULL, " \n");

        add_to_codex(&(*head), &this_word1, &this_word2);

        free(line_ptr);
        line_ptr = NULL;
    }

    fclose(stream);

    return;
}

void translate(struct node *(*list_head), struct codex *codex_head)
{
    struct node *list_current, *list_previous;
    struct codex *codex_current;
    list_current = (*list_head);
    list_previous = list_current;

    while (list_current)
    {
        codex_current = codex_head;

        while (codex_current)
        {
            // If the word in the list matches a word in the codex, but isn't a skipped word, it needs to be replaced.
            // (strstr checks if the second string is found within the first; needed because some words have punctuation/new lines).
            if (strstr(list_current->word, codex_current->word1) != NULL && strcmp(codex_current->word2, "skip") != 0)
            {
                // Make a new node to add to the list.
                struct node *new_node = (struct node *)malloc(sizeof(struct node));
                if (new_node == NULL)
                {
                    printf("ERROR - Could not allocate memory.\n");
                    exit(0);
                }
                // Create space for a word in the new node, same size as the replacement word in the codex.
                new_node->word = (char *)malloc(sizeof(codex_current->word2));
                if (new_node->word == NULL)
                {
                    printf("ERROR - Could not allocate memory.\n");
                    exit(0);
                }
                // Copy the codex replacement into the new node.
                strcpy(new_node->word, codex_current->word2);

                // Insert the new node to the list.
                new_node->next = list_current->next;
                list_previous->next = new_node;
                list_current->next = NULL;
                // Reset the head if this is the first node.
                if (list_current == (*list_head))
                {
                    (*list_head) = new_node;
                }

                // If the last character is punctuation or a new line, need to add it on to the replacement string so that the output will be formatted correctly.
                if (list_current->word[strlen(list_current->word)-1] == '\n' || ispunct(list_current->word[strlen(list_current->word)-1]))
                {
                    // Determine the number of extra characters to add so the new string will be correctly sized.
                    int extra_char = 1;
                    if (ispunct(list_current->word[strlen(list_current->word)-2]))
                    {
                        extra_char = 2;
                    }

                    // Store a copy of the address of the original word.
                    char *unrevised_word = new_node->word;
                    // Must create a new word to avoid buffer overflow with strcpy.
                    new_node->word = (char *)malloc(sizeof(new_node->word)+extra_char);
                    if (new_node->word == NULL)
                    {
                        printf("ERROR - Could not allocate memory.\n");
                        exit(0);
                    }
                    // Copy in the original string to the new, larger word.
                    strcpy(new_node->word, unrevised_word);
                    // Add the remaining characters to the revised string. (The address of last or second to last character of list_current->word returns the whole rest of the string, so this strcat will append both the punctuation and newline characters if both are in the original string.)
                    strcat(new_node->word, &(list_current->word[strlen(list_current->word)-extra_char]));

                    free(unrevised_word);
                    unrevised_word = NULL;
                }

                free(list_current->word);
                free(list_current);
                list_current = new_node;
                list_previous = new_node;
                // Break so that we don't keep searching through the codex if a word has been replaced.
                break;
            }
            // If the word is in the codex but needs to be deleted:
            else if (strstr(list_current->word, codex_current->word1) != NULL && strcmp(codex_current->word2, "skip") == 0)
            {
                list_previous->next = list_current->next;
                free(list_current->word);
                free(list_current);
                list_current = list_previous->next;
                break;
            }

            // If the word didn't match the codex, keep searching the codex.
            codex_current = codex_current->next;
        }

        // Move on to the next word in the list.
        list_previous = list_current;
        list_current = list_current->next;
    }

    return;
}

void display(struct node *list_head)
{
    struct node *current = NULL;
    current = list_head;

    while (current)
    {
        // If the string has a new line, just print it.
        // (strchr checks if the character is in the string.)
        if (strchr(current->word, '\n') != NULL)
        {
            printf("%s", current->word);
        }
        // If the string doesn't have a new line, print a space after it.
        else
        {
            printf("%s ", current->word);
        }
        current = current->next ;
    }
    // Current is null once the while loop is finished.

    return;
}

void free_list(struct node *(*list_head))
{
    // Start at the head.
    struct node *current = (*list_head);

    while ((*list_head))
    {
        // Move the head to the next element in the list.
        (*list_head) = current->next;
        current->next = NULL;
        // Free the word in the list that current points to.
        free(current->word);
        // Free the current element.
        free(current);
        // Move current to point at the new head.
        current = (*list_head);
    }

    return;
}

void free_codex(struct codex *(*codex_head))
{
    // Start at the head.
    struct codex *current = (*codex_head);

    while ((*codex_head))
    {
        // Move the head to the next element in the list.
        (*codex_head) = current->next;
        current->next = NULL;
        // Free the words in the codex that current points to.
        free(current->word1);
        free(current->word2);
        // Free the current element.
        free(current);
        // Move current to point at the new head.
        current = (*codex_head);
    }

    return;
}

int main()
{
    struct node *list_head;
    struct codex *codex_head;
    list_head = NULL;
    codex_head = NULL;

    load_poem(&list_head);
    load_codex(&codex_head);

    translate(&list_head, codex_head);

    display(list_head);

    free_list(&list_head);
    free_codex(&codex_head);

    return 0;
}
