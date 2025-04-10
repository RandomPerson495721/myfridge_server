import uuid

from sqlalchemy import DateTime, Column, ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.sql.sqltypes import NULLTYPE, Integer, String

from models.models import Base, db



class Item(db.Model):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)
    quantity = Column(Integer, nullable=False)
    expiration_date = Column(DateTime, nullable=True)
    position = Column(Integer, nullable=False)
    user_id = Column(String(255), nullable=False)
    reference_id = Column(String(255), nullable=False)
    image_url = Column(String(255), nullable=True)


    def __init__(self, name, description, quantity, expiration_date, position, user_id, image_url):
        super().__init__()
        self.name: Mapped[str] = name
        self.description: Mapped[str] = description
        self.quantity: Mapped[int] = quantity
        self.expiration_date: Mapped[DateTime] = expiration_date
        self.position: Mapped[int] = position
        self.reference_id: Mapped[str] = str(uuid.uuid4())
        self.user_id: Mapped[int] = user_id
        self.image_url: Mapped[str] = image_url


    def to_dict(self):
        return {
            'name': self.name,
            'description': self.description,
            'quantity': self.quantity,
            'expiration_date': self.expiration_date.isoformat(),
            'position': self.position,
            'reference_id': self.reference_id,
            'image_url': self.image_url,
        }

    def from_dict(self, data):
        for field in ['name', 'description', 'quantity', 'expiration_date', 'position' 'reference_id']:
            if field in data:
                setattr(self, field, data[field])
        return self

