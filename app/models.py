from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(25), nullable=False)
    last_name = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    username = db.Column(db.String(25), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    reviews = db.relationship('Reviews', backref='author', lazy='dynamic')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.password = self.set_password(kwargs.get('password', ''))
        db.session.add(self)
        db.session.commit()

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def set_password(self, plain_password):
        return generate_password_hash(plain_password)

    def check_password(self, password_guess):
        return check_password_hash(self.password, password_guess)


@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)



class Reviews(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dealership_name = db.Column(db.String(100), nullable=False)
    dealership_address = db.Column(db.String(200), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    msrp = db.Column(db.Integer, nullable=False) 
    markup = db.Column(db.Integer)
    sold = db.Column(db.Integer, nullable=False) 
    comment = db.Column(db.String(300))
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        db.session.add(self)
        db.session.commit()

    def __str__(self):
        return self.dealership_name

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if key in {'dealership_name', 'dealership_address', 'rating', 'msrp', 'markup', 'sold', 'comment'}:
                setattr(self, key, value)
        db.session.commit()
        

    def delete(self):
        db.session.delete(self)
        db.session.commit()