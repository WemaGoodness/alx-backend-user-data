#!/usr/bin/env python3
"""
SQLAlchemy User model definition.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    """
    SQLAlchemy model for a user. Represents the 'users' table in the database.
    Attributes:
        id (int): The user's ID, primary key.
        email (str): The user's email, must be non-nullable.
        hashed_password (str): The user's password (hashed), must be
        non-nullable.
        session_id (str): The user's session ID, can be nullable.
        reset_token (str): The token used to reset the user's password,
        can be nullable.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
