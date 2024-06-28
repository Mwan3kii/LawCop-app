#!/usr/bin/python3
"""
Contains the class DBStorage
"""

import models
from models.reports import Report
from models.base_model import BaseModel, Base
from models.alerts import Alert
from models.user import User
from os import getenv
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, object_session

classes = {"Alert": Alert, "Report": Report, "User": User}


class DBStorage:
    """interaacts with the MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        LC_MYSQL_USER = getenv('LC_MYSQL_USER')
        LC_MYSQL_PWD = getenv('LC_MYSQL_PWD')
        LC_MYSQL_HOST = getenv('LC_MYSQL_HOST')
        LC_MYSQL_DB = getenv('LC_MYSQL_DB')
        LC_ENV = getenv('LC_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(LC_MYSQL_USER,
                                             LC_MYSQL_PWD,
                                             LC_MYSQL_HOST,
                                             LC_MYSQL_DB))
        if LC_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the current database session"""
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return (new_dict)

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def expunge(self, obj):
        """Expunge object from current session"""
        self.__session.expunge(obj)

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            object_session_instance = object_session(obj)
            if object_session_instance and object_session_instance is not self.__session:
                object_session_instance.expunge(obj)
        self.__session.delete(obj)

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()

    def get(self, cls, id):
        """
        Returns the object based on the class name and its ID, or
        None if not found
        """
        if cls not in classes.values():
            return None

        all_cls = self.all(cls)
        for value in all_cls.values():
            if (value.id == id):
                return value

        return None

    def count(self, cls=None):
        """
        count the number of objects in storage
        """
        all_class = classes.values()

        if not cls:
            count = 0
            for clas in all_class:
                count += len(self.all(clas).values())
        else:
            count = len(self.all(cls).values())

        return count
    
    def user_all(self, user_id, cls=None):
        """gets objects of users"""
        user = self.get(User, user_id)
        if not user:
            return None
        if cls is not None and cls not in classes.values():
            return None
        else:
            all_cls_objs = self.all(cls)
            user_cls_objs = []
            for obj in all_cls_objs.values():
                if getattr(obj, 'user_id', None) == user_id and isinstance(obj, cls):
                    user_cls_objs.append(obj)
        return user_cls_objs