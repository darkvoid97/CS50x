#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max number of candidates
#define MAX 9

// Candidates have name and vote count
typedef struct
{
    string name;
    int votes;
} candidate;

// Array of candidates
candidate candidates[MAX];

// Number of candidates
int candidate_count;

// Function prototypes
bool vote(string name);
void print_winner(void);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: plurality [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i].name = argv[i + 1];
        candidates[i].votes = 0;
    }

    int voter_count = get_int("Number of voters: ");

    // Loop over all voters
    for (int i = 0; i < voter_count; i++)
    {
        string name = get_string("Vote: ");

        // Check for invalid vote
        if (!vote(name))
        {
            printf("Invalid vote.\n");
        }
    }

    // Display winner of election
    print_winner();
}

// Update vote totals given a new vote
bool vote(string name)
{
    //Check each candidate from the array
    for(int i = 0; i < candidate_count; i++)
    {
        //Compare the vote to the canditate's name
        if (strcmp(candidates[i].name, name) == 0)
        {
            //If positive, add a vote to the candidate
            candidates[i].votes++;
            return true;
        }
    }
    return false;
}

// Print the winner (or winners) of the election
void print_winner(void)
{
    //Create a variable to store the bigger value of votes between the candidates
    int winner_votes = 0;

    //Check the votes of each candidate in order to find the biggest value of votes
    for (int i = 0; i < candidate_count; i++)
    {
         if (candidates[i].votes > winner_votes)
            winner_votes = candidates[i].votes;
    }

    //Now check for the candidate (or candidates) that have the same amount of votes as the max value found before
    for (int i = 0; i < candidate_count; i++)
    {
        if (candidates[i].votes == winner_votes)
            printf("%s\n", candidates[i].name);
    }
    return;
}
