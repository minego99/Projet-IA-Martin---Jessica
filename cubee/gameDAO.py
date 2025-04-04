# -*- coding: utf-8 -*-
"""
Created on Fri Mar 28 10:06:11 2025

@author: martin
"""
from sqlalchemy.exc import IntegrityError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import Column, Integer, String, Float

class Base(DeclarativeBase):
    pass

engine = create_engine('sqlite:///cubee.db')
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
    id = Column(String, primary_key=True)
    up_value = Column(Float,nullable =True)
    down_value = Column(Float, nullable=True)
    left_value = Column(Float,nullable =True)
    right_value = Column(Float,nullable =True)

    def to_dto(self):
        """
        Conversion de la chaine de caractères vers un dictionnaire exploitable par le modèle
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
        """
        Conversion du dictionnaire généré par le modèle en une chaîne de caractères
        """
        return cls(
            id = data.get("state_id"),
            up_value = data.get('up_value'),
            down_value = data.get('down_value'),
            left_value = data.get('left_value'),
            right_value = data.get('right_value'),
            
        )
def get_Qline_by_state(state):
    """
    récupère une Qline en fonction d'un id fourni
    si la ligne n'existe pas, une nouvelle est crée immédiatement avec des poids initialisés à 0
    """
    new_line = SESSION.query(QLine).filter(QLine.id == state).first()
    print("querry for a line")
    if(new_line is None):
        print("adding line")
        new_line = QLine(id = state, up_value = 0, down_value = 0, left_value = 0, right_value = 0)
        SESSION.add(new_line)
        SESSION.commit()
        
    return new_line

def init_db():
    # Création des tables
    Base.metadata.create_all(engine)


def save_qline(Qline):
    """
    Save a user to a file
    @param user_dto: dict
    """
      
    try: 
        SESSION.add(QLine.from_dto(Qline))
        SESSION.commit()
    except IntegrityError:
        SESSION.rollback()  # Annule l'insertion en cas d'erreur
        existing_entry = SESSION.query(QLine).filter_by(id=Qline.get("state_id")).first()
        existing_entry.up_value = 0.0  # Modifier les valeurs si besoin
        existing_entry.down_value = 0.0
        SESSION.commit()
if __name__ =="__main__":
     init_db()
     debug = SESSION.query(QLine).all()
     print(len(debug))
     for val in debug:
         print(val.id)