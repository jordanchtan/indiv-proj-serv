import os

from flask import Flask
from flask import jsonify
from flask import request


import requests
import sys
from . import recommender

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )


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

    # a simple page that says hello
    @app.route('/news-items', methods=['GET'])
    def get_news_items():
        recs = recommender.get_recommendations()
        response = jsonify(recs)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    @app.route('/ratings', methods=['OPTIONS','POST'])
    def add_rating():
        # ratingVal = request.form['ratingVal']
        # if request.method == 'OPTIONS':
        #     return ""
        # elif request.method == 'POST':
        data = request.json
        response = jsonify(data)
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Authorization, Content-Type')
        response.headers.add('Access-Control-Allow-Methods', '*')
    
        return response


# news_resp = requests.get(url)
#         news_resp_dict = news_resp.json()
#         articles = news_resp_dict['articles']
#         response = jsonify(articles)
#         response.headers.add('Access-Control-Allow-Origin', 'http://localhost:4200')
#         return response

    return app