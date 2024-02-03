#!/usr/bin/python3
"""This is the state class"""
from models.base_model import BaseModel
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String
import models
from models.city import City
import shlex
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class State(BaseModel):
    """This is the class for State
    Attributes:
        name: input name
    """

    __tablename__ = "states"
    id = Column(String(60), nullable=False, primary_key=True)
    name = Column(String(128), nullable=False)
    cities = relationship("City", cascade="all, delete, delete-orphan", backref="state")

    @property
    def cities(self):
        var = models.storage.all()
        lista = []
        result = []
        for key in var:
            city = key.replace(".", " ")
            city = shlex.split(city)
            if city[0] == "City":
                lista.append(var[key])
        for elem in lista:
            if elem.state_id == self.id:
                result.append(elem)
        return result
engine = create_engine("mysql+mysqldb://hbnb_dev:hbnb_dev_pwd/hbnb_dev_db@localhost")
Session = sessionmaker(engine)
