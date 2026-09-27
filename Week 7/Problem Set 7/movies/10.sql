select distinct name
from people
join directors on directors.person_id = people.id
join movies on directors.movie_id = movies.id
join ratings on ratings.movie_id = movies.id
where ratings.rating >= 9.0;
