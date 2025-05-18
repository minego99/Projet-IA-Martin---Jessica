# -*- coding: utf-8 -*-
from sqlalchemy.exc import IntegrityError
from sqlalchemy import create_engine, Column, String, Float
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Base ORM
class Base(DeclarativeBase):
    pass

# Connexion à la base
engine = create_engine('sqlite:///pixelkart.db')
Session = sessionmaker(bind=engine)
SESSION = Session()

# Table QLine
class QLine(Base):
    __tablename__ = 'QTable'
    id = Column(String, primary_key=True)  # représente l'état unique
    accelerate = Column(Float, nullable=True)
    brake = Column(Float, nullable=True)
    turn_left = Column(Float, nullable=True)
    turn_right = Column(Float, nullable=True)
    do_nothing = Column(Float, nullable=True)

    def to_dto(self):
        return {
            'state_id': self.id,
            'accelerate': self.accelerate,
            'brake': self.brake,
            'turn_left': self.turn_left,
            'turn_right': self.turn_right,
            'do_nothing': self.do_nothing
        }

    @classmethod
    def from_dto(cls, data):
        return cls(
            id=data.get("state_id"),
            accelerate=data.get("accelerate"),
            brake=data.get("brake"),
            turn_left=data.get("turn_left"),
            turn_right=data.get("turn_right"),
            do_nothing=data.get("do_nothing")
        )

# Fonction d'encodage de l'état

def encode_state(grid, x, y, direction, speed):
    dx, dy = 0, 0
    if direction == 'N':
        dx, dy = 0, -1
    elif direction == 'S':
        dx, dy = 0, 1
    elif direction == 'E':
        dx, dy = 1, 0
    elif direction == 'W':
        dx, dy = -1, 0

    def safe_get(x, y):
        if 0 <= y < len(grid) and 0 <= x < len(grid[0]):
            return grid[y][x]
        return "X"

    vision = []
    for dist in range(1, 5):
        for lateral in range(-dist + 1, dist):
            if dx == 0:
                vision.append(safe_get(x + lateral, y + dy * dist))
            else:
                vision.append(safe_get(x + dx * dist, y + lateral))

    vision.append(safe_get(x - dx, y - dy))
    encoded = "".join(vision) + f";{direction};{speed}"
    return encoded

# DAO Utilitaire

def get_Qline_by_state(state):
    line = SESSION.query(QLine).filter(QLine.id == state).first()
    if line is None:
        line = QLine(
            id=state,
            accelerate=0,
            brake=0,
            turn_left=0,
            turn_right=0,
            do_nothing=0
        )
        SESSION.add(line)
        SESSION.commit()
    return line

def save_qline(qline_dict):
    try:
        qline = QLine.from_dto(qline_dict)
        SESSION.merge(qline)
        SESSION.commit()
    except IntegrityError:
        SESSION.rollback()
def print_all_qstates_summary(limit=None):
    """
    Affiche un résumé de tous les états Q enregistrés dans la base de données.
    
    :param limit: Nombre maximum de lignes à afficher (None = pas de limite)
    """
    query = SESSION.query(QLine)
    if limit:
        query = query.limit(limit)
    
    qlines = query.all()
    
    print(f"{'State ID':<30} | Acc | Brk | Lft | Rgt | Nth")
    print("-" * 70)
    
    for line in qlines:
        print(f"{line.id[:30]:<30} | "
              f"{line.accelerate:.2f} | "
              f"{line.brake:.2f} | "
              f"{line.turn_left:.2f} | "
              f"{line.turn_right:.2f} | "
              f"{line.do_nothing:.2f}")

# Initialisation
Base.metadata.create_all(engine)

def init_db():
    Base.metadata.create_all(engine)

if __name__ == '__main__':
    example_q = {
        'state_id': '....G..G....;N;2',
        'accelerate': 1.0,
        'brake': 0.5,
        'turn_left': 0.2,
        'turn_right': 0.8,
        'do_nothing': 0.1
    }
    save_qline(example_q)
    print_all_qstates_summary()