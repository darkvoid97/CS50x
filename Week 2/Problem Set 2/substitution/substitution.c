#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main(int argc, string argv[])
{
    //If there isn't just one argument after the command, exit the program
    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }

    //If the input key isn't 26 characters long, exit the program
    int length = strlen(argv[1]);
    if (length != 26)
    {
        printf("Key must contain 26 characters.\n");
        return 1;
    }

    //Check for non-alphabetical characters. If there are, exit the program
    for (int i = 0; i < length; i++)
    {
        if (isalpha(argv[1][i]) == false)
        {
            printf("Key must contain only alphabetical characters.\n");
            return 1;
        }
        /*While I'm checking for non-alphabetical characters, I'll also check if there are two of the same characters in the string.
        This means there couldn't be every alphabetical character since there are 26 of them*/
        for (int j = i + 1; j < length; j++)
        {
            if (tolower(argv[1][i]) == tolower(argv[1][j]))
            {
                printf("Key must contain every alphabetical character exactly once.\n");
                return 1;
            }
        }
    }

    //If the input passes all the checks, the key is valid. Now, to get the plaintext and cipher it
    string key = argv[1];
    string plain = get_string("plaintext: ");
    string alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

    printf("ciphertext: ");

    //I'll be using the alpha string to substitute each character of the plaintext with the character assigned in the key string
    for (int i = 0; i < strlen(plain); i++)
    {
        if (isalpha(plain[i]))
        {
            char c = plain[i];

            for (int x = 0; x < strlen(alpha); x++)
            {
                if (islower(c))
                {
                    if (c == tolower(alpha[x]))
                        printf("%c", tolower(key[x]));
                }
                else
                {
                    if (c == toupper(alpha[x]))
                        printf("%c", toupper(key[x]));
                }
            }
        }
        else
        {
            printf("%c", plain[i]);
        }
    }

    printf("\n");
    return 0;
}
