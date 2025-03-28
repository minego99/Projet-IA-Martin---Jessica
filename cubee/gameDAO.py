# -*- coding: utf-8 -*-
"""
Created on Fri Mar 28 10:06:11 2025

@author: martin
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import Column, Integer, String

class Base(DeclarativeBase):
    pass

engine = create_engine('sqlite:///store.db')
# Création d'une session
Session = sessionmaker(bind=engine)
SESSION = Session()

class QLine (Base) :
    """
    Classe reprennant un état possible pour la partie
    
    attributs:
        - id (composé de: la position du premier joueur ; la position du deuxième joueur ; le numéro du joueur actuel ; la composition du terrain de jeu) (STR)
        - poids accordé lors du déplacement vers le haut (RÉEL)
        - poids accordé lors du déplacement vers le bas (RÉEL)
        - poids accordé lors du déplacement vers le gauche (RÉEL)
        - poids accordé lors du déplacement vers le droite (RÉEL)
        
    
    """
    __tablename__ = 'Qtable'
    id = Column(String)
    up_value = Column(String(50),nullable =True)
    down_value = Column(String(50),nullable =True)
    left_value = Column(String(50),nullable =True)
    right_value = Column(String(50),nullable =True)

    def to_dto(self):
        """
        Conversion de 
        """
        state = self.id.split(";")
        return {
            'state_id': self.id,
            'up_value' : self.up_value,
            'down_value': self.down_value,
            'left_value' : self.left_value,
            'right_value' : self.right_value
        }

    @classmethod
    def from_dto(cls, data: dict):
        return cls(
            id = ';'.join(data.get('player1_pos'),data.get('player2_pos'),data.get('player_turn'), data.get('grid')),
            up_value = data.get('up_value'),
            down_value = data.get('down_value'),
            left_value = data.get('left_value'),
            right_value = data.get('right_value'),
            
        )

def init_db():
    # Création des tables
    Base.metadata.create_all(engine)

def find_state_by_name(state):
    """
    On considère que l'état sera transformé dans le modèle
    @param user_name: str
    @return: dict
    """
    user = SESSION.query(QLine).filter(QLine.id == state).first()
    return user.to_dto() if user else None

def save_user(user_dto):
    """
    Save a user to a file
    @param user_dto: dict
    """
    SESSION.add(QLine.from_dto(user_dto))
    SESSION.commit()

if __name__ =="__main__":
     init_db()