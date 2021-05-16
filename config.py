# System modules.
import os

# 3rd party modules.
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Get absolute path of this file.
base_dir = os.path.abspath(os.path.dirname(__file__))

# Create the Connexion application instance.
connex_app = connexion.App(__name__, specification_dir=base_dir)

# Get the underlying Flask app instance.
app = connex_app.app

# Configure the SQLAlchemy part of the app instance.
# Echo SQL statements to console.
app.config["SQLALCHEMY_ECHO"] = True
# Use SQLite as database and users.db as database file.
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////" + os.path.join(
    base_dir, "users.db"
)
# Turn off SQLAlchemy's event system.
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Create the SQLAlchemy db instance.
db = SQLAlchemy(app)

# Initialize Marshmallow as ma. After SQLAlchemy instance initialization.
ma = Marshmallow(app)
