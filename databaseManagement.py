# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 11:01:12 2025

@author: martin
"""
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

Base = declarative_base()
    
engine = create_engine('sqlite:///AIDataBase.db')


class AI_Model(Base):
    __tablename__ = 'AI_Model'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    Value_Function = relationship("Value_Function", back_populates="AI")
    learning_rate = Column(Integer)
    epsilon = Column(Integer)
    Value_Function = Column(String)

# # Création des tables
Base.metadata.create_all(engine)

# # Création de la session
Session = sessionmaker(bind=engine)
session = Session()

def creation_database():
    temp_dico = "{'win' : 1, 'lose' : -1, '1' : 0, '2' : 0, '3':0,'4':0,'5':0,'6':0,'7':0,'8':0,'9':0,'10':0,'11':0}"
    main_AI = AI_Model(name="Matches AI", learning_rate = 0.01, epsilon = 0.9, Value_Function = temp_dico)
    session.add(main_AI)
    session.commit()
    
  
   # print(type(session.query(AI_Model).filter_by(name= "Matches AI").first().Value_Function))
    # session.commit()
    # new_dico = {}
    
    # temp_value_function = session.query(AI_Model).filter_by(name= "Matches AI").first().Value_Function
    # for elem in temp_value_function:
    #    new_dico[elem.name] = elem.value * 15
    # print(new_dico)
    
    # new_dico["0"] = 654
    # new_dico["1"] = 5454
    # new_dico["2"] = 2313
    # new_dico["3"] = 1230
    # new_dico["4"] = 864
    # new_dico["5"] = 6454
    # new_dico["6"] = 54684
    # new_dico["7"] = 89486
    
    # for elem in new_dico.keys():
    #     print( "before mapping dico: ", temp_value_function[int(elem)-1].value)
    #     temp_value_function[int(elem)-1].value = new_dico[elem]
    #     temp_value_function[int(elem)-1].name = elem

    #     print("after mapping dico: " ,temp_value_function[int(elem)-1].value)
    # for elem in range(0,len(temp_value_function)):
    #     print("nom: ", temp_value_function[int(elem)].name, " valeur: ", temp_value_function[int(elem)].value)

        
"""
transformer un dictionnaire en table d'objets Value Function
dico = {'clé'('lose','11','10',...) = valeur(1,2,3,4,...)}
Value_Functions = [1,2,3,4,5,6,...].clé, .valeur
value_Function[clé (sauf pour le lose)].clé = dico[clé]
Value_Function[clé (sauf pour le lose)].valeur = dico[valeur]

"""    
if(__name__ == "__main__"):
   temp = session.query(AI_Model).filter_by(name = "Matches AI").first()
   print(temp.Value_Function)

    # for index in range(0, len(new_dico)):
    #     temp_value_function = session.query(AI_Model).filter_by(name= "Matches AI").first().Value_Function[index]
    #     print(temp_value_function)
        
    
    # for index in range(0,len(new_dico)):
    #     temp_value_function[index]= index
    
    # for vf in all_value_functions:
    #     print(f"ID: {vf.id}, Name: {vf.name}, Value: {vf.value}, AI ID: {vf.AI_id}")
