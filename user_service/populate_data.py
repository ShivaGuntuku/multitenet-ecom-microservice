import os
from werkzeug.security import generate_password_hash

from models import db, User, UserRoles
from app import app

def populate_db():
    user_roles = [
        UserRoles(name="Admin", description="Super Admin"),
        UserRoles(name="Vendor", description="Able to add the products"),
        UserRoles(name="Customer", description="Able to purchase products")
    ]
    db.session.add_all(user_roles)
    db.session.commit()

def create_dummy_users():
    users = [User(username="Super Admin",email="admin@example.com",hashed_password=generate_password_hash("admin"),user_role_id=1),
             User(username="Vendor",email="vendor@example.com",hashed_password=generate_password_hash("vendor"), user_role_id=2),
             User(username="Customer",email="customer@example.com",hashed_password=generate_password_hash("customer"), user_role_id=3)]
    db.session.add_all(users)
    db.session.commit()

with app.app_context():
    populate_db()
    create_dummy_users()

print("Data Populated succesfully...")