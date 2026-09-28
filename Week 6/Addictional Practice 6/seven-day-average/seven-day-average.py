import csv
import requests


def main():
    # Read NYTimes Covid Database
    download = requests.get(
        "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv"
    )
    decoded_content = download.content.decode("utf-8")
    file = decoded_content.splitlines()
    reader = csv.DictReader(file)

    # Construct 14 day lists of new cases for each states
    new_cases = calculate(reader)

    # Create a list to store selected states
    states = []
    print("Choose one or more states to view average COVID cases.")
    print("Press enter when done.\n")

    while True:
        state = input("State: ")
        if state in new_cases:
            states.append(state)
        if len(state) == 0:
            break

    print(f"\nSeven-Day Averages")

    # Print out 7-day averages for this week vs last week
    comparative_averages(new_cases, states)


def calculate(reader):
    prev_cases, new_cases = {}, {}

    for day in reader:
        new_cases_day = int(day["cases"])

        try:
            new_cases_day -= prev_cases[day["state"]]

        except KeyError:
            new_cases.update({day["state"]: [new_cases_day]})

        else:
            if len(new_cases[day["state"]]) == 14:
                new_cases[day["state"]].pop(0)

            new_cases[day["state"]].append(new_cases_day)

        prev_cases.update({day["state"]: int(day["cases"])})

    return new_cases


def comparative_averages(new_cases, states):
    for state in states:
        average_current_week = sum(new_cases[state][7:])/7
        average_previous_week = sum(new_cases[state][:7])/7

        difference = average_current_week - average_previous_week

        print(f"{state} had a 7-day average of {round(average_current_week)}", end=" ")

        try:
            percent = difference / average_previous_week
        except ZeroDivisionError:
            raise ZeroDivisionError
        else:
            percent *= 100

        if difference < 0:
            print(f"and a decrease of {abs(percent):.2f}%.")
        else:
            print(f"and an increase of {percent:.2f}%.")


main()
