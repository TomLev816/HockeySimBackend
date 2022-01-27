import os
import flask
import flask_sqlalchemy
import flask_praetorian
import flask_cors

db = flask_sqlalchemy.SQLAlchemy()
guard = flask_praetorian.Praetorian()
cors = flask_cors.CORS()


# Initialize flask app for the example
app = flask.Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'top secret'
app.config['JWT_ACCESS_LIFESPAN'] = {'hours': 24}
app.config['JWT_REFRESH_LIFESPAN'] = {'days': 30}

from Routes import all_routes
from Tables import all_tables

# Initialize the flask-praetorian instance for the app
guard.init_app(app, all_tables.User)

# Initialize a local database for the example
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///OwnerSim.db"
db.init_app(app)

# Initializes CORS so that the api_tool can talk to the example app
cors.init_app(app)


if __name__ == "__main__":
    app.run(debug=True) # debug=True restarts the server everytime we make a change in our code