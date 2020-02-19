from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.email

    def __init__(self, email):
        self.email = email


class Rating(db.Model):
    __tablename__ = 'rating'
    id = db.Column(db.Integer, primary_key=True)
    ratingVal = db.Column(db.Integer, nullable=False)
    user_email = db.Column(db.String(120), nullable=False)
    # user_id = db.Column(db.Integer, db.ForeignKey(
    #     'user.id'), nullable=False)
    # user = db.relationship('User',
    #                        backref=db.backref('rating', lazy=True))

    def __repr__(self):
        return '<Rating %r>' % self.ratingVal

    def __init__(self, ratingVal, user_email):
        self.ratingVal = ratingVal
        self.user_email = user_email
        # self.user_id = user_id
        # self.user = category
