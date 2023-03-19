import os
from flask import Flask
from flask_jwt_extended import JWTManager, create_access_token
from flask import request, jsonify
from bson import ObjectId
import json
from pydantic.json import pydantic_encoder

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from .api.v1 import customer as customer_v1
from .api.v2 import customer as customer_v2

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return pydantic_encoder(obj)

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'secret-jwt'
app.json_encoder = CustomJSONEncoder
jwt = JWTManager(app)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)

@app.route('/login', methods=['POST'])
def login():
    print('here')
    raw_data = request.get_json()
    username = raw_data.get('username', None)
    password = raw_data.get('password', None)
    if username != 'admin' or password != 'password':
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)
    return jsonify(username)


app.register_blueprint(customer_v1.bp)
app.register_blueprint(customer_v2.bp)

