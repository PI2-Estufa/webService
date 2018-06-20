import datetime 
from sqlalchemy import create_engine, Column, Integer, String, Float, Unicode, Sequence, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine("postgresql://greenhouse:greenhouse@postgres:5432/greenhouse", echo=True)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class Temperature(Base):

    __tablename__ = 'temperature'

    id = Column(Integer, 
            Sequence('temperature_id_seq'), primary_key=True)
    value = Column(Float)
    created_date = Column(DateTime, default=datetime.datetime.utcnow) 
    unit = Column(Unicode(2), nullable=False)


class Humidity(Base):
    
    __tablename__ = 'humidity'

    id = Column(Integer,
            Sequence('humidity_id_seq'), primary_key=True)
    value = Column(Float)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)


class Ph(Base):

    __tablename__ = 'ph'

    id = Column(Integer, 
            Sequence('ph_id_seq'), primary_key=True)
    value = Column(Float)
    created_date = Column(DateTime, default=datetime.datetime.utcnow) 


class Ilumination(Base):
    
    __tablename__ = 'ilumination'

    id = Column(Integer,
            Sequence('ilumination_id_seq'), primary_key=True)
    value = Column(Boolean)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)


class WaterTemperature(Base):

    __tablename__ = 'waterTemperature'

    id = Column(Integer, 
            Sequence('waterTemperature_id_seq'), primary_key=True)
    value = Column(Float)
    created_date = Column(DateTime, default=datetime.datetime.utcnow) 
    unit = Column(Unicode(2), nullable=False)


class WaterLevel(Base):

    __tablename__ = 'water_level'

    id = Column(Integer, 
            Sequence('water_level_id_seq'), primary_key=True)
    value = Column(Integer)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)


class DrawerStatus(Base):

    __tablename__ = 'drawer_status'

    id = Column(Integer, 
            Sequence('drawer_status_id_seq'), primary_key=True)
    value = Column(Integer)
    created_date = Column(DateTime, default=datetime.datetime.utcnow) 

class Plant(Base):

    __tablename__ = 'plant'

    id = Column(Integer,
        Sequence('plant_id_seq'), primary_key=True)
    specie = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    observations = Column(String)

    def __init__(self, specie, created_at, observations):
        self.specie = specie
        self.created_at = created_at
        self.observations = observations

class User(Base):

    __tablename__ = 'users'

    id = Column(Integer, 
            Sequence('users_id_seq'), primary_key=True)
    username = Column(String)
    password = Column(String) 

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True
    
    @property
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.id)


Base.metadata.create_all(engine)