# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 09:35:25 2025

@author: marti
"""
from gamemodel import Player,AI
from databaseManagement import AI_Model, Value_Function
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class New_AI(AI):
    def __init__(self, name):
        database_model = session.query(AI_Model).filter_by(name = "Matches AI").first()
