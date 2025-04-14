# -*- coding: utf-8 -*-
"""
Created on Mon Apr 14 08:41:23 2025

@author: martin
"""
from game_view import GameEditor
# A SUPPRIMER DES QUE LE MODELE EST IMPLEMENTE
import pixelKart_dao as dao

if __name__ == "__main__":
    new_game = GameEditor(dao.get_all())    
    new_game.mainloop()
    