#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int n = 0;
    do
    {
        n = get_int("Input a number between 1 and 8, inclusive, to build the Mario pyramid:\n");
    }
    while ((n<1) || (n>8));
    for (int i=0; i<n; i++)
    {
        for (int j=0; j<n-i-1; j++)
            printf(" ");

        for (int k=0; k<=i; k++)
            printf("#");

        printf("  ");

        for (int x=0; x<=i; x++)
            printf("#");

        printf("\n");
    }
    return 0;
}
