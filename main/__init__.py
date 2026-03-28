from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager,current_user
import pickle

app = Flask(__name__)
app.config['SECRET_KEY']='46ced26eca7241daacbd4280470e9612'
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///vehicle.db"
db = SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager=LoginManager(app)
login_manager.login_view='users.login'
login_manager.login_message_category = "info"

from main.models import Admin, User

@login_manager.user_loader
def load_user(user_id):
    admin = Admin.query.get(int(user_id))
    if admin:
        return admin
    return User.query.get(int(user_id))

with open("main/artifacts/model.pkl", "rb") as f:
    model = pickle.load(f)

with open("main/artifacts/model_columns.pkl", "rb") as f:
    model_columns = pickle.load(f)

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