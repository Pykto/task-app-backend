from app import db
from datetime import datetime, timezone
from enum import Enum


class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


class State(Enum):
    PENDING = 1
    IN_PROGRESS = 2
    COMPLETED = 3
    CANCELLED = 4


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    priority = db.Column(db.Enum(Priority), nullable=False)
    state = db.Column(db.Enum(State), nullable=False)
    creation_date = db.Column(
        db.DateTime, default=datetime.now(timezone.utc), nullable=False)
    expiration_date = db.Column(db.DateTime)

    def __repr__(self):
        return f'<Task {self.id - self.title}>'
