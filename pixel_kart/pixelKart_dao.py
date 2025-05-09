import os

FILE_PATH = "pixel_kart/circuits.txt"

def get_all():
    """Retrieve all circuits from the file as a dictionary {name: str}."""
    circuits = {}
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "r", encoding="utf-8") as file:
            for line in file:
                name,circuit = line.split(":")
                if name:
                    circuits[name] = circuit
    return circuits

def get_by_name(name):
    """Retrieve a circuit by its name."""
    circuits = get_all()
    return circuits.get(name)

def save_circuit(name, string):
    """Save a new circuit to the file."""
    if not name:
        raise ValueError("Circuit name cannot be empty.")
    circuits = get_all()
    if name in circuits:
        raise ValueError(f"The circuit '{name}' already exists.")
    with open(FILE_PATH, "a", encoding="utf-8") as file:
        file.write(f"\n{name}:{string}")

def delete_circuit(name):
    """Delete a circuit by its name."""
    if not name:
        raise ValueError("Circuit name cannot be empty.")
    circuits = get_all()
    if name not in circuits:
        raise ValueError(f"The circuit '{name}' does not exist.")
    del circuits[name]
    with open(FILE_PATH, "w", encoding="utf-8") as file:
        for circuit_name in circuits:
            file.write(circuit_name + "\n")

def update_circuit(name, string):
    """Update the name of an existing circuit."""
    circuits = get_all()
    if name not in circuits:
        raise ValueError(f"The circuit '{name}' does not exist.")
    
    circuits[name] = string
    with open(FILE_PATH, "w", encoding="utf-8") as file:
        for circuit_name in circuits:
            file.write(circuit_name + "\n")
            
def get_circuit_grid(name):
    """
    Retourne la grille (2D) du circuit à partir de son nom.
    
    Arguments:
        name (str): nom du circuit
    
    Retourne:
        list[list[str]]: grille du circuit
    """
    encoded = get_by_name(name)
    if not encoded:
        raise ValueError(f"Circuit '{name}' introuvable.")
    
    # Nettoyage et découpage de la chaîne en lignes
    encoded = encoded.strip()
    rows = encoded.split(",")
    
    # Convertir chaque ligne en liste de caractères
    grid = [list(row) for row in rows]
    
    return grid

if( __name__ == "__main__"):
    print(get_all())