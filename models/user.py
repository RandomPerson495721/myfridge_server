from sqlalchemy import DateTime, Column, ForeignKey
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.sql.sqltypes import NULLTYPE, Integer, String
from models import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    items = relationship("item", back_populates="user")

    def __init__(self, name, email, password):
        self.name: Mapped[str] = name