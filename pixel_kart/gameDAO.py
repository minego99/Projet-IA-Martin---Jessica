# -*- coding: utf-8 -*-
"""
DAO pour gérer les états du jeu PixelKart dans une base SQLite avec SQLAlchemy.
"""

from sqlalchemy.exc import IntegrityError
from sqlalchemy import create_engine, Column, String, Float
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Déclaration de la base
class Base(DeclarativeBase):
    pass

# Initialisation de la base de données
engine = create_engine('sqlite:///pixelkart.db')  # nom de la base
Session = sessionmaker(bind=engine)
SESSION = Session()

# Modèle représentant un état du jeu PixelKart
class KartState(Base):
    __tablename__ = 'kart_states'

    # L'état est représenté par une chaîne unique : "x;y;direction;grid"
    id = Column(String, primary_key=True)
    up_value = Column(Float, nullable=True)
    down_value = Column(Float, nullable=True)
    left_value = Column(Float, nullable=True)
    right_value = Column(Float, nullable=True)

    def to_dto(self):
        return {
            "state_id": self.id,
            "up_value": self.up_value,
            "down_value": self.down_value,
            "left_value": self.left_value,
            "right_value": self.right_value
        }

    @classmethod
    def from_dto(cls, data: dict):
        return cls(
            id=data.get("state_id"),
            up_value=data.get("up_value", 0),
            down_value=data.get("down_value", 0),
            left_value=data.get("left_value", 0),
            right_value=data.get("right_value", 0)
        )

# Création des tables
Base.metadata.create_all(engine)

# Récupère un état à partir d'un identifiant, le crée s'il n'existe pas
def get_kart_state_by_id(state_id):
    state = SESSION.query(KartState).filter(KartState.id == state_id).first()
    if state is None:
        state = KartState(id=state_id, up_value=0, down_value=0, left_value=0, right_value=0)
        SESSION.add(state)
        SESSION.commit()
    return state

# Sauvegarde ou met à jour un état
def save_kart_state(state_dict):
    try:
        state_instance = KartState.from_dto(state_dict)
        SESSION.merge(state_instance)
        SESSION.commit()
    except IntegrityError:
        SESSION.rollback()
        print(f"Erreur lors de la sauvegarde de l'état {state_dict.get('state_id')}")

if __name__ == "__main__":
    # Exemple d'utilisation
    test_state = {
        "state_id": "2;4;N;XXXX,XXXX,XXXX",
        "up_value": 0.5,
        "down_value": 1.5,
        "left_value": 0.0,
        "right_value": 2.0
    }

    save_kart_state(test_state)

    retrieved = get_kart_state_by_id("2;4;N;XXXX,XXXX,XXXX")
    print(retrieved.to_dto())