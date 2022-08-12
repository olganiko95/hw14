from flask import Flask, jsonify

import database_request
from database_request import *

app = Flask(__name__)

children = ['G']
family = ['G', 'PG', 'PG-13']
adult = ['R', 'NC-17']

@app.get('/movie/<title>/')
def search_by_title_page(title):

    result = search_film_by_title(title)
    return jsonify(result)

@app.get('/movie/<first_year>/<second_year>/')
def search_film_year_by_year(first_year, second_year):
    return jsonify(database_request.search_film_year_by_year(first_year=first_year, second_year=second_year))

@app.route('/rating/<children>/')
def page_children_films(children):
    return jsonify(database_request.search_by_rating(ratings=children))

@app.route('/rating/<family>/')
def page_family_films(family):
    return jsonify(database_request.search_by_rating(ratings=family))

@app.route('/rating/<adult>/')
def page_adult_films(adult):
    return jsonify(database_request.search_by_rating(ratings=adult))

@app.route('/genre/<genre>/')
def page_search_film_by_genre(genre):
    return jsonify(database_request.search_film_by_genre(genre=genre))



if __name__ == '__main__':
    app.run(host='127.0.0.2', port=80)


