import numpy as np
from collections import deque
from copy import deepcopy
from node import Node
import time  
"""
SokobanPuzzle.py sert à créer une simulation du jeu Sokoban, en gérant 
la logique de déplacement et les interactions entre le robot et les caisses, permettant ainsi
 au joueur de résoudre des niveaux en poussant les caisses vers les emplacements appropriés.
 Aussi 
"""
class SokoPuzzle:

    def __init__(self, grid, robot_pos): 
        
        # initialisation du sokoban board
        self.grid = grid #une matrice 2D (tableau) représentant l'état actuel du puzzle.
        self.robot_pos = robot_pos 
                
        
        self.moves = ["U", "D", "L", "R"]        

    def isDeadLock(self, blockage_map):
        # Elle identifie les positions des cases de stockage ou celles où un blocage pourrait survenir.
        x_storage, y_storage = np.where(np.logical_or(np.array(blockage_map) == 'D', np.array(blockage_map) == 'L')) # x_storage and y_storage are 1D arrays of ints representing the indices of the storage cells in the puzzle board
        
        # Si un bloc B se trouve sur l'une de ces positions, la méthode retourne True, indiquant un blocage.
        for x_pos, y_pos in zip(x_storage, y_storage):
            if self.grid[x_pos][y_pos] == 'B':
                return True
        return False
    
    def isGoal(self, tab_stat): # vérifie si le puzzle est résolu
         # Récupère toutes les cellules de stockage
         # x_storage et y_storage sont des tableaux 1D contenant les indices des cellules de stockage
        x_storage, y_storage = np.where(np.array(tab_stat) == 'S') 
        
         # Vérifie si les cellules de stockage contiennent des blocs
        for x_pos, y_pos in zip(x_storage, y_storage):
            if self.grid[x_pos][y_pos] != 'B': #puzzle n'est pas résolu
                return False
        return True
    
    def successorFunction(self, parent_node):
        succs = deque() # Crée une deque pour stocker les successeurs
        for m in self.moves:# Pour chaque mouvement possib
            succState = deepcopy(self) # Crée une copie profonde de l'état actuel
            if succState.executeMove(m, Node.tab_stat):# Exécute le mouvement sur l'état copié
                new_node = Node(succState, parent=parent_node, move=m)# Crée un nouveau nœud pour l'état successeur
                succs.append((new_node, m))# Ajoute le nœud successeur et le mouvement à la deque
        return succs

    def executeMove(self, action, tab_stat): # Exécute le mouvement du robot et retourne le nouvel état du plateau
        if action == "U":
            return (self.up(tab_stat))
           
        if action == "D":
            return (self.down(tab_stat))
            
        if action == "L":
            return (self.left(tab_stat))
            
        if action == "R":
            return (self.right(tab_stat))
            

    def up(self, tab_stat):

        # Get the robot position
        robot_x, robot_y = self.robot_pos

        # Move the robot up: U => [-1, 0]
        robot_x = robot_x-1
        
        # Check if the robot is moving towards a block
        if self.grid[robot_x][robot_y] == 'B':
            # Moving the box
            box_x, box_y = robot_x-1, robot_y
            # If the robot is not pushing another box and is moving the box towards an empty space or storage
            if self.grid[box_x][box_y] != 'B' and (tab_stat[box_x][box_y] == ' ' or tab_stat[box_x][box_y] == 'S'):
                self.robot_pos = (robot_x, robot_y)
                self.grid[robot_x+1][robot_y] = ' ' 
                self.grid[robot_x][robot_y] = 'R'
                self.grid[box_x][box_y] = 'B'
                return True            
                
        else: # The robot is moving towards an empty space, a storage or a wall
            if tab_stat[robot_x][robot_y] == ' ' or tab_stat[robot_x][robot_y] == 'S':
                self.robot_pos = (robot_x, robot_y)
                self.grid[robot_x+1][robot_y] = ' ' 
                self.grid[robot_x][robot_y] = 'R'                
                return True

        return False

    def down(self, tab_stat):

        # Get the robot position
        robot_x, robot_y = self.robot_pos

        # Move the robot down: D => [1, 0]
        robot_x = robot_x+1

        # Check if the robot is moving towards a block
        if self.grid[robot_x][robot_y] == 'B':
            # Moving the box
            box_x, box_y = robot_x+1, robot_y
            # If the robot is not pushing another box and is moving the box towards an empty space or storage
            if self.grid[box_x][box_y] != 'B' and (tab_stat[box_x][box_y] == ' ' or tab_stat[box_x][box_y] == 'S'):
                self.robot_pos = (robot_x, robot_y)
                self.grid[robot_x-1][robot_y] = ' ' 
                self.grid[robot_x][robot_y] = 'R'
                self.grid[box_x][box_y] = 'B'
                return True
                
        else: # The robot is moving towards an empty space, a storage or a wall
            if tab_stat[robot_x][robot_y] == ' ' or tab_stat[robot_x][robot_y] == 'S':
                self.robot_pos = (robot_x, robot_y)
                self.grid[robot_x-1][robot_y] = ' '
                self.grid[robot_x][robot_y] = 'R'                
                return True

        return False
            
    def left(self, tab_stat):

        # Get the robot position
        robot_x, robot_y = self.robot_pos

        # Move the robot left: L => [0, -1]
        robot_y = robot_y-1

        # Check if the robot is moving towards a block
        if self.grid[robot_x][robot_y] == 'B':
            # Moving the box
            box_x, box_y = robot_x, robot_y-1
            # If the robot is not pushing another box and is moving the box towards an empty space or storage
            if self.grid[box_x][box_y] != 'B' and (tab_stat[box_x][box_y] == ' ' or tab_stat[box_x][box_y] == 'S'):
                self.robot_pos = (robot_x, robot_y)
                self.grid[robot_x][robot_y+1] = ' ' 
                self.grid[robot_x][robot_y] = 'R'
                self.grid[box_x][box_y] = 'B'
                return True
                
        else: # The robot is moving towards a space, a storage or a wall
            if tab_stat[robot_x][robot_y] == ' ' or tab_stat[robot_x][robot_y] == 'S':
                self.robot_pos = (robot_x, robot_y)
                self.grid[robot_x][robot_y+1] = ' ' 
                self.grid[robot_x][robot_y] = 'R'                
                return True

        return False

    def right(self, tab_stat):

        # Get the robot position
        robot_x, robot_y = self.robot_pos

        # Move the robot right: R => [0, 1]
        robot_y = robot_y+1

        # Check if the robot is moving towards a block
        if self.grid[robot_x][robot_y] == 'B':
            # Moving the box
            box_x, box_y = robot_x, robot_y+1
            # If the robot is not pushing another box and is moving the box towards an empty space or storage
            if self.grid[box_x][box_y] != 'B' and (tab_stat[box_x][box_y] == ' ' or tab_stat[box_x][box_y] == 'S'):
                self.robot_pos = (robot_x, robot_y)
                self.grid[robot_x][robot_y-1] = ' ' 
                self.grid[robot_x][robot_y] = 'R'
                self.grid[box_x][box_y] = 'B'
                return True

                
        else: # The robot is moving towards an empty space, a storage or a wall
            if tab_stat[robot_x][robot_y] == ' ' or tab_stat[robot_x][robot_y] == 'S':
                self.robot_pos = (robot_x, robot_y)
                self.grid[robot_x][robot_y-1] = ' ' 
                self.grid[robot_x][robot_y] = 'R'                
                return True

        return False 

    



            
                






    
