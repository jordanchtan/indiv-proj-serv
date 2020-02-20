from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

db = SQLAlchemy()


# class User(db.Model):
#     __tablename__ = 'user'
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(120), unique=True, nullable=False)

#     def __repr__(self):
#         return '<User %r>' % self.email

#     def __init__(self, email):
#         self.email = email


class Rating(db.Model):
    __tablename__ = 'rating'
    rating_id = db.Column(db.Integer, primary_key=True)
    ratingVal = db.Column(db.Integer, nullable=False)
    user_email = db.Column(db.String(120), nullable=False)
    article_id = db.Column(db.Integer, db.ForeignKey(
        'article.article_id'), nullable=False)
    article_rel = db.relationship('Article',
                                  backref=db.backref('rating', lazy=True))

    def __repr__(self):
        return '<Rating %r>' % self.rating_id

    # def __init__(self, ratingVal, user_email, article_id):
    #     self.ratingVal = ratingVal
    #     self.user_email = user_email
    #     self.article_id = article_id


class Article(db.Model):
    __tablename__ = 'article'
    article_id = db.Column(db.Integer, primary_key=True)
    article_json = db.Column(db.JSON, primary_key=False)
    batch_id = db.Column(db.Integer, db.ForeignKey(
        'batch.batch_id'), nullable=False)
    batch_rel = db.relationship(
        'Batch', backref=db.backref('article', lazy=True))

    def __repr__(self):
        return '<Article %r>' % self.article_id

    # def __init__(self, article_id, article_json, batch_id):
    #     self.article_id = article_id
    #     self.article_json = article_json
    #     self.batch_id = batch_id


class Batch(db.Model):
    __tablename__ = 'batch'
    batch_id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime(timezone=True),
                          server_default=func.now())

    def __repr__(self):
        return '<Batch %r>' % self.batch_id
