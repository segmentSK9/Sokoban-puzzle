from collections import deque
from tkinter import *
from node import *
import time
"""
La classe Search permet de résoudre 
le jeu Sokoban en utilisant deux 
méthodes de recherche : breadthFirst, 
qui explore tous les nœuds de manière exhaustive, 
et Astar, qui utilise une heuristique pour optimiser
 la recherche. Les deux méthodes mettent à jour une 
 interface utilisateur Tkinter pour afficher l'avancement 
 des étapes de la recherche. La détection de blocages est
  également intégrée pour éviter 
de tomber dans des configurations de jeu non résolubles
"""
class Search:

    from collections import deque
from tkinter import *
from node import *

class Search:

    @staticmethod
    def breadthFirst(initial_node, window, deadlock_detection=False):
        # Check if the start element is the goal
        if initial_node.state.isGoal(Node.tab_stat):
            return initial_node.getPath(), 0
        elif deadlock_detection and initial_node.state.isDeadLock(Node.blockage_map):
            return None, -1 

        # Initialize the OPEN queue and CLOSED set
        open_queue = deque([initial_node])
        closed_set = set()
        closed_set.add(tuple(map(tuple, initial_node.state.grid)))  # Mark initial node as visited
        
        step = 0

        while open_queue:
            # Track the number of nodes at the current level
            nodes_at_current_level = len(open_queue)
            step += 1  # Increment step only once per level

            for _ in range(nodes_at_current_level):
                current = open_queue.popleft()

                # Check if the current node is the goal
                if current.state.isGoal(Node.tab_stat):
                    label = Label(window, text=f'*** Step {step} *** (Goal found)', bg='#c45242', fg='white')
                    label.pack()
                    window.update()
                    return current.getPath(), step  # Return the shortest path and step count

                # Generate successors
                successors = current.state.successorFunction(current)
                for child, move in successors:
                    child_grid_tuple = tuple(map(tuple, child.state.grid))

                    # Only enqueue child if it's not visited
                    if child_grid_tuple not in closed_set:
                        open_queue.append(child)
                        closed_set.add(child_grid_tuple)

        # If the goal is not found
        label = Label(window, text=f'*** Step {step} *** (Goal not found)', bg='#c45242', fg='white')
        label.pack()
        window.update()
        return None, -1


             
    @staticmethod
    def Astar(init_node, window, heuristic=1, deadlock_detection=False):
        # Check if the start element is the goal
        if init_node.state.isGoal(Node.tab_stat):
            return init_node.getPath(), 0 
        elif deadlock_detection:
            if init_node.state.isDeadLock(Node.blockage_map):
                return None, -1 
         
        init_node.setF(heuristic)
        # Create the OPEN priority queue and the CLOSED list
        open = deque([init_node])
        closed = list()
        step = 0
        while True:
            step += 1
            
            # Delete the last label if it exists
            try:
                label123.destroy()
            except:
                pass
            
            label123 = Label(window, text=f'*** Step {step} ***', bg='#c45242', fg='white')
            label123.pack()
            window.update()
            
            # Check if the OPEN queue is empty => goal not found
            if len(open) == 0:
                return None, -1
            
            # Sort the open list by the f value
            open = deque(sorted(list(open), key=lambda node: node.f))

            # Get the first element of the OPEN queue
            current = open.popleft()
            
            # Put the current node in the CLOSED list
            closed.append(current)

            # Check if the current node is the goal
            if current.state.isGoal(Node.tab_stat):
                label123.destroy()
                
                return current.getPath(), step 
            elif deadlock_detection:
                if current.state.isDeadLock(Node.blockage_map):
                    continue
            
            # Generate the successors of the current node
            successors = current.state.successorFunction(current)
            while len(successors) != 0:
                child, move = successors.popleft()
                child.setF(heuristic)

                # Check if the child is in the OPEN queue
                if child.state.grid in [node.state.grid for node in open]:
                    index = [node.state.grid for node in open].index(child.state.grid)
                    if child.f < open[index].f:
                        open[index] = child
                # Check if the child is not in CLOSED list
                elif child.state.grid not in [node.state.grid for node in closed]:
                    open.append(child)
                # If the child is in CLOSED list
                else:
                    index = [node.state.grid for node in closed].index(child.state.grid)
                    if child.f < closed[index].f:
                        closed.remove(closed[index])
                        open.append(child)
