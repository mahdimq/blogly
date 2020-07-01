"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
import datetime


db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    """Create a schema table for users"""
    __tablename__ = 'users'

    def __repr__(self):
        u = self
        return f"<User id={u.id} firstname={u.firstname} lastname={u.lastname} image_url={u.image_url}>"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String, default="https://tinyurl.com/y7akjlzy")

    posts = db.relationship('Post', backref='users',
                            lazy=True, cascade="all, delete-orphan")

    def get_fullname(self):
        name = f'{self.firstname} {self.lastname}'
        return name

# =========== PART TWO ============ #


class Post(db.Model):
    """Create a schema table for user posts"""
    __tablename__ = "posts"

    def __repr__(self):
        p = self
        return f"<Post id={p.id} title={p.title} content={p.content} created_at={p.created_at}"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # users = db.relationship('User', backref='posts', lazy=True)

    def friendly_date(self):
        """Create friendly date"""
        date = self.created_at.strftime("%a %b %d %Y,  %-I:%-M %p")
        return date
