import sqlite3

#функция подключения к базе
def get_data_by_db(query):
    with sqlite3.connect("netflix.db") as connection:
        cur = connection.cursor()
        cur.execute(query)
        result = cur.fetchall()
        return result

#функция форматирования
def formated(films):
    result = []
    i = 0
    for _ in films:
        film = {
                'title': films[i][0],
                'release_year': films[i][1],
                'description': films[i][2]
                }
        i+=1
        result.append(film)
    return(result)

#функция поиска по названию
def search_film_by_title(film_title):
    query_title = f"""
                    SELECT title, country, release_year, listed_in, description  FROM netflix
                    WHERE `title` LIKE '%{film_title}%'
                    ORDER BY release_year DESC LIMIT 1
                    """

    result = get_data_by_db(query_title)
    film = {
        'title': result[0][0],
        'country': result[0][1],
        'release_year': result[0][2],
        'genre': result[0][3],
         'description': result[0][4]
    }

    return film

#функция поиска в промежутке между годами
def search_film_year_by_year(first_year, second_year):

    query_years = f"""
                    SELECT title, release_year  FROM netflix
                    WHERE release_year BETWEEN {first_year} AND {second_year}
                    ORDER BY release_year LIMIT 100
                    """
    films = get_data_by_db(query_years)
    result = []
    i = 0
    for _ in films:
        film = {
        'title': films[i][0],
        'release_year': films[i][1],
        }
        i+=1
        result.append(film)

    return result

#функция поиска по рейтингу
def search_by_rating(ratings):
    query_rating = f"""
                    SELECT title, release_year, description  FROM netflix
                    WHERE rating IN ('{(", ").join(ratings)}')
                    ORDER BY release_year LIMIT 100
                    """
    films = get_data_by_db(query_rating)
    result = formated(films)
    return result

#функция поиска по жанру
def search_film_by_genre(genre):
    genre_query = f"""
			SELECT title, release_year, description FROM netflix
			WHERE listed_in LIKE '%{genre}%'
			ORDER BY release_year DESC LIMIT 10
			"""
    films = get_data_by_db(genre_query)
    result = formated(films)
    return result

#функция поиска по актерам, игравшим вместе
def search_cast_by_actors(first_actor, second_actor):
    actors_query = f"""
			SELECT 'cast' FROM netflix
			WHERE 'cast' LIKE '%{first_actor}%'
			AND 'cast' LIKE '%{second_actor}%'
			ORDER BY release_year DESC
			"""
    films = get_data_by_db(actors_query)
    actors_all = []
    for film in films:
        actors = film[0].split(', ')
        actors_all.extend(actors)
    actors_seen_twice = {actor for actor in actors_all if actors_all.count(actor)>2} - {first_actor, second_actor}
    return actors_seen_twice

#функция расширенного поиска
def search_film_extended(type, release_year, genre):
    extended_query = f"""
			SELECT title, release_year, description FROM netflix
			WHERE type LIKE '{type}' AND release_year = {release_year} 
			AND listed_in LIKE '%{genre}%'
			ORDER BY release_year DESC
			"""
    films = get_data_by_db(extended_query)
    result = formated(films)
    return result
