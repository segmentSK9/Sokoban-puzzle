from tkinter import *
import itertools
from search import Search
from sokobanPuzzle import *
from node import *
import time

board1 = [['O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'S', ' ', 'B', ' ', 'O'],
        ['O', ' ', 'O', 'R', ' ', 'O'],
        ['O', ' ', ' ', ' ', ' ', 'O'],
        ['O', ' ', ' ', ' ', ' ', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O']]

board2 = [['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'O'],
        ['O', ' ', ' ', ' ', ' ', ' ', 'R', ' ', 'O'],
        ['O', ' ', ' ', 'O', 'O', 'O', ' ', ' ', 'O'],
        ['O', ' ', ' ', ' ', ' ', 'O', 'S', ' ', 'O'],
        ['O', ' ', ' ', ' ', ' ', ' ', 'O', ' ', 'O'],
        ['O', ' ', ' ', 'B', ' ', ' ', 'O', ' ', 'O'],
        ['O', ' ', ' ', ' ', ' ', ' ', 'O', ' ', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O']]

board3 = [['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', ' ', ' ', ' ', 'O', ' ', ' ', 'O'],
        ['O', ' ', ' ', 'B', 'R', ' ', ' ', 'O'],
        ['O', ' ', ' ', ' ', 'O', 'B', ' ', 'O'],
        ['O', 'O', 'O', 'O', 'O', ' ', 'S', 'O'],
        ['O', 'O', 'O', 'O', 'O', ' ', 'S', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O']]

board4 = [['O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', ' ', ' ', 'O', 'O', 'O'],
        ['O', 'O', ' ', ' ', 'O', 'O', 'O'],
        ['O', 'O', ' ', '*', ' ', ' ', 'O'],
        ['O', 'O', 'B', 'O', 'B', ' ', 'O'],
        ['O', ' ', 'S', 'R', 'S', ' ', 'O'],
        ['O', ' ', ' ', ' ', ' ', 'O', 'O'],
        ['O', 'O', 'O', ' ', ' ', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O']]

board5 = [['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'S', 'O', ' ', ' ', 'O', 'O'],
        ['O', ' ', ' ', ' ', ' ', 'B', ' ', 'O', 'O'],
        ['O', ' ', 'B', ' ', 'R', ' ', ' ', 'S', 'O'],
        ['O', 'O', 'O', ' ', 'O', ' ', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'B', 'O', ' ', 'O', 'O', 'O'],
        ['O', 'O', 'O', ' ', ' ', 'S', 'O', 'O', 'O'],
        ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O']]


#-------------------------------------------------------      Gui_class (pour l'interface de level)     ---------------------------------------------------------------------------------------


class Gui:
    def __init__(self, board, search_algo, deadlock_detection, type ="watch", num_step_level = 0):  # passer comme paremetre le nom de search_algo, si avec detection de deadlock ou pas (deadlock_detection) et le type de jeux, et le nombre minimal de step pour ce niveau(each one of them is declared manualy,(pour le type de jeux "play"))
        self.board = board
        self.height = len(board)
        self.width = len(board[0])
        self.window = Tk()
        self.window.title("Sokoban")
        self.canvas = Canvas(self.window, width=32*self.width, height=32*self.height)
        self.canvas.pack()
        self.search_algo = search_algo
        self.final_steps = False
        self.legnth_solution = 0
        self.num_steps = 0
        self.deadlock_detection = deadlock_detection
        self.type = type
        self.num_step_level = num_step_level
        
        
        
        #make a button to close the window
        self.button = Button(self.window, text="Exit", padx=10, bg='#263D42', pady=4, command=self.close)
        self.button.pack(side=RIGHT)
        
        # make a button to back to the level
        self.button = Button(self.window, text="Back", padx=10, bg='#263D42', pady=4, command=self.Back)
        self.button.pack(side=LEFT)
        
        if self.type == "watch":
            # make a button to start the search
            self.button = Button(self.window, text="Start", padx=10, bg='#263D42', pady=4, command=self.start)
            self.button.pack()

                
        
        
        # vider Node.blockage_map pour si l'utilsateur a fait le button 'back' aprés a rentrer dans le level
        Node.blockage_map = [] 
        self.draw_board()
        
        self.window.eval('tk::PlaceWindow . center')
        self.window.mainloop()

    def start(self):
        show_solution(self, self.board, self.search_algo, self.deadlock_detection, self.window)

    def close(self):
        self.window.destroy()
        
    def Back(self):
        self.window.destroy()
        Level(self.search_algo, self.deadlock_detection, type=self.type)

    def draw_board(self,final_steps=False):
        # recuperer les photos
        self.obstacle = PhotoImage(file="images/obs.png")
        self.vide = PhotoImage(file="images/floor.png")
        self.cible = PhotoImage(file="images/goal1.png")
        self.robot = PhotoImage(file="images/player.png")
        self.bloc = PhotoImage(file="images/box.png")
        self.blocible = PhotoImage(file="images/boxg.png")
        self.DeadCoin = PhotoImage(file="images/DeadCoin1.png")
        self.DeadLigne = PhotoImage(file="images/DeadLigne1.png")

        for i, j in itertools.product(range(self.height), range(self.width)): # placer les photos sur le window
            if self.board[i][j] == 'O':
                self.canvas.create_image(32*j, 32*i, anchor=NW, image=self.obstacle)
            elif self.board[i][j] == 'S':
                self.canvas.create_image(32*j, 32*i, anchor=NW, image=self.vide)
                self.canvas.create_image(32*j, 32*i, anchor=NW, image=self.cible)
            elif self.board[i][j] == 'B':
                self.canvas.create_image(32*j, 32*i, anchor=NW, image=self.bloc)
            elif self.board[i][j] == 'R':
                self.canvas.create_image(32*j, 32*i, anchor=NW, image=self.vide)
                self.canvas.create_image(32*j, 32*i, anchor=NW, image=self.robot)
            elif self.board[i][j] == '*':
                self.canvas.create_image(32*j, 32*i, anchor=NW, image=self.blocible)
            elif self.board[i][j] == '.':
                self.canvas.create_image(32*j, 32*i, anchor=NW, image=self.vide)
                self.canvas.create_image(32*j, 32*i, anchor=NW, image=self.robot)
            else:
                self.canvas.create_image(32*j, 32*i, anchor=NW, image=self.vide)
                
            # tester si la case est une deadlock coin ou line par tester dans la matrice blockage_map
            # tester si blockage_map est declarer ou pas encore
            
            try: # on a fait la notion 'try-except' pour si l'utilisateur a pas utiliser la detection de deadlock, ou si il a utilisé mais cet itération c'est la premiere itération donc on ne draw pas les Deadlock(on l'affiche seulement dans la periode de solution) 
                if self.deadlock_detection: 
                    if Node.blockage_map[i][j] == 'D':
                        self.canvas.create_image(32*j, 32*i, anchor=NW, image=self.DeadCoin)
                    elif Node.blockage_map[i][j] == 'L':
                        self.canvas.create_image(32*j, 32*i, anchor=NW, image=self.DeadLigne)
            except:
                pass
        
        if self.final_steps: # si cet itéraion est la derniere, donc on fait des messages
            if self.deadlock_detection:
                self.label = Label(self.window, text="L'algorithme de "+ self.search_algo + " avec detection de deadlock : ", bg='green', fg='white')
            else:
                 self.label = Label(self.window, text="L'algorithme de "+ self.search_algo + " sans detection de deadlock : ", bg='green', fg='white')
                 self.label.pack()
            # make a label to show the number of steps de l'algorithme
            self.label = Label(self.window, text="Nombre de steps utilisé par cet algorithme : " + str(self.num_steps), bg='#FCCD2A', fg='black')
            self.label.pack()
          
            # make a label to show the number of steps necessaire pour resoudre le probleme
            self.label = Label(self.window, text="Nombre de steps minimum pour gagner est : " + str(self.legnth_solution), bg='#FCCD2A', fg='black')
            self.label.pack()
                 
    def update_board(self, board, final_steps=False, legnth_solution=0, num_steps=0):
        self.final_steps = final_steps
        self.legnth_solution = legnth_solution
        self.num_steps = num_steps
        
        self.board = board
        self.canvas.delete("all")
        self.draw_board()
        self.window.update()   
        return
        
#--------------------------------------------------------         start_game_class (la premeire page de jeux)        ---------------------------------------------------------------------------------------


class start_game_class:
    def __init__(self):
        self.window = Tk()
        self.window.title("Sokoban")
        self.canvas = Canvas(self.window, width=297, height=297, bg='#004d00')  # Set a dark green background color
        self.canvas.pack()

        # Draw an aesthetically pleasing text
        self.text = self.canvas.create_text(148, 50, text="SOKOBAN", fill="#FFCC00", font=("Helvetica", 24, "bold italic"))

        # Create a circular button
        self.button_radius = 30  # Adjust the size of the circle
        self.button_x = 148  # Centered horizontally
        self.button_y = 148  # Centered vertically

        # Draw the circle
        self.circle = self.canvas.create_oval(self.button_x - self.button_radius, 
                                               self.button_y - self.button_radius, 
                                               self.button_x + self.button_radius, 
                                               self.button_y + self.button_radius, 
                                               fill='#FFCC00', outline='')

        # Create the start text inside the circle
        self.start_text = self.canvas.create_text(self.button_x, self.button_y, text="Start", fill="black", font=("Arial", 12))

        # Bind the circle to the start_game method
        self.canvas.tag_bind(self.circle, '<Button-1>', self.start_game)

        self.window.eval('tk::PlaceWindow . center')
        self.window.mainloop()

    def start_game(self, event):
        self.window.destroy()
        search_method()
#--------------------------------------------------------------------         search_method class(pour choisir algorithme de recherche)        ---------------------------------------------------------------------------------------
    

class search_method: 
    def __init__(self):
        self.window = Tk()
        self.window.title("Sokoban")
        self.canvas = Canvas(self.window, width=400, height=400, bg='#004d00')  # Dark green background
        self.canvas.pack()

        # Make a button Exit
        self.button_exit = Button(self.window, text="Exit", padx=5, bg='#537365', pady=2, command=self.Exit)
        button_exit_canvas = self.canvas.create_window(350, 20, anchor="nw", window=self.button_exit)

        # Add a text label to the window
        #self.label = Label(self.window, text="Choose a search method:", bg='#537365', fg='white', font=("Arial", 18))
        #self.label.config(padx=3, pady=2, borderwidth=2)
        #label_canvas = self.canvas.create_window(20, 60, anchor="nw", window=self.label)

        # Make buttons with grey background
        button_bg_color = '#537365'  # Grey color for buttons

        # Make a button to start the game (Breadth First)
        self.button_bfs = Button(self.window, text="BFS", padx=5, bg=button_bg_color, fg='white', font=("Arial", 13), pady=1, command=self.BFS)
        button_bfs_canvas = self.canvas.create_window(200, 130, anchor="center", window=self.button_bfs)  # Centered

        # Make a button for Astar avec heuristic 1
        self.button_astar1 = Button(self.window, text="A* avec h1", padx=5, bg=button_bg_color, fg='white', font=("Arial", 13), pady=1, command=self.Astar1)
        button_astar1_canvas = self.canvas.create_window(200, 170, anchor="center", window=self.button_astar1)  # Centered

        # Other Astar buttons with the same grey background
        self.button_astar2 = Button(self.window, text="A* avec h2", padx=5, bg=button_bg_color, fg='white', font=("Arial", 13), pady=1, command=self.Astar2)
        button_astar2_canvas = self.canvas.create_window(200, 210, anchor="center", window=self.button_astar2)  # Centered

        self.button_astar3 = Button(self.window, text="A* avec h3", padx=5, bg=button_bg_color, fg='white', font=("Arial", 13), pady=1, command=self.Astar3)
        button_astar3_canvas = self.canvas.create_window(200, 250, anchor="center", window=self.button_astar3)  # Centered

        # Make a check box to choose if we want to use deadlock detection or not
        self.var = IntVar()
        self.check = Checkbutton(self.window, text="Avec detection de deadlock", variable=self.var, bg='#003161', font=("Arial", 13))
        self.check.config(padx=5, pady=1, borderwidth=2)
        check_canvas = self.canvas.create_window(70, 290, anchor="nw", window=self.check)

        self.window.eval('tk::PlaceWindow . center')
        self.window.mainloop()

    def Exit(self):
        self.window.destroy()
        
    def BFS(self):
        self.window.destroy()
        if self.var.get() == 1:
            deadlock_detection = True
        else:
            deadlock_detection = False
        Level("BFS", deadlock_detection, "watch")
    
    def Astar1(self):
        self.window.destroy()
        if self.var.get() == 1:
            deadlock_detection = True
        else:
            deadlock_detection = False
        Level("Astar,heuristic1", deadlock_detection, "watch")
        
    def Astar2(self):
        self.window.destroy()
        if self.var.get() == 1:
            deadlock_detection = True
        else:
            deadlock_detection = False
        Level("Astar,heuristic2", deadlock_detection, "watch")
        
    def Astar3(self):
        self.window.destroy()
        if self.var.get() == 1:
            deadlock_detection = True
        else:
            deadlock_detection = False
        Level("Astar,heuristic3", deadlock_detection, "watch")
#--------------------------------------------------------------------         Level class(pour choisir le level)        ---------------------------------------------------------------------------------------
       
class Level:
    def __init__(self, search_algo="BFS", deadlock_detection=False, type="watch"):
        self.window = Tk()
        self.window.title("Sokoban")
        self.canvas = Canvas(self.window, width=400, height=400, bg='#004d00')  # Dark green background
        self.canvas.pack()
        
        self.search_algo = search_algo
        self.deadlock_detection = deadlock_detection
        self.type = type
        
        # Make a button Back
        self.button_back = Button(self.window, text="Back", padx=5, bg='#537365', pady=2, command=self.Back)
        button_back_canvas = self.canvas.create_window(20, 20, anchor="nw", window=self.button_back)

        # Make a button Exit
        self.button_exit = Button(self.window, text="Exit", padx=5, bg='#537365', pady=2, command=self.Exit)
        button_exit_canvas = self.canvas.create_window(350, 20, anchor="nw", window=self.button_exit)

        # Create buttons for levels with red bourgeois style
        level_buttons = []
        for i in range(1, 6):
            button = Button(self.window, text=f"Level {i}", padx=20, bg='#800000', pady=10, font=("Arial", 13), command=getattr(self, f'level{i}'))
            level_buttons.append(button)

        # Position the buttons in the middle of the canvas
        for index, button in enumerate(level_buttons):
            button_canvas = self.canvas.create_window(200, 70 + index * 60, anchor="center", window=button)  # Centered horizontally

        self.window.eval('tk::PlaceWindow . center')
        self.window.mainloop()

    def Back(self):
        self.window.destroy()
        if self.type == "watch":
            search_method()
        
    def Exit(self):
        self.window.destroy()
        
    def level1(self):
        self.window.destroy()
        Gui(board1, self.search_algo, self.deadlock_detection, self.type, 4)
        
    def level2(self):
        self.window.destroy()
        Gui(board2, self.search_algo, self.deadlock_detection, self.type, 29)
    
    def level3(self):
        self.window.destroy()
        Gui(board3, self.search_algo, self.deadlock_detection, self.type, 33)
    
    def level4(self):
        self.window.destroy()
        Gui(board4, self.search_algo, self.deadlock_detection, self.type, 30)
        
    def level5(self):
        self.window.destroy()
        Gui(board5, self.search_algo, self.deadlock_detection, self.type, 25)

#--------------------------------------------------------------------         create_initial_node Fonction (pour creer le noeud initial)       ---------------------------------------------------------------------------------------
    
def create_initial_node(board=None, type='watch'):        
        
        height = len(board)
        width = len(board[0])
                
        # deviser le tableau sur deux, un dynamique et un statique
        grid = [['']*width for _ in range(height)]
        tab_stat = [['']*width for _ in range(height)]
        blockage_map = [['']*width for _ in range(height)] # initialiser la variable
        
        for i, j in itertools.product(range(height), range(width)):
            if board[i][j] == 'R':
                robot_pos = (i, j) 
                grid[i][j] = 'R'
                tab_stat[i][j] = ' '
            elif board[i][j] == 'B':
                grid[i][j] = 'B'
                tab_stat[i][j] = ' '
            elif board[i][j] == 'S' or board[i][j] == 'O' or board[i][j] == ' ':
                grid[i][j] = ' '   
                tab_stat[i][j] = board[i][j]         
            elif board[i][j] == '*':
                grid[i][j] = 'B'
                tab_stat[i][j] = 'S'
            else: # self.board[i][j] == '.'
                robot_pos = (i, j) 
                grid[i][j] = 'R'
                tab_stat[i][j] = 'S'

        Node.tab_stat = tab_stat # Create the static board 
        
        # remplire blockage_map avec D dans les coins bloqué
        for i, j in itertools.product(range(height), range(width)):
            if(tab_stat[i][j] == ' ' and tab_stat[i][j-1] == 'O' and tab_stat[i-1][j] == 'O') or (tab_stat[i][j] == ' ' and tab_stat[i][j+1] == 'O' and tab_stat[i-1][j] == 'O') or (tab_stat[i][j] == ' ' and tab_stat[i][j-1] == 'O' and tab_stat[i+1][j] == 'O') or (tab_stat[i][j] == ' ' and tab_stat[i][j+1] == 'O' and tab_stat[i+1][j] == 'O'):
                blockage_map[i][j] = 'D'
            else:
                blockage_map[i][j] = ' '
                
        
        # remplire blockage_map avec L ou il existe des deadlocks lineaires
        for i, j in itertools.product(range(height), range(width)):
            
            if blockage_map[i][j] == 'D':
                # verifier quel coin est bloqué de les 4 coins
                # enft on verifier just deux coins (top gauche et bottom droit) et pour chaque coin on verifer vertical et horizontal
                
                # on commence avec le coin top gauche
                if tab_stat[i][j-1] == 'O' and tab_stat[i-1][j] == 'O':
                    
                    # verifier si il existe un deadlock lineaire en horizontal
                    deadlock_line = False
                    for k in range(j+1, width):
                        if blockage_map[i][k] == 'D':
                            deadlock_line = True
                            break
                        elif Node.tab_stat[i][k] != ' ' or Node.tab_stat[i-1][k] != 'O':
                            deadlock_line = False
                            break
                    #fin de boucle
                    if deadlock_line:
                        for k in range(j+1, k):
                            blockage_map[i][k] = 'L'
                    
                    # verifier si il existe un deadlock lineaire en vertical
                    deadlock_line = False        
                    for k in range(i+1, height):
                        if blockage_map[k][j] == 'D':
                            deadlock_line = True
                            break
                        elif Node.tab_stat[k][j] != ' ' or Node.tab_stat[k][j-1] != 'O':
                            deadlock_line = False
                            break
                    if deadlock_line:
                        for k in range(i+1, k):
                            blockage_map[k][j] = 'L'
                        
                # et maintenent avec le coin bottom droit            
                elif tab_stat[i][j+1] == 'O' and tab_stat[i+1][j] == 'O':
                    deadlock_line = False
                    for k in range(j-1, 0, -1):
                        if blockage_map[i][k] == 'D':
                            deadlock_line = True
                            break
                        elif Node.tab_stat[i][k] != ' ' or Node.tab_stat[i+1][k] != 'O':
                            deadlock_line = False
                            break
                    if deadlock_line:
                        for k in range(j-1, k, -1):
                            blockage_map[i][k] = 'L'
                    
                    deadlock_line = False
                    for k in range(i-1, 0, -1):
                        if blockage_map[k][j] == 'D':
                            deadlock_line = True
                            break
                        elif Node.tab_stat[k][j] != ' ' or Node.tab_stat[k][j+1] != 'O':
                            deadlock_line = False
                            break
                    if deadlock_line:
                        for k in range(i-1, k, -1):
                            blockage_map[k][j] = 'L'
                            
        Node.blockage_map = blockage_map # Create the deadlock board
        sokoPuzzle = SokoPuzzle(grid, robot_pos)
        initial_node = Node(sokoPuzzle)
        if type == 'watch':
            return initial_node # Return the initial node
       
            


#--------------------------------------------------------------------         show_solution Function(pour commence la recherche)       ---------------------------------------------------------------------------------------

def show_solution(gui, board, search_algo, deadlock_detection, window):
    initial_node = create_initial_node(board=board)  # Create the initial node
    match search_algo:
        case 'BFS':
            goal_path, num_steps  = Search.breadthFirst(initial_node, window, deadlock_detection)
        case 'Astar,heuristic1':
            goal_path, num_steps  = Search.Astar(initial_node, window, 1, deadlock_detection)
        case 'Astar,heuristic2':
            goal_path, num_steps = Search.Astar(initial_node, window, 2, deadlock_detection)
        case 'Astar,heuristic3':
            goal_path, num_steps  = Search.Astar(initial_node, window, 3, deadlock_detection)
        case 'Astar,heuristic4':
            goal_path, num_steps  = Search.Astar(initial_node, window, 4, deadlock_detection)

    if goal_path:
        goal_node = goal_path[-1]  # Get the actual goal node from the path
        solution = goal_node.getSolution()
        for action in solution:
            gui.update_board(action)
            time.sleep(0.3)
        gui.update_board(action, True, len(solution) - 1, num_steps)
    else:
        labelerreur = Label(window, text='Optimal solution not found', bg='#FCCD2A', fg='white')
        labelerreur.pack()
        window.update()

        
#--------------------------------------------------------------------         Main        ---------------------------------------------------------------------------------------

start_game_class()

