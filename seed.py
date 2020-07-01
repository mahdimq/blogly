from models import User, Post, db
import datetime
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

# =========== PART TWO ============ #

# Add Posts
p1 = Post(title="Lets Code",
          content="Lorem, ipsum dolor sit amet consectetur adipisicing elit. In iste maxime dolorem natus iusto eveniet!", user_id=2)
p2 = Post(title="Lets Play",
          content="Lorem, ipsum dolor sit amet consectetur adipisicing elit. In iste maxime dolorem natus iusto eveniet!", user_id=1)
p3 = Post(title="Sleep Time",
          content="Lorem, ipsum dolor sit amet consectetur adipisicing elit. In iste maxime dolorem natus iusto eveniet!", user_id=3)
p4 = Post(title="I'm Hungry",
          content="Lorem, ipsum dolor sit amet consectetur adipisicing elit. In iste maxime dolorem natus iusto eveniet!", user_id=2)
p5 = Post(title="Soccer",
          content="Lorem, ipsum dolor sit amet consectetur adipisicing elit. In iste maxime dolorem natus iusto eveniet!", user_id=4)
p6 = Post(title="Terminator",
          content="Lorem, ipsum dolor sit amet consectetur adipisicing elit. In iste maxime dolorem natus iusto eveniet!", user_id=4)

# Add new objects to session and commit, so they'll persist
db.session.add_all([john, tommy, queen, jane, james])
# Commit - Otherwise, this never gets saved
db.session.commit()
# Add new objects to session and commit, so they'll persist
db.session.add_all([p1, p2, p3, p4, p5, p6])
# Commit - Otherwise, this never gets saved
db.session.commit()
