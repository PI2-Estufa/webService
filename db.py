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

Base.metadata.create_all(engine)