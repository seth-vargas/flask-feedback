from models import db, User, Feedback
from app import app

def seed():
    # Create all tables
    db.drop_all()
    db.create_all()

    # Add users
    u1 = User.register("test1", "password", "test1@gmail.com", "John", "Doe")
    u2 = User.register("test2", "password", "test2@gmail.com", "Jane", "Doe")
    u3 = User.register("test3", "password", "test3@gmail.com", "Robert", "Doe")
    
    db.session.add_all([u1, u2, u3])
    
    p1 = Feedback(title="Johns opinion on onions", content="They are alright", username=u1.username)
    p2 = Feedback(title="Johns opinion on bananas", content="They are bananas", username=u1.username)
    p3 = Feedback(title="Johns opinion on food", content="This is the best thing to exist", username=u1.username)
    p4 = Feedback(title="Janes opinion on food", content="This is the worst thing to exist", username=u2.username)
    
    db.session.add_all([p1, p2, p3, p4])
    db.session.commit()
    
if __name__ == "__main__":
    seed()