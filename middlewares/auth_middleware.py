import jwt
from uuid import UUID
from flask import request, jsonify
from functools import wraps
from config import Config

def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]

        if not token:
            return jsonify({"message": "Necesita iniciar sesión"}), 401

        try:
            data = jwt.decode(token, Config.JWT_SECRET, algorithms=["HS256"])
            request.user_id = UUID(data['user_id'])
        except:
            return jsonify({"message": "Ha ocurrido un error"}), 401

        return f(*args, **kwargs)

    return decorated