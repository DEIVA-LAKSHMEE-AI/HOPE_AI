#1
SHOW TABLES;
SELECT * FROM Users;
SELECT * FROM Movies;
SELECT * FROM WatchHistory;
SELECT * FROM Reviews;


#2
SELECT title, genre, rating
FROM Movies
WHERE genre = 'Drama'
AND rating > 8.5;

#3
SELECT AVG(rating) AS average_rating
FROM Movies
WHERE release_year > 2015;

#4
SELECT
    U.name,
    W.completion_percentage
FROM Users U
JOIN WatchHistory W
ON U.user_id = W.user_id
JOIN Movies M
ON W.movie_id = M.movie_id
WHERE M.title = 'Stranger Things';


#5
SELECT
    U.name
FROM Users U
JOIN Reviews R
ON U.user_id = R.user_id
WHERE R.rating = (
    SELECT MAX(rating)
    FROM Reviews
);

#6
SELECT
    U.name,
    COUNT(W.watch_id) AS movies_watched
FROM Users U
JOIN WatchHistory W
ON U.user_id = W.user_id
GROUP BY U.user_id, U.name
ORDER BY movies_watched DESC;

#7
SELECT
    M.title,
    M.genre,
    M.rating,
    W.completion_percentage
FROM Movies M
JOIN WatchHistory W
ON M.movie_id = W.movie_id
JOIN Users U
ON W.user_id = U.user_id
WHERE U.name = 'John Doe';

#8
UPDATE Movies
SET rating = 8.9
WHERE title = 'Stranger Things';
SELECT * FROM Movies;

#9
DELETE FROM Reviews
WHERE movie_id IN (
    SELECT movie_id
    FROM Movies
    WHERE rating < 4.0
);

SELECT * FROM Reviews;

#10
SELECT
    U.name,
    M.title,
    R.review_text
FROM Users U
JOIN Reviews R
ON U.user_id = R.user_id
JOIN Movies M
ON R.movie_id = M.movie_id
LEFT JOIN WatchHistory W
ON U.user_id = W.user_id
AND M.movie_id = W.movie_id
WHERE W.completion_percentage IS NULL
OR W.completion_percentage < 100;


#11
SELECT
    M.title,
    M.genre,
    W.completion_percentage
FROM Movies M
JOIN WatchHistory W
ON M.movie_id = W.movie_id
JOIN Users U
ON W.user_id = U.user_id
WHERE U.name = 'John Doe';


#12
SELECT
    U.name,
    R.review_text,
    R.rating
FROM Users U
JOIN Reviews R
ON U.user_id = R.user_id
JOIN Movies M
ON R.movie_id = M.movie_id
WHERE M.title = 'Stranger Things';

#13
SELECT
    U.name,
    U.email,
    M.title,
    M.genre,
    W.watched_date,
    W.completion_percentage
FROM Users U
JOIN WatchHistory W
ON U.user_id = W.user_id
JOIN Movies M
ON W.movie_id = M.movie_id;

#14
SELECT
    M.title,
    COUNT(R.review_id) AS total_reviews,
    AVG(R.rating) AS average_rating
FROM Movies M
JOIN Reviews R
ON M.movie_id = R.movie_id
GROUP BY M.movie_id, M.title
HAVING COUNT(R.review_id) >= 2;


#8
SELECT * FROM Movies;

UPDATE Movies
SET rating = 8.9
WHERE movie_id = 1;
