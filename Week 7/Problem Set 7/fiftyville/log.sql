-- Keep a log of any SQL queries you execute as you solve the mystery.
-- Checking crime scene reports from the specified day
select id, description from crime_scene_reports where year = 2024 and month = 7 and day = 28 and street = "Humphrey Street";
-- Crime scene ID 295 mentions three witnesses and all their interviews transcripts mentioning the bakery. Theft took place at 10:15am
select id, transcript from interviews where year = 2024 and month = 7 and day = 28 and transcript like "%bakery%";
-- Interview ID 161 mentions within 10 minutes of 10:15am, the thief got into a car in the bakery parking lot
-- Interview ID 162 mentions the thief being by the ATM on Leggett Street earlier in that morning, and withdrawing some money
-- Interview ID 163 mentions the thief calling someone while leaving the bakery, as they wanted to take the earliest flight out of Fiftyville the next day

-- Checking the bakery security logs for parking activity in the same day, within 10 minutes of 10:15a, meaning <= 10:25am
select id, activity, license_plate, hour, minute from bakery_security_logs where year = 2024 and month = 7 and day = 28 and hour = 10 and minute <= 25;
-- Several cars exited the parking lot within those 10 minutes. Not sure how to exclude some of them.

-- Checking the Leggett Street ATM withdraw transactions of the same day
select id, account_number, transaction_type, amount from atm_transactions where atm_location = "Leggett Street" and year = 2024 and month = 7 and day = 28 and transaction_type = "withdraw";
-- Several withdraw transactions happened that day

-- Checking the phone calls that happened in that day
select id, caller, receiver, duration from phone_calls where year = 2024 and month = 7 and day = 28;
-- Several phone calls happened

-- Checking for the flights that departed shortly after the theft happened
SELECT flights.*, airports.city FROM flights JOIN airports ON flights.destination_airport_id = airports.id WHERE (year = 2024 AND month = 7 AND day > 28) ORDER BY year, month, day, hour, minute;
-- Earliest flight after July 28 2024 is to New York City, July 29 2024 at 8:20am, flight ID is 36

-- Cross referencing the people's licence plates and the other info with the ones who did activity at the bakery parking
SELECT name, phone_number, passport_number, people.license_plate, hour, minute FROM people JOIN bakery_security_logs ON people.license_plate = bakery_security_logs.license_plate WHERE day = 28 AND month = 7 AND year = 2024 AND hour = 10 AND minute >= 15 AND minute < 25 AND activity = 'exit';

-- Cross referencing the people who used the atm with their bank account's info
SELECT name, phone_number, passport_number, people.license_plate FROM people JOIN bank_accounts on people.id = bank_accounts.person_id JOIN atm_transactions on bank_accounts.account_number = atm_transactions.account_number WHERE day = 28 AND year = 2024 AND month = 7 AND atm_transactions.atm_location = 'Leggett Street' AND atm_transactions.transaction_type = 'withdraw';
-- Bruce, Luca, Iman, Diana appear in both the cross references

-- Checking receivers for short phone calls happened in that day
SELECT name, phone_calls.receiver, phone_calls.caller FROM people JOIN phone_calls ON people.phone_number = phone_calls.receiver WHERE day = 28 AND month = 7 AND year = 2024 AND duration < 60;

-- Checking callers for short phone calls happened in that day
SELECT name, phone_calls.caller, phone_calls.receiver FROM people JOIN phone_calls ON people.phone_number = phone_calls.caller WHERE day = 28 AND month = 7 AND year = 2024 AND duration < 60;
-- Bruce and Diana appear in this list

-- Cross referencing receiver and callers from the last two lists
SELECT people.name, phone_calls.receiver, phone_calls.caller, caller.name FROM people JOIN phone_calls ON people.phone_number = phone_calls.receiver JOIN people AS caller on caller.phone_number = phone_calls.caller WHERE day = 28 AND month = 7 AND year = 2024 AND duration < 60;
-- Bruce called Robin and Diana called Philip
-- (Bruce is Batman?)

-- We already found out that the earliest plane the next day has ID 36 and is off to New York City
-- Check for list of passengers who took that flight
SELECT name FROM people JOIN passengers on people.passport_number = passengers.passport_number JOIN flights on passengers.flight_id = flights.id WHERE passengers.flight_id = 36;
-- Bruce appeared on the list, meaning apparently Batman himself is the culprit, and Robin is the accomplice
