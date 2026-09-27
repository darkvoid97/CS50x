// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <math.h>

#include "dictionary.h"

// To count words in the load function, and to return the value when the size function is called. Made global so they both can access the variable
unsigned int n_words = 0;

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// Choose number of buckets in hash table
const unsigned int N = 26000;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // Check into the linked list to search for a matching word
    // Hash the word so that it can search it into the linked list
    int index = hash(word);

    // Cursor to search into the linked list, inspired by c++ I guess
    node *cursor = table[index];

    // Iterate the search until you get a NULL node
    while (cursor != NULL)
    {
        // strcasecmp checks two strings byte-by-byte ignoring the case, outputting 0 if the two strings are equal
        if(strcasecmp(word, cursor->word) == 0)
            return true;

        // If not equal, set the cursor to the next node in the linked list
        cursor = cursor->next;
    }
    // Return false if no equal string found after the cursor reached the NULL node
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // Improve this hash function
    // Check each char of the string, first half of the string square the uppercase ASCII number, sum them and mod N to keep it in N range
    // Second half of the string, do it differently
    unsigned int roll = 0;
    unsigned int square = 0;
    for (int i = 0; i < strlen(word); i++)
    {
        square = pow(toupper(word[i]), 2);
        if (i == round(strlen(word) / 2))
        {
            roll = roll + round(sqrt(roll)) + 17;
        }
        roll = square + roll + 47;
    }
    return roll % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // Open the dictionary file
    FILE *source = fopen(dictionary, "r");
    if (source == NULL)
    {
        printf("Dictionary file not found\n");
        return false;
    }

    // Read each word in the file
    char buffer[LENGTH + 1];
    int hash_index = 0;
    while (fscanf(source, "%s", buffer) != EOF)
    {
        // Create a new node
        node *n = malloc(sizeof(node));
        if (n == NULL)
            return false;

        // Insert the current word in the node, and set the next node to NULL
        strcpy(n->word, buffer);
        n->next = NULL;

        // Get the hash of current word
        hash_index = hash(buffer);

        // Add each word to the hash table
        // If there are already entries, insert in the linked list
        if (table[hash_index] != NULL)
            n->next = table[hash_index];

        table[hash_index] = n;

        n_words++;
    }

    // Close the dictionary file
    fclose(source);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // Return counted words in the load function
    return n_words;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // Loop through the indexes
    for (int i = 0; i < N; i++)
    {
        // Use the linked list properties to free each node while setting index to the next node
        node *to_free = table[i];
        node *cursor = table[i];
        while (to_free != NULL)
        {
            cursor = cursor->next;
            free(to_free);
            to_free = cursor;
        }
    }
    return true;
}
