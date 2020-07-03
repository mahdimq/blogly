from unittest import TestCase

from app import app
from models import db, User, Post, Tag

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
    """Tests for all routes."""

    def setUp(self):
        """Add sample user."""
        Tag.query.delete()
        Post.query.delete()

        user = User(firstname="TestFname", lastname="TestLname",
                    image_url="https://tinyurl.com/y7akjlzy")
        post = Post(title="TestTitle", content="LoremIpsum", user_id=1)
        tag = Tag(name="TagName")

        db.session.add_all([user, post, tag])
        db.session.commit()

        self.post_id = post.id
        self.user_id = user.id
        self.tag_id = tag.id

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
        """Show adding user post route"""
        with app.test_client() as client:
            user_data = {"firstname": "TestFname", "lastname": "TestLname",
                         "image": "https://tinyurl.com/y7akjlzy"}
            response = client.post(
                "/users/new", data=user_data, follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn(
                '<h3 class="profile-name">TestFname TestLname</h3>', html)

# ==================== POST ROUTES ==================== #

    def test_list_posts(self):
        """Check posts list"""
        with app.test_client() as client:
            response = client.get(f"/posts/{self.post_id}")
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<p class="tag-title">Tags: </p>', html)
            self.assertIn('<p class="text">LoremIpsum</p>', html)

    def test_show_post(self):
        """Test posts details route"""
        with app.test_client() as client:
            response = client.get(f"/posts/{self.post_id}")
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<h1>TestTitle</h1>', html)
            self.assertIn('<p class="text">LoremIpsum</p>', html)

    def test_add_post(self):
        """Show adding Post post route"""
        with app.test_client() as client:
            post_data = {"title": "TestTitle",
                         "content": "Jibberish", "user_id": 1}
            response = client.post(
                f"/users/1/posts/new", data=post_data, follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<h3 class="list-title">Posts</h4>', html)
            self.assertIn('<div class="profile-sidebar">', html)

# ==================== TAG ROUTES ==================== #

    def test_list_tags(self):
        """Check Route to list all tags"""
        with app.test_client() as client:
            response = client.get("/tags")
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn(
                f'<li><a href="/tags/{self.tag_id}">TagName</a></li>', html)
            self.assertIn('<h3>TAG LIST PAGE</h3>', html)
            self.assertIn('<h1>Tags</h1>', html)

    def test_add_tag(self):
        """Show adding tag post route"""
        with app.test_client() as client:
            tag_data = {"name": "TestTagName"}
            response = client.post(
                f"/tags/new", data=tag_data, follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<h3>TAG LIST PAGE</h3>', html)
            self.assertIn(
                f'<li><a href="/tags/{self.tag_id}">TagName</a></li>', html)

    def test_edit_tag(self):
        """Check post route to edit tags and follow redirects"""
        with app.test_client() as client:
            tag_data = {"name": "TestTagName"}
            response = client.post(
                f"/tags/{self.tag_id}/edit", data=tag_data, follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<h1>Tags</h1>', html)
            self.assertNotIn(b"jibberish", response.data)
            self.assertIn(
                '<a class="pure-button" href="/tags/new">Add Tag</a>', html)

    def test_tags_redirect(self):
        """Test redirect route and status code of 302"""
        with app.test_client() as client:
            # find out why get method and not post
            response = client.get(f"/tags/{self.tag_id}/delete")

            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.location, 'http://localhost/tags')
            self.assertNotIn(b"jibberish", response.data)
