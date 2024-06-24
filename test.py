"""Lets test out some shit"""
# from flask import Flask, render_template, request, redirect, url_for
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
# from sqlalchemy import Integer, String, Float, Column, create_engine,ForeignKey



from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

import os

"""creating the database"""
# app = Flask(__name__)

engine = create_engine("sqlite:///Diseases.db", echo=True)
Base = declarative_base()

class Disease(Base):
    __tablename__ = "diseases"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    prescription = Column(String)
    health_tips = Column(String)

"""create the table"""
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

"""insert values into the table"""

disease1 = Disease(name="diabetes", prescriptionn="Metformin, 40grams", health_tips="Exercise regularly and train")
session.add(disease1)
session.commit()

diabetes = session.query(Disease).filter_by(name='Diabetes').first()
print(diabetes.health_tips)
session.close()



