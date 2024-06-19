from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Response(Base):
    __tablename__ = 'responses'
    id = Column(Integer, primary_key=True, autoincrement=True)
    query = Column(String, unique=True)
    response = Column(Text)

engine = create_engine('sqlite:///responses.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def save_response(query, response):
    new_response = Response(query=query, response=response)
    session.add(new_response)
    session.commit()

def get_saved_response(query):
    return session.query(Response).filter_by(query=query).first()
