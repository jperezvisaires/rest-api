# System modules.
import os

# 3rd party modules.
from flask import render_template
import connexion

# Local modules.
import config

"""
We are using the Flask Micro Framework to create a simple web server that
serves as a REST API. We also use Connexion to add Swagger specification to
our API.

Using Swagger adds useful extra functionality: validation of input and output 
(to and from our API), a really easy way of configuring URL endpoints (and the 
expected parameters) and a nice UI to explore the created API.
"""

# Get the app instance.
app = config.connex_app

# Configure API endpoints using connexion and the swagger.yml file.
app.add_api("swagger.ylm")

# Create the '/' URL route in our app.
@app.route("/")
def home():
    """
    The home function responds to the browser URL localhost:5000/

    :return: The rendered template 'home.html'
    """
    return render_template("home.html")


# Directly run the app if we're running in standalone mode and not importing
# as a package.
# Swagger UI found in "0.0.0.0:5000/api/ui"
if __name__ == "__main__":
    app.run(debug=True)
