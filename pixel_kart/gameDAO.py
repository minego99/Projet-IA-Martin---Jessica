# -*- coding: utf-8 -*-
from sqlalchemy.exc import IntegrityError
from sqlalchemy import create_engine, Column, String, Float
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Base ORM
class Base(DeclarativeBase):
    pass

# Connexion à la base
engine = create_engine('sqlite:///pixelkart_model_3.db')
Session = sessionmaker(bind=engine)
SESSION = Session()

# Table QLine
class QLine(Base):
    """
    Classe Représentant une Qline, utilisée pour enregistrer l'état d'un kart
    attributs:
        - id, reprenant l'environnement immédiat du kart, ainsi que sa direction et sa vitesse (STR resessemblant à RRRRRRRRRWGRRRRGR;down;2)
        - actions values pour chacune des actions possible (accélerer, freiner, passer, tourner à gauche/droite) (INT)
    """
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
    """
    Encode l'état du joueur sous forme de chaîne, avec une vision en flèche inversée :
    d'abord la ligne la plus proche du joueur (5 cases), puis celle à 2 de distance (3 cases),
    puis celle à 3 (1 case), puis la case derrière.
    """

    # Vecteur directionnel principal
    dx, dy = 0, 0
    if direction == 'up':
        dx, dy = 0, -1
    elif direction == 'down':
        dx, dy = 0, 1
    elif direction == 'right':
        dx, dy = 1, 0
    elif direction == 'left':
        dx, dy = -1, 0

    # Vecteurs latéraux (gauche/droite)
    perp_dx, perp_dy = -dy, dx

    def safe_get(x, y):
        if 0 <= x < len(grid) and 0 <= y < len(grid[0]):
            return grid[x][y]
        return "X"

    vision = []

    # Ligne 1 (5 cases, juste devant le joueur)
    for offset in [-2, -1, 0, 1, 2]:
        px = x + dx + perp_dx * offset
        py = y + dy + perp_dy * offset
        vision.append(safe_get(px, py))

    # Ligne 2 (3 cases, deux cases devant)
    for offset in [-1, 0, 1]:
        px = x + 2 * dx + perp_dx * offset
        py = y + 2 * dy + perp_dy * offset
        vision.append(safe_get(px, py))

    # Ligne 3 (1 case, trois cases devant)
    px = x + 3 * dx
    py = y + 3 * dy
    vision.append(safe_get(px, py))

    # Case derrière
    px = x - dx
    py = y - dy
    vision.append(safe_get(px, py))
    # rrrrrrrRgr case juste devant
    # Format final (base de la flèche → pointe → arrière)
    encoded = "".join(vision) + f";{direction};{speed}"
    return encoded

# DAO Utilitaire

def get_Qline_by_state(state):
    """
    Crée une QLine en fonction de l'id de l'état entré
    Cré une nouvelle QLine si l'état n'a jamais été rencontré
    argument:
        - état de la partie actuel (STR)
        
    renvoie:
        - Qline adéquate avec les poids corresponants
    """
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
    """
    Ajoute une Qline sous forme de dictionnaire et essaye de la sauvegarder si son format est valide
    """
    try:
        qline = QLine.from_dto(qline_dict)
        SESSION.merge(qline)
        SESSION.commit()
        
        print(f"{qline.id[:30]:<30} | "
              f"{qline.accelerate:.2f} | "
              f"{qline.brake:.2f} | "
              f"{qline.turn_left:.2f} | "
              f"{qline.turn_right:.2f} | "
              f"{qline.do_nothing:.2f}")
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
    i=0
    for line in qlines:
        if(i < 1000):
            i+=1
            print(f"{line.id[:30]:<30} | "
                  f"{line.accelerate:.2f} | "
                  f"{line.brake:.2f} | "
                  f"{line.turn_left:.2f} | "
                  f"{line.turn_right:.2f} | "
                  f"{line.do_nothing:.2f}")
            
def clear_qtable():
    """
    Supprime toutes les entrées de la Q-table sans supprimer la table elle-même.
    Utilisable pour essayer un nouveau modèle sans devoir supprimer/déplacer la db
    """
    try:
        num_deleted = SESSION.query(QLine).delete()
        SESSION.commit()
        print(f"{num_deleted} lignes supprimées de la Q-table.")
    except Exception as e:
        SESSION.rollback()
        print("Erreur lors de la suppression des données :", e)

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
    #☺clear_qtable()
    print_all_qstates_summary()