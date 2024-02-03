#!/usr/bin/python3
"""This is the city class"""
import os
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from models.place import Place


class City(BaseModel, Base):
    """This is the class for City
    Attributes:
        state_id: The state id
        name: input name
    """

    __tablename__ = "cities"
    id = Column(String(60), nullable=False, primary_key=True)
    name = Column(String(128), nullable=False)
    state_id = Column(String(60), ForeignKey("states.id"), nullable=False) if os.getenv('HBNB_TYPE_STORAGE') == 'db' else ''
        "Place", cascade="all, delete, delete-orphan", backref="cities"
    )
