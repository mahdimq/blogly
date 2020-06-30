from models import User, db
from app import app

# create all tables
db.drop_all()
db.create_all()

# if table isn't empty, empty it
User.query.delete()

# Add Users
john = User(firstname='John', lastname='Conner',
            image_url='https://tinyurl.com/ya27nb56')
tommy = User(firstname='Thomas', lastname='Engine',
             image_url='https://tinyurl.com/ycjaxkap')
queen = User(firstname='Queen', lastname='Elizabeth',
             image_url='https://tinyurl.com/y7de7fbt')
jane = User(firstname='Jane', lastname='Doe')
james = User(firstname='James', lastname='Mallone')

# Add new objects to session, so they'll persist
db.session.add(john)
db.session.add(tommy)
db.session.add(queen)
db.session.add(jane)
db.session.add(james)

# Commit - Otherwise, this never gets saved
db.session.commit()
