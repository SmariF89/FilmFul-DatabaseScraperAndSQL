-- Returns names of all actors with acting credits in over two films.
SELECT a.name
FROM actor a
JOIN action ac ON a.id = ac.actor_id
JOIN movie m ON m.id = ac.movie_id
GROUP BY a.name
HAVING (COUNT(m.title) > 2);

-- Returns all films starring Ethan Hawke.
SELECT m.title
FROM actor a
JOIN action ac ON a.id = ac.actor_id
JOIN movie m ON m.id = ac.movie_id
WHERE a.name = 'Ethan Hawke';