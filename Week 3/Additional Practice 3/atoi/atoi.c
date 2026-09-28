#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

int convert(string input);

int main(void)
{
    string input = get_string("Enter a positive integer: ");

    for (int i = 0, n = strlen(input); i < n; i++)
    {
        if (!isdigit(input[i]))
        {
            printf("Invalid Input!\n");
            return 1;
        }
    }

    // Convert string to int
    printf("%i\n", convert(input));
}

int convert(string input)
{
    int number = 0, length = -1;
    for (int i=0; input[i]!='\0'; i++)
        length++;

    number = input[length] - '0';
    input[length] = '\0';

    if (length == 0)
        return number;

    return number + (10 * convert(input));
}
