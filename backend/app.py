import os
from datetime import datetime
from functools import wraps
from pathlib import Path

import jwt
from dotenv import load_dotenv
from flask import Flask, jsonify, make_response, request
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)


app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f'sqlite:///{Path().cwd() / "db_web.db"}'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    private_key = db.Column(db.String(255), nullable=False)
    passphrase = db.Column(db.String(255), nullable=False)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if "x-access-token" in request.headers:
            token = request.headers["x-access-token"]

        if not token:
            return make_response(
                jsonify({"success": False, "data": "Token missing"}), 403
            )

        try:
            data = jwt.decode(
                token, app.config["SECRET_KEY"], algorithms=["HS256"]
            )
            current_user = Users.query.filter_by(id=data["id"]).first()
        except:
            return make_response(
                jsonify({"success": False, "data": "Token is invalid"}), 401
            )

        # returns the current logged in users contex to the routes
        return f(current_user, *args, **kwargs)

    return decorated


@app.route("/health", methods=["GET"])
def index():
    return make_response(
        jsonify({"timestamp": datetime.now().isoformat()}), 200
    )


@app.route("/protected", methods=["GET"])
@token_required
def protected(current_user):
    return make_response(
        jsonify(
            {
                "success": True,
                "email": current_user.email,
                "data": "Viewing protected data!",
            }
        ),
        200,
    )


@app.route("/register", methods=["POST"])
def register():
    email = request.json["email"]
    password = request.json["password"]
    role = request.json["role"]

    hashed_password = bcrypt.generate_password_hash(password)

    user = Users.query.filter_by(email=email).first()

    if not user:
        user = Users(email=email, password=hashed_password, role=role)

        db.session.add(user)
        db.session.commit()

        return make_response(
            jsonify({"success": True, "data": "Successfully registered"}), 201
        )
    else:
        return make_response(
            jsonify(
                {
                    "success": False,
                    "data": "User already exists. Please Log in",
                }
            ),
            202,
        )


@app.route("/login", methods=["POST"])
def login():
    email = request.json["email"]
    password = request.json["password"]

    user = Users.query.filter_by(email=email).first()

    if not user:
        return make_response(
            jsonify(
                {
                    "success": False,
                    "data": "User not found",
                }
            ),
            404,
        )

    if bcrypt.check_password_hash(password=password, pw_hash=user.password):
        token = jwt.encode(
            {"id": user.id, "email": user.email},
            app.config["SECRET_KEY"],
            algorithm="HS256",
        )

        return make_response(
            jsonify(
                {
                    "success": True,
                    "data": {
                        "token": token,
                        "id": user.id,
                        "email": user.email,
                        "role": user.role,
                    },
                }
            ),
            200,
        )

    return make_response(
        jsonify(
            {
                "success": False,
                "data": "Invalid credentials",
            }
        ),
        404,
    )


if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
