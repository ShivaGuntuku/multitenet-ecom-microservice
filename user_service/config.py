import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "hello_world")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///user_service.db") # For Sqlitedb
    # SQLALCHEMY_DATABASE_URI="postgresql://ecom_db_padmin:ecom_db_padmin_pass@localhost:5432/user_service_db"
    # SQLALCHEMY_DATABASE_URI="postgresql://ecom_db_padmin:ecom_db_padmin_pass@db:5432/user_service_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

config = Config()