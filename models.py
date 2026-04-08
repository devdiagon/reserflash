import uuid
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Reservation(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    date = db.Column(db.String(50), nullable=False)
    room = db.Column(db.String(50), nullable=False)
    hour = db.Column(db.String(50), nullable=False)

    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'), nullable=False)