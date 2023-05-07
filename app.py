from flask import Flask, render_template, redirect, session, flash
from models import db, connect_db, User, Feedback
from forms import RegisterUserForm, LoginForm, FeedbackForm, EditFeedbackForm
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///sb_flask_feedback"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "Oh-So-Secret"

connect_db(app)


@app.errorhandler(404)
def not_found(error):
    """ Handles 404 errors """
    return render_template("404.html")


@app.route("/")
def redirect_to_register():
    return redirect("/register")


@app.route("/register", methods=["GET", "POST"])
def handle_register():
    """ Returns register.html if method is get, else will handle form data from register.html """
    form = RegisterUserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        new_user = User.register(
            username, password, email, first_name, last_name)

        db.session.add(new_user)

        try:
            db.session.commit()
        except IntegrityError:
            flash("Please resubmit form with new data.", "danger")
            return render_template("register.html", form=form)

        session["current_user"] = new_user.username
        flash("Successfully created your account!", "success")
        return redirect(f"/users/{new_user.username}")
    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def handle_login():
    """ Returns login.html if method is get, else will handle form data from login.html """
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            flash(f"Welcome back {user.first_name}!", "primary")
            session["current_user"] = user.username
            return redirect(f"/users/{user.username}")

        else:
            flash("Incorrect login info, please try again", "danger")

    return render_template("login.html", form=form)


@app.route("/logout")
def logout_user():
    session.pop("current_user")
    flash("Goodbye!", "info")
    return redirect("/")


@app.route("/users/<username>")
def show_page(username):
    if "current_user" not in session:
        flash("Please Login to view", "danger")
        return redirect("/login")
    return render_template("user.html", user=User.query.get(username))


@app.route("/users/<username>/delete")
def delete_user(username):
    user = User.query.get(username)
    db.session.delete(user)
    db.session.commit()
    return redirect("/")


@app.route("/users/<username>/feedback/add", methods=["GET", "POST"])
def add_feedback(username):
    """ 
    GET: Display a form to add feedback.
    
    POST: Add a new piece of feedback and redirect to /users/<username>
    """
    if "current_user" not in session:
        flash("Please Login to view", "danger")
        return redirect("/login")
    
    form = FeedbackForm()
    
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        user = User.query.get(username)
        
        new_post = Feedback(title=title, content=content, username=user.username)
        
        db.session.add(new_post)
        db.session.commit()
        
        return redirect(f"/users/{user.username}")
    
    return render_template("new-feedback.html", form=form)
        
    
@app.route("/feedback/<int:id>/update", methods=["GET", "POST"])
def update_feedback(id):
    """ 
    GET: Display a form to edit feedback 

    POST: Update a specific piece of feedback and redirect to /users/<username>
    """
    
    if "current_user" not in session:
        flash("Please Login to view", "danger")
        return redirect("/login")
    
    form = EditFeedbackForm()
    post = Feedback.query.get_or_404(id)
    
    if form.validate_on_submit():
        old_title = post.title
        
        post.title = form.title.data if form.title.data else post.title
        post.content = form.content.data if form.content.data else post.content
        
        db.session.add(post)
        db.session.commit()
        
        flash(f"'{old_title}' was successfully updated", "success")
        return redirect(f"/users/{post.username}")
    
    return render_template("edit-feedback.html", form=form)


@app.route("/feedback/<int:id>/delete")
def delete_feedback(id):
    """ Delete a specific piece of feedback and redirect to /users/<username> """
    
    if "current_user" not in session:
        flash("Please Login to view", "danger")
        return redirect("/login")
    
    post = Feedback.query.get_or_404(id)
    title = post.title
    username = post.username
        
    db.session.delete(post)
    db.session.commit()

    flash(f"{title} was successfully deleted", "success")
    return redirect(f"/users/{username}")