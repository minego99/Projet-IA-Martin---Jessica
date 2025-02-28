# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 11:01:12 2025

@author: martin
"""
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from gamemodel import Player, AI



Base = declarative_base()
    
engine = create_engine('sqlite:///AIDataBase.db')


class AI_Model(Base):
    __tablename__ = 'AI_Model'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    Value_Function = relationship("Value_Function", back_populates="AI")
    learning_rate = Column(Integer)
    epsilon = Column(Integer)

class Value_Function(Base):
    __tablename__ = 'Value_Function'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    value = Column(Integer)
    AI_id = Column(Integer, ForeignKey('AI_Model.id'))
    AI = relationship("AI_Model", back_populates="Value_Function")

# # Création des tables
Base.metadata.create_all(engine)


# # Création de la session
Session = sessionmaker(bind=engine)
session = Session()

def creation_database():
    
    main_AI = AI_Model(name="Matches AI", learning_rate = 0.01, epsilon = 0.9)
    session.add(main_AI)
    
    lose_value = Value_Function(name="1",value = -1, AI =main_AI)
    value_2 = Value_Function(name="2",value = 0, AI =main_AI)
    value_3 = Value_Function(name="3",value = 0, AI =main_AI)
    value_4 = Value_Function(name="4",value = 0, AI =main_AI)
    value_5 = Value_Function(name="5",value = 0, AI =main_AI)
    value_6 = Value_Function(name="6",value = 0, AI =main_AI)
    value_7 = Value_Function(name="7",value = 0, AI =main_AI)
    value_8 = Value_Function(name="8",value = 0, AI =main_AI)
    value_9 = Value_Function(name="9",value = 0, AI =main_AI)
    value_10 = Value_Function(name="10",value = 0, AI =main_AI)
    value_11 = Value_Function(name="11",value = 0, AI =main_AI)
    win_value = Value_Function(name="12",value = 1, AI =main_AI)
    
    session.add_all([lose_value, value_2, value_3, value_4, value_5, value_6, value_7, value_8, value_9, value_10, value_11, win_value])
    
    session.commit()

if __name__ == "__main__":
    
    new_AI = AI("test")
    random_AI = Player("Random")
    
    
    print(session.query(Value_Function).filter_by(name = "win").first().name)
    print(session.query(AI_Model).count())
    session.commit()
    
    # for vf in all_value_functions:
    #     print(f"ID: {vf.id}, Name: {vf.name}, Value: {vf.value}, AI ID: {vf.AI_id}")
