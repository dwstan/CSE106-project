from flask import Flask
from website.user import user as user
from website.auth import auth as auth
from .model import db, User
from flask_login import LoginManager
  # Import the 'main' blueprint from the routes module

# Defines some of the Flask app's creation and settings
def create_app():
    app = Flask(__name__)

    # Register the 'main' blueprint
    app.register_blueprint(user)
    app.register_blueprint(auth)

    # Configure SQLAlchemy
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite'  # Store the database locally in the instance folder
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'secret-key-goes-here'



    db.init_app(app)


    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)


    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))






    return app