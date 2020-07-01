"""Blogly application."""
from flask import Flask, render_template, redirect, request, flash
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'abcd1234'

connect_db(app)
# db.create_all()


@app.route('/')
def show_index():
    """renders home page with 5 latest posts"""
    post = Post.query.order_by(Post.created_at.desc()).limit(5)
    return render_template('home.html', post=post)


@app.route("/users")
def list_users():
    """Shows list of all users in the db"""
    users = User.query.all()
    return render_template('list.html', users=users)


@app.route("/users/new", methods=["GET"])
def show_form():
    """Show form for adding new user"""
    return render_template("/form.html")


@app.route("/users/new", methods=["POST"])
def add_user():
    """Add user to the database"""
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    image = request.form['image']
    image = image if image else None

    new_user = User(firstname=firstname,
                    lastname=lastname,
                    image_url=image)

    db.session.add(new_user)
    db.session.commit()

    flash("Created a New User!", "success")
    return redirect(f'/users/{new_user.id}')


@app.route('/users/<int:user_id>')
def show_user(user_id):
    """show details about a single user"""
    user = User.query.get_or_404(user_id)
    return render_template("user.html", user=user)


@ app.route("/users/<int:user_id>/edit")
def show_edit_page(user_id):
    """show user edit page"""
    user = User.query.get_or_404(user_id)
    return render_template("edit.html", user=user)


@ app.route("/users/<int:user_id>/edit", methods=["POST"])
def edit_user(user_id):
    """edit current user"""
    update = User.query.get_or_404(user_id)
    update.firstname = request.form['firstname']
    update.lastname = request.form['lastname']
    update.image = request.form['image']

    db.session.add(update)
    db.session.commit()
    flash(f"Edited User", "success")
    return redirect(f"/users/{user_id}")


@ app.route('/users/<int:user_id>/delete', methods=["GET"])
def delete_user(user_id):
    """delete a single user"""
    del_user = User.query.get_or_404(user_id)
    db.session.delete(del_user)
    db.session.commit()

    flash(f"Deleted {del_user.get_fullname()}", "danger")
    return redirect("/")

# ================ POSTS ROUTE ================== #


@app.route('/users/<int:user_id>/posts/new', methods=['GET'])
def show_post_form(user_id):
    """show form for adding a post"""
    user = User.query.get_or_404(user_id)
    return render_template("add_post.html", user=user)


@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def add_post(user_id):
    """submit a new post for a user"""
    title = request.form['title']
    content = request.form['content']
    new_post = Post(title=title, content=content, user_id=user_id)

    db.session.add(new_post)
    db.session.commit()

    """show flash message when a new post is created"""
    flash("Added a new post!", "success")
    return redirect(f'/users/{user_id}')


@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """show post for information when clicked on title"""
    post = Post.query.get_or_404(post_id)

    return render_template('posts.html', post=post)


@app.route('/posts/<int:post_id>/edit')
def edit_post_form(post_id):
    """show form to edit a post"""
    post = Post.query.get_or_404(post_id)

    return render_template('edit_post.html', post=post)


@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def edit_post(post_id):
    """show form to edit a post and redirect to post"""
    edit_post = Post.query.get_or_404(post_id)

    edit_post.title = request.form['title']
    edit_post.content = request.form['content']
    db.session.add(edit_post)
    db.session.commit()
    """show flash message when post is edited"""
    flash(f"Edited Post", "success")
    return redirect(f"/posts/{post_id}")


@app.route("/posts/<int:post_id>/delete")
def delete_post(post_id):
    """delete specific post and redirect to user page"""
    del_post = Post.query.get_or_404(post_id)
    user = del_post.users.id
    db.session.delete(del_post)
    db.session.commit()
    """show flash message when post is deleted"""
    flash(f"Deleted {del_post.title}", "danger")
    return redirect(f"/users/{user}")
