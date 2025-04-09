# Projet IA Martin - Jessica

Ordre de lecture :
gamemodel => gamevieuw => gamecontroller

 Structure des DocString:

 1) Description globale de la fonction/classe
 2) Héritage
 3) Paramètre/argument de la fonction/classe (avec type)
 4) Valeurs retournées (avec type)
 5) Description des fonctionnalités supplémentaires de l'objet

Requirement:
- pytest: avec "pip install pytest" dans l'invite de commande

Lancer les jeux :

Deux options :
- Lancer main.py directement et choisir le jeu souhaité dans le menu
- Ou via le terminal, aller dans le dossier contenant le projet avec cd puis exécuter "python main.py"

Pour lancer un exemple d'entraînement, compiler directement le script "gamemodel.py"

Allumettes : 

Règles du jeu :
 À chaque tour, le joueur doit prendre 1 à 3 allumettes, et l'intelligence artificielle fera de même.
 Le joueur qui prendra la dernière allumette aura perdu la partie

Cubee :

Requirements:
- SQL Alchemy, peut-être installé avec la commande "pip install SQLAlchemy" dans le cmd

Règle du jeu :
But :
Posséder plus de cases que l’adversaire
Déroulement :
Deux joueurs s'affrontent sur un plateau carré d'une taille variable (5x5 cases par défaut).
Un joueur gagne des cases en se déplaçant dessus.
Au début de la partie, les joueurs commencent chacun dans un coin opposé du terrain. Chacun à leur tour, ils vont se déplacer d'une case (vers le haut, le bas, la gauche ou la droite). Un joueur ne peut pas se déplacer sur une case appartenant au joueur adverse ni sortir des limites du plateau.
Si un joueur arrive à faire un enclos (bloquer l’accès à certaines cases pour l’adversaire), les cases de l'enclos appartiennent automatiquement au joueur qui les a bloquées.
Le jeu s’arrête lorsqu’il ne reste plus de case libre.



