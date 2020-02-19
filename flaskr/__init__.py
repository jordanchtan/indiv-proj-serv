import os

from flask import Flask
from flask import jsonify
from flask import request


import requests
import sys
from . import recommender
from . import dto
import json
from . import util
from flask_sqlalchemy import SQLAlchemy
from flask_heroku import Heroku
from flaskr.model import db, Rating, User
import copy


# set FLASK_APP=flaskr
# set FLASK_ENV=development
# flask run
# pipreqs
# https://download.pytorch.org/whl/cpu/torch-1.4.0%2Bcpu-cp36-cp36m-linux_x86_64.whl
# gunicorn==20.0.4
# psycopg2==2.8.4


def create_app(test_config=None):
    # create and configure the app

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_TRACK_MODIFICATIONS=False
        # DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'

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

    heroku = Heroku(app)

    # from flaskr.model import db
    db.init_app(app)

    bucketName = "indivprojcht116"
    remoteDirectoryName = "model"
    util.downloadDirectoryFroms3(bucketName, remoteDirectoryName)

    @app.route('/news-items', methods=['GET'])
    def get_news_items():
        rec = recommender.Recommender()
        recs = rec.get_recommendations()

        response = jsonify(recs)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    @app.route('/ratings', methods=['OPTIONS', 'POST', 'GET'])
    def add_rating():

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
            user_email = request.json['userEmail']
            # query = 'INSERT INTO rating (userID, ratingVal) VALUES(0, ?)'
            # db.query_db(query, [ratingVal], one=True)

            rating = Rating(ratingVal, user_email)
            # data = copy(rating. __dict__)
            # del data["_sa_instance_state"]

            try:
                db.session.add(rating)
                db.session.commit()
            except Exception as e:
                # print("\n FAILED entry: {}\n".format(json.dumps(data)))
                print(e)
                # sys.stdout.flush()

            data = request.json
            response = jsonify(data)
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add(
                'Access-Control-Allow-Headers', 'Authorization, Content-Type')
            response.headers.add('Access-Control-Allow-Methods', '*')

            return response
        elif request.method == 'GET':
            data = []
            # for rating in db.query_db('SELECT * FROM rating'):
            #     r = dto.Rating(rating['ratingID'],
            #                    rating['userID'], rating['ratingVal'])
            #     data.append(r.__dict__)
            for rating in Rating.query.all():
                r = copy.copy(rating. __dict__)
                del r["_sa_instance_state"]
                data.append(r)

            response = jsonify(data)
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add(
                'Access-Control-Allow-Headers', 'Authorization, Content-Type')
            response.headers.add('Access-Control-Allow-Methods', '*')

            return response

    return app
