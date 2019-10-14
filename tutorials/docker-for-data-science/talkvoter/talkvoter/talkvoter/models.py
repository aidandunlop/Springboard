from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship
from flask_login import UserMixin


db = SQLAlchemy()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __str__(self):
        return str(self.username)


class Talk(db.Model):
    __tablename__ = 'talk'

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String)
    description = db.Column(db.String)
    presenters = db.Column(db.String)

    talk_dt = db.Column(db.DateTime)
    year = db.Column(db.Integer)
    location = db.Column(db.String)

    date_created = db.Column(
        db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return '<Talk {}>'.format(self.id)


class Vote(db.Model):
    __tablename__ = 'vote'

    id = db.Column(db.Integer, primary_key=True)
    talk_id = db.Column(db.Integer, db.ForeignKey('talk.id'))
    talk = relationship("Talk", backref="votes")
    value = db.Column(db.Integer)  # 0=watch_later; 1=in_person
    processed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='votes')

    date_created = db.Column(
        db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return '<Vote %r>' % self.id
