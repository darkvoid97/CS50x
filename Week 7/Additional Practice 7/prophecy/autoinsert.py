from cs50 import SQL
from csv import DictReader

new_db = SQL("sqlite:///new_roster.db")
new_db.execute("DELETE FROM students")
new_db.execute("DELETE FROM houses")
new_db.execute("DELETE FROM assignments")

db = SQL("sqlite:///roster.db")
houses = db.execute("SELECT DISTINCT(house), head FROM students ORDER BY house")

for house in houses:
    new_db.execute("INSERT INTO houses (house_name, head_name) VALUES (?, ?)", house["house"], house["head"])

with open("students.csv") as file:
    for student in DictReader(file):
        new_db.execute("INSERT INTO students (student_name) VALUES (?)", student["student_name"])

        student_id = new_db.execute("SELECT id FROM students WHERE student_name = ?", student["student_name"])[0]["id"]
        house_id = new_db.execute("SELECT id FROM houses WHERE house_name = ?", student["house"])[0]["id"]
        
        new_db.execute("INSERT INTO assignments (student_id, house_id) VALUES (?, ?)", student_id, house_id)
