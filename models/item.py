import uuid

from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from sqlalchemy import DateTime, Column, ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.sql.sqltypes import NULLTYPE, Integer, String

from models.models import Base, db


# A class to represent an item in the inventory.

class Item(db.Model):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)
    quantity = Column(Integer, nullable=False)
    expiration_date = Column(DateTime, nullable=True)
    position = Column(Integer, nullable=False)
    user_id = Column(String(255), nullable=False)
    reference_id = Column(Integer, nullable=False)


    def __init__(self, name, description, quantity, expiration_date, position, user_id):
        super().__init__()
        self.name: Mapped[str] = name
        self.description: Mapped[str] = description
        self.quantity: Mapped[int] = quantity
        self.expiration_date: Mapped[DateTime] = expiration_date
        self.position: Mapped[int] = position
        self.reference_id: Mapped[str] = str(uuid.uuid4())
        self.user_id: Mapped[int] = user_id


    def to_dict(self):
        return {
            'name': self.name,
            'description': self.description,
            'quantity': self.quantity,
            'expiration_date': self.expiration_date.isoformat(),
            'position': self.position,
            'unique_id': self.reference_id,
        }

    def from_dict(self, data):
        for field in ['name', 'description', 'quantity', 'expiration_date']:
            if field in data:
                setattr(self, field, data[field])
        return self

# A class to represent a database connection.
