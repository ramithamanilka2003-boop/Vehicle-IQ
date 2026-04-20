from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from main.config import config
import pickle

db = SQLAlchemy()
bcrypt=Bcrypt()
login_manager=LoginManager()
login_manager.login_view='users.login'
login_manager.login_message_category = "info"

from main.models import Admin, User

@login_manager.user_loader
def load_user(user_id):
    if ":" in user_id:
        role, uid = user_id.split(":", 1)
        if role == "admin":
            return db.session.get(Admin, int(uid))
        elif role == "user":
            return db.session.get(User, int(uid))
    
    # Fallback/Backward compatibility for existing sessions (pre-prefix)
    try:
        uid = int(user_id)
        admin = db.session.get(Admin, uid)
        if admin:
            return admin
        return db.session.get(User, uid)
    except (ValueError, TypeError):
        return None



def create_app(config_class=config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    with open("main/artifacts/model.pkl", "rb") as f:
        app.model = pickle.load(f)

    with open("main/artifacts/model_columns.pkl", "rb") as f:
        app.model_columns = pickle.load(f)

    from main.Users.routes import users
    from main.About.routes import info
    from main.Feedbacks.routes import feedbacks
    from main.Home.routes import index
    from main.Predictions.routes import prediction
    from main.Search.routes import searchs
    from main.Admins.routes import admin
    from main.Error.handler import errors

    app.register_blueprint(users)
    app.register_blueprint(info)
    app.register_blueprint(feedbacks)
    app.register_blueprint(index)
    app.register_blueprint(prediction)
    app.register_blueprint(searchs)
    app.register_blueprint(admin)
    app.register_blueprint(errors)
    
    return app