from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin

from config import db, bcrypt

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    _password_hash = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(200))
    bio = db.Column(db.String(200))

    recipes = db.relationship('Recipe', backref='user', lazy=True)

    def __init__(self, username, password, image_url=None, bio=None):
        self.username = username
        self.password = password
        self.image_url = image_url
        self.bio = bio

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self._password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self._password_hash, password)

class Recipe(db.Model, SerializerMixin):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    instructions = db.Column(db.String(500), nullable=False)
    minutes_to_complete = db.Column(db.Integer, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, title, instructions, minutes_to_complete, user_id):
        self.title = title
        self.instructions = instructions
        self.minutes_to_complete = minutes_to_complete
        self.user_id = user_id