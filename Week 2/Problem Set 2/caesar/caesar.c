#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main(int argc, string argv[])
{
    // Make sure program was run with just one command-line argument
    // Make sure every character in argv[1] is a digit
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    for(int i = 0; i < strlen(argv[1]); i++)
    {
        if (isdigit(argv[1][i]) == false)
        {
            printf("Usage: ./caesar key\n");
            return 1;
        }
    }

    // Convert argv[1] from a `string` to an `int`
    int key = atoi(argv[1]);

    // Prompt user for plaintext
    string plain = get_string("plaintext: ");

    printf("ciphertext: ");
    // For each character in the plaintext:
    for (int c = 0; c < strlen(plain); c++)
    {
        if (plain[c] >= 'a' && plain[c] <= 'z')
        {
            printf("%c", ((((plain[c] - 'a') + key) % 26) + 'a'));
        }

        else if (plain[c] >= 'A' && plain[c] <= 'Z')
        {
            printf("%c", ((((plain[c] - 'A') + key) % 26) + 'A'));
        }

        else
        {
            printf("%c", plain[c]);
        }
    }
    printf("\n");

    return 0;
}
