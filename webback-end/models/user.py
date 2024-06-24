#!/usr/bin/python3
""" holds class User"""

import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from hashlib import md5


class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        username = Column(String(50), nullable=False, unique=True)
        email = Column(String(128), nullable=False, unique=True)
        password = Column(String(128), nullable=False)
        reports = relationship('Report', backref='user', lazy=True)
        alerts = relationship('Alert', backref='user', lazy=True)
    else:
        username = ""
        email = ""
        password = ""

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)

    def __setattr__(self, name, value):
        """sets a password with md5 encryption"""
        if name == "password":
            value = md5(value.encode()).hexdigest()
        super().__setattr__(name, value)