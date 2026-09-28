// Check that a password has at least one lowercase letter, uppercase letter, number and symbol
// Practice iterating through a string
// Practice using the ctype library

#include <cs50.h>
#include <stdio.h>
#include <ctype.h>

bool valid(string password);

int main(void)
{
    string password = get_string("Enter your password: ");
    if (valid(password))
    {
        printf("Your password is valid!\n");
    }
    else
    {
        printf("Your password needs at least one uppercase letter, lowercase letter, number and symbol\n");
    }
}

bool valid(string password)
{
    bool upper, lower, number, symbol = false;
    for(int i=0; password[i]!='\0'; i++)
    {
        if ((!upper) && (isupper(password[i])))
            upper = true;

        if ((!lower) && (islower(password[i])))
            lower = true;

        if ((!number) && (isdigit(password[i])))
            number = true;

        if ((!symbol) && (ispunct(password[i])))
            symbol = true;

        if (upper && lower && number && symbol)
            return true;
    }

    return false;
}
