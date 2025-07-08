from copy import deepcopy
import numpy as np
from math import inf
import itertools
"""
a classe Node est une structure de données 
qui représente un état dans la recherche de solutions 
pour le jeu Sokoban. Chaque nœud contient des informations
sur l'état actuel du jeu ainsi que des liens vers d'autres nœuds (parents), 
permettant de reconstruire le chemin de solution.
"""
class Node:

    tab_stat = []
    blockage_map = []

    def __init__(self, sokoPuzzle, parent=None, move="", c=1):
        self.state = sokoPuzzle
        self.parent = parent
        if self.parent == None:
            self.g = 0
            self.moves = move
        else:
            self.g = self.parent.g + c
            self.moves = self.parent.moves + move
        self.f = self.g


    def getSolution(self):
        node = self
        solution = []
        while node:
            height = len(node.state.grid)
            width = len(node.state.grid[0])
            state = deepcopy(Node.tab_stat)
            for i, j in itertools.product(range(height), range(width)):
                if node.state.grid[i][j] == 'R':
                    if state[i][j] == ' ':
                        state[i][j] = 'R'
                    else:
                        state[i][j] = '.'
                elif node.state.grid[i][j] == 'B':
                    if state[i][j] == ' ':
                        state[i][j] = 'B'
                    else:
                        state[i][j] = '*'
            solution.append(state)
            node = node.parent
        solution = solution[::-1]
        return solution
    
    def setF(self, heuristic=1):
        heuristics = {1: self.heuristic1(),
                      2: self.heuristic2(),
                      3: self.heuristic3(),}
        self.g = self.g + heuristics[heuristic]
        
        
    def getPath(self):
        path = []
        node = self
        while node is not None:
            path.append(node)  
            node = node.parent  
        path.reverse()  
        return path

# Compte le nombre de caisses restantes qui ne sont pas dans les emplacements de stockage.    
    def heuristic1(self):
        tab_stat = np.array(Node.tab_stat)
        x_storage, y_storage = np.where(tab_stat == 'S')
        left_storage = len(x_storage)
        for x_pos, y_pos in zip(x_storage, y_storage):
            if self.state.grid[x_pos][y_pos] == 'B':
                left_storage -= 1
        return left_storage
#Calcule la distance minimale totale entre les caisses et les emplacements de stockage, en tenant compte des caisses déjà positionnées.
    def heuristic2(self):
        tab_stat = np.array(Node.tab_stat)
        x_storage, y_storage = np.where(tab_stat == 'S')
        grid = np.array(self.state.grid)
        B_indices_x, B_indices_y = np.where(grid == 'B')
        sum_distance = 0
        storage_left = len(x_storage)
        for b_x_pos, b_y_pos in zip(B_indices_x, B_indices_y):
            min_distance = +inf
            for s_x_pos, s_y_pos in zip(x_storage, y_storage):
                distance = abs(b_x_pos-s_x_pos) + abs(b_y_pos-s_y_pos)
                if distance == 0: storage_left -= 1
                if distance < min_distance:
                    min_distance = distance
            sum_distance += min_distance
        return sum_distance + 2 * storage_left

    def heuristic3(self):
        tab_stat = np.array(Node.tab_stat)
        x_storage, y_storage = np.where(tab_stat == 'S')
        grid = np.array(self.state.grid)
        B_indices_x, B_indices_y = np.where(grid == 'B')
        sum_distance = 0
        storage_left = len(x_storage)
        min_distance_br = +inf
        for b_x_pos, b_y_pos in zip(B_indices_x, B_indices_y):
            distance_br = abs(b_x_pos - self.state.robot_pos[0]) + abs(b_y_pos - self.state.robot_pos[1])
            if distance_br < min_distance_br:
                min_distance_br = distance_br
            min_distance = +inf
            for s_x_pos, s_y_pos in zip(x_storage, y_storage):
                distance = abs(b_x_pos - s_x_pos) + abs(b_y_pos - s_y_pos)
                if distance == 0: storage_left -= 1
                if distance < min_distance:
                    min_distance = distance
            sum_distance += min_distance
        return sum_distance + min_distance_br + 2 * storage_left

    
   