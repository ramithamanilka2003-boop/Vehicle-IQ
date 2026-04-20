from main import db,login_manager
from datetime import datetime
from flask_login import UserMixin


class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True,unique=True,nullable=False)
    username=db.Column(db.String(20),unique=True,nullable=False)
    email=db.Column(db.String(40),unique=True,nullable=False)
    password=db.Column(db.String(60),nullable=False)
    is_admin = db.Column(db.Boolean, default=False) 
    predictions=db.relationship('Prediction',backref='user',lazy=True)

    def get_id(self):
        return f"user:{self.id}"

    def __repr__(self):
        return f"User('{self.username}','{self.email}')"
    
class Prediction(db.Model):
    id=db.Column(db.Integer,primary_key=True,unique=True,nullable=False)
    model=db.Column(db.String(20),nullable=False)
    model_year=db.Column(db.String(4),nullable=False)
    milage=db.Column(db.Integer,nullable=False)
    fuel_type=db.Column(db.String(10),nullable=False)
    transmission=db.Column(db.String(10),nullable=False)
    ext_col=db.Column(db.String(10),nullable=False)
    type=db.Column(db.String(10),nullable=False)
    condition=db.Column(db.String(10),nullable=False)
    location=db.Column(db.String(20),nullable=False)
    cc=db.Column(db.Integer,nullable=False)
    power_steering = db.Column(db.Boolean, default=False, nullable=False)
    push_start = db.Column(db.Boolean, default=False, nullable=False)
    price=db.Column(db.Integer,nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Prediction(User={self.user.username}, Model={self.model}, Year={self.model_year}, Price={self.price})>"
    
class Vehicles(db.Model):
    id=db.Column(db.Integer,primary_key=True,unique=True,nullable=False)
    photo=db.Column(db.String(60),nullable=True)
    brand=db.Column(db.String(20),nullable=False)
    model=db.Column(db.String(20),nullable=False)
    vehicle_category=db.Column(db.String(20),nullable=False)
    fuel_type=db.Column(db.String(20),nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


    def __repr__(self):
        return f"Vehicle('{self.brand}','{self.model}','{self.vehicle_category}','{self.fuel_type}')"
    

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('feedbacks', lazy='dynamic'), lazy='joined')

    def __repr__(self):
        return f"Feedback('{self.rating}','{self.message}')"

class Admin(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True,unique=True,nullable=False)
    username=db.Column(db.String(20),unique=True,nullable=False)
    email=db.Column(db.String(40),unique=True,nullable=False)
    password=db.Column(db.String(60),nullable=False)
    is_admin = db.Column(db.Boolean, default=True)

    def get_id(self):
        return f"admin:{self.id}"

    def __repr__(self):
        return f"Admin('{self.username}','{self.email}')"

class Budgetrequest(db.Model):
    id=db.Column(db.Integer,primary_key=True,unique=True,nullable=False)
    model=db.Column(db.String(20),nullable=False)
    year=db.Column(db.String(40),nullable=False)
    price=db.Column(db.Integer,nullable=False)

    def __repr__(self):
        return f"Budgetrequest('{self.model}','{self.year}','{self.price}')"
    