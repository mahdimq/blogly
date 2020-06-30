from unittest import TestCase

from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class BloglyRoutesTestCase(TestCase):
    """Tests for routes for Users."""

    def setUp(self):
        """Add sample user."""

        User.query.delete()

        user = User(firstname="TestFname", lastname="TestLname",
                    image_url="https://tinyurl.com/y7akjlzy")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_list_users(self):
        """Check root route"""
        with app.test_client() as client:
            response = client.get("/users")
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('TestFname', html)

    def test_show_user(self):
        """Test show user details route"""
        with app.test_client() as client:
            response = client.get(f"/users/{self.user_id}")
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn(
                '<h3 class="profile-name">TestFname TestLname</h3>', html)

    def test_add_user(self):
        """Show adding user route"""
        with app.test_client() as client:
            user_data = {"firstname": "TestFname", "lastname": "TestLname",
                         "image": "https://tinyurl.com/y7akjlzy"}
            response = client.post(
                "/users/new", data=user_data, follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn(
                '<h3 class="profile-name">TestFname TestLname</h3>', html)
