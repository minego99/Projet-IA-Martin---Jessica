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

    Pour lancer le jeu, passer par le script main.
    Le main ouvre un éditeur de partie. Vous pouvez y choisir le circuit enregistré, si la partie doit se dérouler avec une IA ou pas (IA pas encore présente). 
    Ainsi que le nombre de tours prévus pour la partie. 

    Déroulement: 
        Le joueur commence sur un circuit prédéfini à la ligne d'arrivée. Chaque joueur (humain ou IA) joue à son tour, avec plusieurs actions possibles :
            - Accélérer (augmenter la vitesse de 1, avec un max de 2).
            - Freiner (diminuer la vitesse de 1, avec un minimum de -1).
            - Tourner à gauche/droite (changer l'orientation pour son accélération, par exemple : d’Est vers Nord ou Sud, ou encore de Sud vers Est ou Ouest).
            - attendre (le kart avance selon sa vitesse et dans sa direction actuelle)
        Les joueurs commencent avec une vitesse de 0 et une orientation vers l'Est.
        À chaque début de tour, le kart avance dans sa direction actuelle le nombre de cases correspondantes.
        Un tour est terminé lorsque le joueur passe correctement la ligne d'arrivée.
        Les informations des joueurs (vitesse, direction, tours réalisés) sont visibles durant la partie pour chaque joueur.
        L'alternance entre les joueurs se fait à chaque action.
    
    But: 
       Faire un certain nombre de tours de circuit (choisi à l'avance) et atteindre la ligne d'arrivée par le côté gauche avant l'autre joueur.
       La partie se termine une fois que tous les tours ont été effectués. Le joueur qui a fait le plus de tours (ou qui a réussi à franchir la ligne d'arrivée) gagne.

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
