# Projet IA Martin - Jessica

Projet de programmation python contenant 3 jeux: les allumettes, cubee et pixelkart

## Lancement

Après avoir installé le nécessaire dans "Requirements.txt"
Éxécuter le script "main.py" et choisir un jeu dans le menu

## Usage

Allumettes : 

    Déroulement :
        À chaque tour, le joueur doit prendre 1 à 3 allumettes, et l'intelligence artificielle fera de même.
    
    But:
        Le joueur qui prendra la dernière allumette aura perdu la partie

Cubee :

    Déroulement:
        Deux joueurs s'affrontent sur un plateau carré d'une taille variable (5x5 cases par défaut).
        Un joueur gagne des cases en se déplaçant dessus.
        Au début de la partie, les joueurs commencent chacun dans un coin opposé du terrain. Chacun à leur tour, ils vont se déplacer d'une case (vers le haut, le bas, la gauche ou la droite). Un joueur ne peut pas se déplacer sur une case appartenant au joueur adverse ni sortir des limites du plateau.
        Si un joueur arrive à faire un enclos (bloquer l’accès à certaines cases pour l’adversaire), les cases de l'enclos appartiennent automatiquement au joueur qui les a bloquées.
        Le jeu s’arrête lorsqu’il ne reste plus de case libre.

    But :
        Posséder plus de cases que l’adversaire

PixelKart: 

    Déroulement: 
        Les 2 (ou 3) joueurs commencent sur un circuit prédifini sur la ligne d'arrivée. Chacun des joueurs (humain ou IA) joueront à leur tour, avec plusieurs actions à leur disposition. Les joueurs commencent avec une vitesse de 0 et une orientation vers l'Est. À chaque début de son tour, le kart avance dans sa direction le nombre de cases dans sa direction actuelle. Les joueurs peuvent:
            - accélerer (augmenter la vitesse de 1)
            - freiner (diminuer la vitesse de 1 avec un minimum de -1)
            - tourner à gauche/droite(changer son orientation pour son accélération ex: d'Est vers Nord ou Sud, ou encore de Sud vers Est ou Ouest). 
    But: 
        Le but est de faire un certain nombre de tours de circuit (choisi à l'avance) et d'atteindre la ligne d'arrivée par le côté gauche.

## Contribution

On fait de notre mieux, mais un coup de pousse est toujours apprécié

## Roadmap

Le projet Allumettes est complètement fini
Le projet Cubee est jouable, mais doit être réparé sur plusieurs aspects.
Le projet Pixelkart est encore en cours de construction

## TODO

- Les enclos de Cubee ne s'affichent pas et ne s'effectuent pas tout le temps
- le main ne peut pas lancer pixelkart
- pixelkart ne contient ni logique, ni retour visuel
- il n'y a pas de gestion de la base de données dans pixelkart
