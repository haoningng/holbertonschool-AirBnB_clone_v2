#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
import os


Base = object
if os.getenv('HBNB_TYPE_STORAGE') == "db":
    Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models"""
    storage_engine = os.getenv('HBNB_TYPE_STORAGE')

    if storage_engine == "db":
        id = Column(String(60), primary_key=True)
        created_at = Column(DateTime,
                            default=datetime.utcnow(),
                            nullable=False)
        updated_at = Column(DateTime,
                            default=datetime.utcnow(),
                            nullable=False)
    else:
        id = None
        created_at = None
        updated_at = None

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        if not kwargs:
            from models import storage
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        else:
            date_format = "%Y-%m-%dT%H:%M:%S.%f"
            for key, value in kwargs.items():
                if key != "__class__":
                    if key == "created_at" or key == "updated_at":
                        value = datetime.strptime(value, date_format)
                    setattr(self, key, value)

            identifier = {'id': str(uuid.uuid4()),
                          'created_at': datetime.now(),
                          'updated_at': datetime.now()
                          }

            for key, value in identifier.items():
                if key not in kwargs.keys():
                    setattr(self, key, value)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        if '_sa_instance_state' in dictionary.keys():
            del dictionary['_sa_instance_state']
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        return dictionary

    def delete(self):
        """delete the current instance from the storage"""
        from models import storage
        storage.delete(self)
