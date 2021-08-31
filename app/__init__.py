import os
from flask import Flask, render_template
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


if __name__ == "__main__":
    app.run(host="127.0.0.1", port="5000", debug=True)

