from flask_sqlalchemy import SQLAlchemy
from flaskr.model import db, Batch, Rating, Article
from sqlalchemy import desc


def add_batch(articles):
    batch = Batch()

    try:
        db.session.add(batch)
        db.session.commit()
    except Exception as e:
        print(e)

    for article in articles:
        a = Article(batch_id=batch.batch_id, article_json=article)
        db.session.add(a)

    db.session.commit()


def get_latest_batch_articles():
    latest_batch = Batch.query.order_by(desc(Batch.batch_id)).first()
    batch_id = latest_batch.batch_id
    articles = Article.query.filter_by(batch_id=batch_id).all()

    return articles
