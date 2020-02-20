from flaskr.recommender import recommender
from flask_sqlalchemy import SQLAlchemy
from flaskr.model import db, Rating
from flaskr.batch_utils import add_batch

print("RUNNING SCHEDULED")

rec = recommender.Recommender()
articles = rec.get_recommendations()
add_batch(articles)

print("COMPLETED SCHEDULED")
