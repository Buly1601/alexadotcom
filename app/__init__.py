import os
import re
from flask import Flask, render_template, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
#from flask_migrate import Migrate

app = Flask(__name__)

# setting up db
# app.config["SQALCHEMY_DATABASE_URI"] = "sqlite:///registration.db"
db = SQLAlchemy(app)

# basic registration
class User_password(db.Model):

    id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    name = db.Column(db.Text)
    password = db.Column(db.String)

    def __init__(self, name, password):
        self.name = name
        self.password = password


with app.app_context():
    
    @app.route("/")
    def main_page():
        """
        Renders the main pagem, where basic info is displayed for the user
        """
        return render_template("main_page.html", title="Menu", url=os.getenv("URL"))

    @app.route("/login", methods=["GET","POST"])
    def login_page():
        """
        Renders the login page, as well as some db work to confirm user's 
        identity
        """
        if request.method == "POST":
            # take information from post
            username = request.form.get("username")
            password = request.form.get("password")
            conf_passoword = request.form.get("conf_psswd")
            error = None

            # check for potential errors before adding to db
            if not username:
                error = "Username is required."
            elif not password:
                error = "Password is required."
            elif password != conf_passoword:
                error = "Passwords must match."
            elif User_password.query.filter_by(name=username).first() is not None:
                error = f"User {username} already exists, try logging in."

            if not error:
                # TODO need JSON
                new_user = User_password(username, generate_password_hash(password))
                db.session.add(new_user)
                db.session.commit()
                return "Success"

            else:
                return error, 402
        
        else:
            return render_template("login_page.hmtl", title="Login", url=os.getenv("URL"))

    @app.route("/register", methods=["GET", "POST"])
    def register_page():
        """
        Renders the register page, as well as creates the user instance
        in the db
        """
        if request.method == "POST":
            # take information from post
            username = request.form.get("username")
            password = request.form.get("password")
            user_check = User_password.query.filter_by(name=username).first()
            error = None

            if not username:
                error = "Username is required"
            elif not password:
                error = "Password is required"
            elif user_check is None:
                error = "Nonexistent username"
            elif check_password_hash(user_check.password, password):
                error = "Incorrect password"

            if not error:
                # TODO return json
                # TODO render user's template
                return "success", 200
            else:
                return error,402
        
        else:
            return render_template("register_page.html", title="Register", url=os.getenv("URL"))
    
    @app.route("/__health__")
    def healthy():
        """
        Health monitoring help function
        """
        return ""

if __name__ == "__main__":
    app.run(host="127.0.0.1", port="5000", debug=True)

