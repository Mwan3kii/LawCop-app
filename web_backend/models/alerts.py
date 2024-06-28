#!/usr/bin/python3
""" holds class User"""

import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from hashlib import md5
from datetime import datetime


class Alert(BaseModel, Base):
    """Representation of a alerts """
    if models.storage_t == 'db':
        __tablename__ = 'alerts'
        report_id = Column(String(60), ForeignKey('reports.id'), nullable=True)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        message = Column(Text, nullable=False)
        read_status = Column(String(20), default='unread')

    else:
        report_id = ""
        user_id = ""
        message = ""
        read_status = ""

    def __init__(self, *args, **kwargs):
        """initializes alerts"""
        super().__init__(*args, **kwargs)