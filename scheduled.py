from flaskr import recommender
from flask_sqlalchemy import SQLAlchemy
from flaskr import batch_utils
from flaskr import create_app

print("RUNNING SCHEDULED")
# heroku = Heroku(app)

app = create_app()
app.app_context().push()
rec = recommender.Recommender()
articles = rec.get_recommendations()
batch_utils.add_batch(articles)

print("COMPLETED SCHEDULED")
