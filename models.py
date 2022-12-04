from sqlalchemy.orm import relationship

from database import Base
from sqlalchemy import Column, String, Integer, ForeignKey


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
