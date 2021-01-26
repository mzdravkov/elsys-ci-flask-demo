from datetime import datetime
from itsdangerous import (
        TimedJSONWebSignatureSerializer as Serializer,
        BadSignature,
        SignatureExpired
        )

from tinder import app, db
from tinder.utils import hash_password

likes_table = db.Table('like', db.Model.metadata,
        db.Column('liking_user_id', db.Integer, db.ForeignKey('user.id'), index=True),
        db.Column('liked_user_id', db.Integer, db.ForeignKey('user.id')))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    likes = db.relationship(
            'User',
            secondary=likes_table,
            primaryjoin=id==likes_table.c.liking_user_id,
            secondaryjoin=id==likes_table.c.liked_user_id,
            backref='liked_by'
            )
    description = db.Column(db.String(500), nullable=True)
    picture = db.Column(db.String(48), nullable=True)
    sent_messages = db.relationship('Message',
            foreign_keys='Message.sender_id',
            backref='sender'
            )
    received_messages = db.relationship('Message',
            foreign_keys='Message.receiver_id',
            backref='receiver'
            )

    def __init__(self, **kwargs):
        if 'password' in kwargs:
            kwargs['password'] = hash_password(kwargs['password'])
        super(User, self).__init__(**kwargs)

    def __repr__(self):
        return '<User %r>' % self.username

    def verify_password(self, password):
        return self.password == hash_password(password)

    def generate_token(self):
        s = Serializer(app.secret_key, expires_in=600)
        return s.dumps({'username': self.username})

    @staticmethod
    def find_by_token(token):
        if not token:
            return None

        try:
            s = Serializer(app.secret_key)
            payload = s.loads(token)
            return User.query.filter_by(username=payload.get('username')).first()
        except SignatureExpired:
            return None

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey(User.id))
    receiver_id = db.Column(db.Integer, db.ForeignKey(User.id))
    content = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
