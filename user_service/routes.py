from flask import Blueprint, request, jsonify, current_app
from sqlalchemy.orm import Session, joinedload
from models import db, User, UserRoles
from auth import generate_jwt_token, verify_jwt_token

user_bp = Blueprint('users', '__name__')

@user_bp.route('/', methods=['GET'])
def get_all_users():
    try:
        # Query all users
        users = User.query.all()
        
        # Serialize the result
        users_data = [
            {
                "user_id": user.id,
                "username": user.username,
                "email": user.email,
                "user_role": user.user_role.name if user.user_role else None,
                "user_role_id": user.user_role_id
            }
            for user in users
        ]
        
        return jsonify(users_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route("/register", methods=['POST'])
def register():
    data = request.get_json()
    current_app.logger.info("Processing user registration")
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"Error": "User Already Exist"}), 400
    
    user = User(username=data['username'], email=data['email'], user_role_id=data["user_role_id"])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    current_app.logger.info("User registration successful")
    return jsonify({"message": "User created successfully"}), 201

@user_bp.route('/login', methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    current_app.logger.info(f"Processing {user.email if user else data['email']} for login..!")

    if user and user.check_password(data['password']):
        token = generate_jwt_token(user.id, user.username)
        return jsonify({"token": token})
    
    current_app.logger.info(f"Invalid creds for user: {data['email']} for login..!!")
    return jsonify({"Error": "Invalid Credentials"}), 401


@user_bp.route("/profile", methods=["GET"])
def user_profile():
    try:
        token = request.headers.get("Authorization").split()[1]
        current_app.logger.info("User Authentication Pending...")
        decoded_token = verify_jwt_token(token)
        user_id = decoded_token.get("user_id")

        if user_id is None:
            return jsonify({"Error": "Invalid Token or Expired Token."}), 404

        with Session(db.engine) as session:
            # Use joinedload to eagerly load user_role in the same query
            user = (
                session.query(User)
                .options(joinedload(User.user_role))  # Ensures user_role is loaded
                .filter(User.id == user_id)
                .one_or_none()
            )

        if user is None:
            current_app.logger.info("User not found")
            return jsonify({"Error": "User not found"}), 404

        current_app.logger.info(f"User login profile {user.username} redirection..!!")
        current_app.logger.info(f"User role Name: {user.user_role.name if user.user_role else 'No Role'}")

        return jsonify({
            "user_id": user.id,
            "username": user.username,
            "email": user.email,
            "user_role": user.user_role.name if user.user_role else "No Role",
            "user_role_id": user.user_role_id
        })
    except Exception as e:
        current_app.logger.info("Invalid or Expired Token: " + str(e))
        return jsonify({"Error": "Invalid or Expired Token or Token not provided.."}), 401



@user_bp.route("/user_role", methods=['POST'])
def create_user_role():
    data = request.get_json()
    current_app.logger.info("Processing user role creation..")
    
    user_role = UserRoles(name=data['name'], description=data['description'])
    db.session.add(user_role)
    db.session.commit()
    current_app.logger.info("User registration successful")
    return jsonify({"message": "User Role created successfully"}), 201


@user_bp.route("/logout", methods=["POST"])
def logout():
    current_app.logger.info("User Logged in success")
    return jsonify({'message': "User Logged in success"})