from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    db.app = app
    db.init_app(app)
    

class User(db.Model):
    """ User model for app """
    
    __tablename__ = "users"
    
    username = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    posts = db.relationship("Feedback")
    
    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """ Register a user with hashed password, returns user """

        hashed_password = bcrypt.generate_password_hash(password) # currently a bytestring
        hashed_utf8 = hashed_password.decode("utf8") # converts bytestring to unicode string
        
        return cls(username=username, password=hashed_utf8, email=email, first_name=first_name, last_name=last_name)
        
        
    @classmethod
    def authenticate(cls, username, password):
        """ Validates that user exists and password is correct """
        
        user = User.query.get(username)
        
        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False
        
    
class Feedback(db.Model):
    """ Feedback model """
    
    __tablename__ = "feedback"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String, nullable=False)
    username = db.Column(db.String, db.ForeignKey("users.username"))