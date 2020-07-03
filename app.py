"""Blogly application."""
from flask import Flask, render_template, redirect, request, flash
from models import db, connect_db, User, Post, PostTag, Tag

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
    return render_template('/home.html', post=post)


@app.route("/users")
def list_users():
    """Shows list of all users in the db"""
    users = User.query.all()
    return render_template('/users/list.html', users=users)


@app.route("/users/new", methods=["GET"])
def show_form():
    """Show form for adding new user"""
    return render_template("/users/form.html")


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
    return render_template("/users/user.html", user=user)


@ app.route("/users/<int:user_id>/edit")
def show_edit_page(user_id):
    """show user edit page"""
    user = User.query.get_or_404(user_id)
    return render_template("/users/edit.html", user=user)


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


@ app.route('/users/<int:user_id>/delete', methods=["POST"])
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
    tags = Tag.query.all()  # <-- retrieves all tags for that user

    return render_template("/posts/add_post.html", user=user, tags=tags)


@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def add_post(user_id):
    """submit a new post for a user and tags"""
    title = request.form['title']
    content = request.form['content']

    tag_id = [int(num) for num in request.form.getlist(
        "tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_id)).all()

    new_post = Post(title=title, content=content, user_id=user_id, tags=tags)

    db.session.add(new_post)
    db.session.commit()

    """show flash message when a new post is created"""
    flash("Added a new post!", "success")
    return redirect(f'/users/{user_id}')


@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """show post for information when clicked on title"""
    post = Post.query.get_or_404(post_id)
    return render_template('/posts/posts.html', post=post)


@app.route('/posts/<int:post_id>/edit')
def edit_post_form(post_id):
    """show form to edit a post"""
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template('/posts/edit_post.html', post=post, tags=tags)


@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def edit_post(post_id):
    """show form to edit a post and redirect to post"""
    edit_post = Post.query.get_or_404(post_id)

    edit_post.title = request.form['title']
    edit_post.content = request.form['content']

    tag_id = [int(num) for num in request.form.getlist("tags")]
    edit_post.tags = Tag.query.filter(Tag.id.in_(tag_id)).all()

    db.session.add(edit_post)
    db.session.commit()
    """show flash message when post is edited"""
    flash(f"Edited Post", "success")
    return redirect(f"/users/{edit_post.user_id}")


@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    """delete specific post and redirect to user page"""
    del_post = Post.query.get_or_404(post_id)
    db.session.delete(del_post)
    db.session.commit()
    """show flash message when post is deleted"""
    flash(f"Deleted {del_post.title}", "danger")
    return redirect(f"/users/{del_post.user_id}")

# ================ TAGS ROUTE ================== #

@app.route('/tags')
def list_tags():
    """route to list all tags with links to tag details"""
    tags = Tag.query.all()
    return render_template("/tags/tags.html", tags=tags)


@app.route("/tags/new")
def add_tag_form():
    """show form to add a new tag"""
    tags = Tag.query.all()

    return render_template("/tags/add_tag.html", tags=tags)


@app.route("/tags/new", methods=["POST"])
def add_tag():
    """Adds a new tag"""
    post_id = [int(num) for num in request.form.getlist("posts")]
    posts = Post.query.filter(Post.id.in_(post_id)).all()

    name = request.form["name"]
    new_tag = Tag(name=name, posts=posts)

    db.session.add(new_tag)
    db.session.commit()

    """show flash message when a new post is created"""
    flash("Added a new tag!", "success")
    return redirect('/tags')


@app.route("/tags/<int:tag_id>")
def show_tag(tag_id):
    """shows detail about a tag, links to edit and delete"""
    tags = Tag.query.get_or_404(tag_id)
    return render_template('/tags/tag_detail.html', tags=tags)


@app.route("/tags/<int:tag_id>/edit")
def edit_tag_form(tag_id):
    """shows form to edit the tag"""
    tags = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
    return render_template('/tags/edit_tag.html', tags=tags, posts=posts)


@app.route("/tags/<int:tag_id>/edit", methods=["POST"])
def edit_tag(tag_id):
    """edit the tag and redirect to tag list"""
    update_tag = Tag.query.get_or_404(tag_id)
    update_tag.name = request.form["name"]

    post_id = [int(num) for num in request.form.getlist("posts")]
    update_tag.posts = Post.query.filter(Post.id.in_(post_id)).all()

    db.session.add(update_tag)
    db.session.commit()

    """show flash message when a new post is created"""
    flash("Updated tag!", "success")
    return redirect("/tags")


@app.route("/tags/<int:tag_id>/delete", methods=["POST"])
def del_tag(tag_id):
    """deletes a specific tag and redirects to tag list"""

    tags = Tag.query.get_or_404(tag_id)

    db.session.delete(tags)
    db.session.commit()

    """show flash message when a new post is created"""
    flash("Deleted tag!", "danger")
    return redirect("/tags")

# =============== ERROR 404 PAGE ================ #


@app.errorhandler(404)
def page_not_found(error):
    """Show 404 ERROR page if page NOT FOUND"""

    return render_template('error.html'), 404
