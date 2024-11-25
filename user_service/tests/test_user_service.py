import pytest
from app import app, db
from models import User, UserRoles

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_create_user_role(client):
    response = client.post('/user/user_role', json={
        "name": "Vendor1",
        "description": "Vendor Role",
    })
    assert response.status_code == 201


def test_register_user(client):
    response = client.post('/user/register', json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123",
        "user_role_id": 1
    })
    assert response.status_code == 201
    assert response.get_json() == {"message": "User created successfully"}


def test_get_all_users(client):
    # Pre-create a user role and a user as in previous tests
    test_create_user_role(client)
    test_register_user(client)
    
    response = client.get("/user/")
    assert response.status_code == 200
    assert response.get_json() == [{"user_id": 1,
                                    "username": "testuser",
                                    "email": "test@example.com",
                                    "user_role": "Vendor1",
                                    "user_role_id":1}]



def test_duplicate_register_user(client):
    # Pre-create a user role and a user as in previous tests
    test_create_user_role(client)
    test_register_user(client)

    # Test duplicate registration
    response = client.post('/user/register', json={
        "username": "testuser2",
        "email": "test@example.com",
        "password": "password123",
        "user_role_id": 1
    })
    assert response.status_code == 400
    assert response.get_json() == {"Error": "User Already Exist"}

def test_login_user(client):
    # Pre-create a user role and a user as in previous tests
    test_create_user_role(client)
    test_register_user(client)

    # Test successful login
    response = client.post('/user/login', json={
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    assert "token" in response.get_json()

    # Test login with invalid credentials
    response = client.post('/user/login', json={
        "email": "test@example.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401
    assert response.get_json() == {"Error": "Invalid Credentials"}

def test_profile_access(client):
    # Pre-create a user role and a user as in previous tests
    test_create_user_role(client)
    test_register_user(client)

    # Test successful login
    login_response = client.post('/user/login', json={
        "email": "test@example.com",
        "password": "password123"
    })
    assert login_response.status_code == 200

    token = login_response.get_json()["token"]

    #Access profile with valid token
    response = client.get("/user/profile", headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 200
    assert response.get_json() == {"user_id":1, "username": "testuser", 
                                   "email": "test@example.com", "user_role": "Vendor1",
                                   "user_role_id": 1
                                   }

    # Access profile with invalid token
    response = client.get("/user/profile", headers={
        "Authorization": f"Bearer invalidtoken"
    })
    assert response.status_code == 401
    assert response.get_json() == {"Error": "Invalid or Expired Token or Token not provided.."}