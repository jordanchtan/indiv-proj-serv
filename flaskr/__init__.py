import os

from flask import Flask
from flask import jsonify
from flask import request


import requests
import sys
from . import recommender
from . import dto
# from . import indiv_models
import json

# set FLASK_APP=flaskr
# set FLASK_ENV=development
# flask run
# pipreqs
# https://download.pytorch.org/whl/cpu/torch-1.4.0%2Bcpu-cp36-cp36m-linux_x86_64.whl
# gunicorn==20.0.4


def create_app(test_config=None):
    # create and configure the app
    from . import db

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    db.init_app(app)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    rec = recommender.Recommender()
    # a simple page that says hello
    @app.route('/news-items', methods=['GET'])
    def get_news_items():
        recs = rec.get_recommendations()

        response = jsonify(recs)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    @app.route('/ratings', methods=['OPTIONS', 'POST', 'GET'])
    def add_rating():
        # db.query_db

        if request.method == 'OPTIONS':
            data = request.json
            response = jsonify(data)
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add(
                'Access-Control-Allow-Headers', 'Authorization, Content-Type')
            response.headers.add('Access-Control-Allow-Methods', '*')
            return response
        elif request.method == 'POST':
            ratingVal = request.json['ratingVal']
            query = 'INSERT INTO rating (userID, ratingVal) VALUES(0, ?)'
            db.query_db(query, [ratingVal], one=True)
            # print(request)
            # print(request.json)

            data = request.json
            response = jsonify(data)
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add(
                'Access-Control-Allow-Headers', 'Authorization, Content-Type')
            response.headers.add('Access-Control-Allow-Methods', '*')

            return response
        elif request.method == 'GET':
            data = []
            for rating in db.query_db('SELECT * FROM rating'):
                r = dto.Rating(rating['ratingID'],
                               rating['userID'], rating['ratingVal'])
                data.append(r.__dict__)
                # print(rating)
                # print(rating.json)
                # print("yo")
            response = jsonify(data)
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add(
                'Access-Control-Allow-Headers', 'Authorization, Content-Type')
            response.headers.add('Access-Control-Allow-Methods', '*')

            return response

            # data = request.json
            # response = jsonify(data)
            # response.headers.add('Access-Control-Allow-Origin', '*')
            # response.headers.add('Access-Control-Allow-Headers', 'Authorization, Content-Type')
            # response.headers.add('Access-Control-Allow-Methods', '*')


# news_resp = requests.get(url)
#         news_resp_dict = news_resp.json()
#         articles = news_resp_dict['articles']
#         response = jsonify(articles)
#         response.headers.add('Access-Control-Allow-Origin', 'http://localhost:4200')
#         return response

    return app
