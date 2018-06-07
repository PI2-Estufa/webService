import datetime 
from sqlalchemy import create_engine, Column, Integer, Float, Unicode, Sequence, DateTime
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
    created_at = Column(DateTime, default=datetime.datetime.utcnow) 

Base.metadata.create_all(engine)


