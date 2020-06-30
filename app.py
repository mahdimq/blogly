"""Blogly application."""

from flask import Flask, render_template, redirect, request, flash
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'abcd1234'

connect_db(app)
# db.create_all()


@app.route('/')
def show_index():
    """redirects user to list of users in db"""
    return redirect("/users")


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


@app.route("/users/<int:user_id>/edit")
def show_edit_page(user_id):
    """show user edit page"""
    user = User.query.get_or_404(user_id)

    return render_template("edit.html", user=user)


@app.route("/users/<int:user_id>/edit", methods=["POST"])
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


@app.route('/users/<int:user_id>/delete', methods=["GET"])
def delete_user(user_id):
    """delete a single user"""
    del_user = User.query.get_or_404(user_id)
    db.session.delete(del_user)
    db.session.commit()

    flash(f"Deleted {del_user.get_fullname()}", "danger")
    return redirect("/")
