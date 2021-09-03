import os
import re
from flask import Flask, render_template, request
#from werkzeug.security import generate_password_hash, check_password_hash
#from flask_sqlalchemy import SQLAlchemy
#from flask_migrate import Migrate

app = Flask(__name__)

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

            if not username:
                error = "Username is required"
            elif not password:
                error = "Password is required"
            elif password != conf_passoword:
                error = "Passwords must match"
            # TODO check existance of user in db

            if not error:
                # TODO need JSON
                return "success"

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
            error = None

            if not username:
                error = "Username is required"
            elif not password:
                error = "Password is required"
            # TODO check the existance of user and password with hash

            if not error:
                # TODO return json
                return "success"
            else:
                return error,402
        
        else:
            return render_template("register_page.html", title="Register", url=os.getenv("URL"))

if __name__ == "__main__":
    app.run(host="127.0.0.1", port="5000", debug=True)

