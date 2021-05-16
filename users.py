# System modules.
from datetime import datetime

# 3rd party modules.
from flask import make_response, abort
import requests

# Personal modules.
from config import db
from models import Master, MasterSchema, Detail, DetailSchema


# Get current time as a timestamp string.
def _get_timestamp():

    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))


# From postal code to city name (Spain only).
def _get_cityname(postalcode):

    try:
        r = requests.get(
            "http://api.geonames.org/postalCodeLookupJSON?postalcode="
            + postalcode
            + "&country=ES&username=jperezvisaires"
        )
        cityname = r.json()["postalcodes"][-1]["placeName"]

    except:
        cityname = None

    return cityname


# CREATE operations.
def create(user):
    """
    This function creates a new user in the database
    based on the passed-in user data.

    :param user: User to create in database
    
    :return: 201 on success, 400 on bad postal code, 406 on user exists
    """
    username = user.get("username", None)
    postalcode = user.get("postalcode", None)
    cityname = _get_cityname(postalcode)

    # Does the user already exist?
    existing_master = Master.query.filter(Master.username == username).one_or_none()

    if existing_master is None and cityname is not None:
        # Create a user instance using the schema and the passed-in user.
        user_master = Master(username=username)
        db.session.add(user_master)
        user_detail = Detail(postalcode=postalcode, cityname=cityname)
        db.session.add(user_detail)

        # Save changes to database.
        db.session.commit()

        return make_response(
            "{username} successfully created".format(username=username), 201,
        )

    # If the Postal Code doesn't return any hits in Geonames
    elif cityname is None:
        abort(
            400, "Postal code {postalcode} is invalid".format(postalcode=postalcode),
        )

    # Otherwise, they exist, and that's an error
    else:
        abort(
            406,
            "User with username {username} already exists".format(username=username),
        )


# READ operations.
def read_all():
    """
    This function responds to a request for /api/users
    with the complete lists of users.

    :return: JSON string of list of users
    """
    # Create the list of people from our data
    master = Master.query.all()

    # Serialize the data for the response
    master_schema = MasterSchema(many=True)

    return master_schema.dump(master)


def read_one(username):
    """
    This function responds to a request for /api/users/{username}
    with one matching user from the database.

    :param username: Username of user to find

    :return: User matching username
    """
    # Get the user requested
    master = Master.query.filter(Master.username == username).one_or_none()

    # Did we find a user?
    if master is not None:

        # Serialize the data for the response
        master_schema = MasterSchema()

        return master_schema.dump(master)

    # Otherwise, not found.
    else:
        abort(404, "User with username {username} not found".format(username=username))


def read_one_details(username):
    """
    This function responds to a request for /api/users/{username}
    with one matching user from the database.

    :param username: Username of user to find

    :return: User matching username
    """
    # Get the user requested
    master = Master.query.filter(Master.username == username).one_or_none()
    detail = Detail.query.filter(Detail.user_id == master.user_id).one_or_none()

    # Did we find a user?
    if detail is not None:

        # Serialize the data for the response
        detail_schema = DetailSchema()

        return detail_schema.dump(detail)

    # Otherwise, not found.
    else:
        abort(404, "User with username {username} not found".format(username=username))


# UPDATE operations.
def update(username, user):
    """
    This function updates an existing user in the database.

    :param username: Username of user to update in the database
    :param user: User to update

    :return: Updated user structure
    """
    cityname = _get_cityname(user.get("postalcode"))

    # Get the user requested from the db into session
    master_update = Master.query.filter(Master.username == username).one_or_none()
    detail_update = Master.query.filter(Master.username == username).one_or_none()

    # Does the user already exist?
    if username is not None and cityname is not None:
        # turn the passed in person into a db object
        master_user = {"username": user["username"]}
        master_schema = MasterSchema()
        master_update = master_schema.load(master_user, session=db.session)

        detail_user = {"postalcode": user["postalcode"], "cityname": cityname}
        detail_schema = DetailSchema()
        detail_update = detail_schema.load(detail_user, session=db.session)

        # Set the id to the person we want to update
        master_update.user_id = master_update.user_id
        detail_update.user_id = detail_update.user_id

        # merge the new object into the old and commit it to the db
        db.session.merge(master_update)
        db.session.merge(detail_update)
        db.session.commit()

        # return updated person in the response
        data = master_schema.dump(master_update)

        return data, 200

    # If the Postal Code doesn't return any hits in Geonames
    elif cityname is None:
        abort(
            400,
            "Postal code {postalcode} is invalid".format(
                postalcode=user.get("postalcode")
            ),
        )

    # Otherwise, that's an error
    else:
        abort(
            404, "User with username {username} not found".format(username=username),
        )


# DELETE operations.
def delete(username):
    """
    This function deletes a user from the users structure

    :param username: Username of user to delete

    :return: 200 on successful delete, 404 if not found
    """
    # Get the person requested
    master = Master.query.filter(Master.username == username).one_or_none()
    detail = Detail.query.filter(Detail.user_id == master.user_id).one_or_none()

    # Does the person to delete exist?
    if master is not None:
        db.session.delete(master)
        db.session.delete(detail)
        db.session.commit()

        return make_response(
            "{username} successfully deleted".format(username=username), 200
        )

    # Otherwise, user to delete not found
    else:
        abort(404, "User with username {username} not found".format(username=username))
