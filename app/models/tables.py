from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(500))
    email = db.Column(db.String(100))

    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_active(self):
        return True
    
    @property
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.id)

    def __init__(self, username, password, name, email):
        self.username = username
        self.password = password
        self.name = name
        self.email = email

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self): #repr = representative -> como vai ser representado
        #vai devolver User e o usuário escolhido 
        #Exemplo: <User fer123>
        return "<User %r>" % self.username
        #return "<User %r>" % self.username
    
class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) #em comum com a tabela users

    user = db.relationship('User', backref=db.backref('posts', lazy='dynamic'))

    def __init__(self, id, content, user_id):
        self.content = content
        self.user_id = user_id

    def __repr__(self):
        return f"<Post {self.id}>"
       #return "<Post %r>" %self.id
    
class Follow(db.Model):
    __tablename__ = "followers"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), )
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User', foreign_keys=user_id, backref=db.backref('followers_received', lazy='dynamic'))
    follower = db.relationship('User', foreign_keys=follower_id, backref=db.backref('following', lazy='dynamic'))

    def __init__(self, user_id, follower_id):
        self.user_id = user_id
        self.follower_id = follower_id

    def __repr__(self):
        return f"<Follower {self.follower_id} follows {self.user_id}>"