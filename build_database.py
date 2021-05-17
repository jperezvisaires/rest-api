# System modules.
import os

# Personal modules.
from config import db
from models import Master, Detail

# List of dictionaries to populate the 2 databases (master and detail).
USERS = [
    {"username": "Aitor", "postalcode": "01240", "cityname": "Alegria-Dulantzi",},
    {"username": "Mikel", "postalcode": "01001", "cityname": "Vitoria-Gasteiz",},
    {"username": "Amaia", "postalcode": "48011", "cityname": "Bilbao",},
]

# Get absolute path of this file.
base_dir = os.path.abspath(os.path.dirname(__file__))

# Delete database file if it exists currently.
if os.path.isfile(os.path.join(base_dir, "users.db")):
    print("Removed database")
    os.remove("users.db")

# Creates the database.
db.create_all()

# Iterate over the USERS structure and populate the databases.
for user in USERS:
    user_master = Master(username=user["username"])
    user_detail = Detail(postalcode=user["postalcode"], cityname=user["cityname"])
    db.session.add(user_master)
    db.session.add(user_detail)

# Save changes to database.
db.session.commit()
