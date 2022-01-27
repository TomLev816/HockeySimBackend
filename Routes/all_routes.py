from app import db, app, guard
import flask
import flask_praetorian

from Tables import all_tables

# Set up some routes for the example
@app.route('/api/')
def home():
    return {"Hello": "World"}, 200

@app.route("/api/reset_tables", methods=["GET"])
def reset_tables():
    db.drop_all()
    db.create_all()
    User = all_tables.User
    if db.session.query(User).filter_by(username='tom').count() < 1:
        db.session.add(User(
          username='tom',
          password=guard.hash_password('tom'),
          roles='admin'
            ))
    db.session.commit()
    return "reset Tables"

@app.route('/api/login', methods=['POST'])
def login():
    """
    Logs a user in by parsing a POST request containing user credentials and
    issuing a JWT token.
    .. example::
        $ curl http://localhost:5000/api/login -X POST \
        -d '{"username":"Tom","password":"tom"}'
    """
    req = flask.request.get_json(force=True)
    username = req.get('username', None)
    password = req.get('password', None)
    user = guard.authenticate(username, password)
    ret = {'access_token': guard.encode_jwt_token(user)}
    return ret, 200


@app.route('/api/refresh', methods=['POST'])
def refresh():
    """
    Refreshes an existing JWT by creating a new one that is a copy of the old
    except that it has a refrehsed access expiration.
    .. example::
       $ curl http://localhost:5000/api/refresh -X GET \
         -H "Authorization: Bearer <your_token>"
    """
    print("refresh request")
    old_token = request.get_data()
    new_token = guard.refresh_jwt_token(old_token)
    ret = {'access_token': new_token}
    return ret, 200


@app.route('/api/protected')
@flask_praetorian.auth_required
def protected():
    """
    A protected endpoint. The auth_required decorator will require a header
    containing a valid JWT
    .. example::
       $ curl http://localhost:5000/api/protected -X GET \
         -H "Authorization: Bearer <your_token>"
    """
    return {'message': f'protected endpoint (allowed user {flask_praetorian.current_user().username})'}
