select others.name
from stars
join people as kevin on stars.person_id = kevin.id
join stars as others_stars on stars.movie_id = others_stars.movie_id
join people as others on others_stars.person_id = others.id
where kevin.name = "Kevin Bacon" and kevin.birth = 1958 and others.name != "Kevin Bacon";
