-- Use this to check all the students with the House names and House head assigned to them in one table

select students.id, students.student_name, houses.house_name, houses.head_name
from students
join assignments on students.id = assignments.student_id
join houses on houses.id = assignments.house_id;
