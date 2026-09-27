#include <cs50.h>
#include <stdio.h>
#include <math.h>

// Gets credit card number and checks whether it's valid
int main(void)
{
    long number, card;
    do
    {
        number = get_long("Hands up, give me your credit card numbah, right now!\n");
    }
    while (number < 0);

    card = number;

    // Calculate total number of digits
    int count = (card == 0) ? 1  : (log10(card) + 1);

    int sum = 0;

    // Reiterate through each pair of digits. First digit adds to sum, second digit * 2 and add sum of digits.
    while (card != 0)
    {
        int d1 = card % 10;
        sum += d1;
        int d2 = 2 * ((card / 10) % 10);
        int r1 = (d2 % 10) + floor((d2 / 10) % 10);
        sum += r1;
        card /= 100;
    }

    string type;
    // Identify which card type
    int test = number / pow(10, count - 2);
    if ((count == 13 || count == 16) && test / 10 == 4)
    {
        type = "VISA";
    }
    else if (count == 16  && test >= 51 && test <= 55)
    {
        type = "MASTERCARD";
    }
    else if (count == 15 && (test == 34 || test == 37))
    {
        type = "AMEX";
    }
    else
    {
        type = "INVALID";
    }

    // Final verification
    if (sum % 10 == 0)
    {
        printf("%s\n", type);
    }
    else
    {
        printf("INVALID\n");
    }

    return 0;
}
