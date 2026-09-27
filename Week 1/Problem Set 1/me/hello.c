#include <stdio.h>
#include <cs50.h>

int main(void)
{
    string name = get_string("Yo, gimme yo' name, yo!\n");
    printf("hello, %s\n", name);
    return 0;
}
