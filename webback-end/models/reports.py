#!/usr/bin/python
""" holds class City"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class Report(BaseModel, Base):
    """Representation of report """
    if models.storage_t == "db":
        __tablename__ = 'reports'
        report_id = Column(String(60), PrimaryKey=True, nullable=False)
        user_id = Column(String(60), ForeignKey('user.id'), nullable=False)
        crime_type = Column(String(50), nullable=False)
        description = Column(String(50), nullable=False)
        location = Column(String(50), nullable=False)
        date_reported = Column(Date, nullable=False)
        status = Column(String(20), default='pending')

    else:
        report_id = ""
        user_id = ""
        crime_type = ""
        description = ""
        location = ""
        date_reported = ""
        status = ""

    def __init__(self, *args, **kwargs):
        """initializes report"""
        super().__init__(*args, **kwargs)