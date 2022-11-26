"""
This is the maze generation algorithm, which is basically the code from this link
"https://www.geeksforgeeks.org/random-acyclic-maze-generator-with-given-entry-and-exit-point/"
Maze Info
0 = Wall
1 = Empty Path
2 = Entrance
3 = Exit
"""

# Numpy is used to convert non np array to np array
import numpy as np
import sys
import math

# Python3 code to implement the approach
from random import randint
# Class to define structure of a node
class Node:
    def __init__(self, value = None, next_element = None):
        self.val = value
        self.next = next_element

# Class to implement a stack
class stack:
    # Constructor
    def __init__(self):
        self.head = None
        self.length = 0

    # Put an item on the top of the stack
    def insert(self, data):
        self.head = Node(data, self.head)
        self.length += 1

    # Return the top position of the stack
    def pop(self):
        if self.length == 0:
            return None
        else:
            returned = self.head.val
            self.head = self.head.next
            self.length -= 1
            return returned

    # Return False if the stack is empty 
    # and true otherwise
    def not_empty(self):
        return bool(self.length)

    # Return the top position of the stack
    def top(self):
        return self.head.val

class Maze:
    def __init__(self,width, height, entrancePoint, exitPoint):
        self.width = width
        self.height = height
        self.entrancePoint = entrancePoint
        self.exitPoint = exitPoint
        self.savePoint = entrancePoint

        self.walls = []

        self.marks = []
        self.num_marks_max = 10

        self.traps = []
        self.num_traps = math.floor((self.width+self.height)/4)

        self.pathMap = None

    def SetPathMap(self, pathMap):
        """
        Create Map of Paths
        """
        self.pathMap = pathMap

    def CountWalls(self):
        """
        Create A list of walls
        1) Calculate the L2 => square root Distance
        2) Calculate the L1 => abs Distance -> THis is the one to use for now           
        """
        exit_x = self.exitPoint[0]
        exit_z = self.exitPoint[1]

        max_distance_x = max(exit_x, self.width -1 -exit_x)
        max_distance_z = max(exit_z, self.height -1 -exit_z)
        max_distance = max_distance_x + max_distance_z

        space = 6

        for i in range(math.ceil(max_distance/space)):
            self.walls.append([])

        for i in range(self.width):
            for j in range(self.height):
                if self.pathMap[i,j]==0:                    
                    # Calculate L1 Distance
                    delta_x = i-exit_x
                    delta_z = j-exit_z
                    distance = abs(delta_x) + abs(delta_z)
                    self.walls[math.ceil(distance/space)-1].append((i,j))

        print("walls arranged in distance is")
        for walls in self.walls:
            print("walls is :: ", walls)
                    
    def PushMarks(self, pos, mark_type):
        """
        Create a position (parse pos)
        create a mark
        append to self.marks
        pop if num over max
        """
        pos_x = pos[2,3]
        pos_z = pos[0,3]
        self.marks.append((pos_x, pos_z, mark_type))
        if len(self.marks) > self.num_marks_max:
            self.marks.pop(0)
        print("Creating Marks\n",self.marks)

    def SetTraps(self):
        for i in range(self.num_traps):
            self.CreateTrap()

    def CreateTrap(self):
        """
        Create a random trap
        """

        # point_x = randint(0, self.width-1)
        # point_z = randint(0, self.height-1)

        # pos_x = pos[2,3]
        # pos_z = pos[0,3]
        # self.traps.append((pos_x, pos_z, trap_type))
        # if len(self.traps) > self.num_marks_max:
        #     self.marks.pop(0)
        # print("Creating Marks\n",self.marks)
        pass
class Trap:
    def __init__(self):
        self.pos_x = None
        self.pos_z = None

        self.type = None
class MazeGenerator:
    def __init__(self):
        pass

    # Function to generate the random maze
    def GenerateMaze(self,width, height, entrancePoint, exitPoint):
        ROWS = width
        COLS = height
        P0 = entrancePoint
        Pf = exitPoint

        # Create A Maze Object
        maze = Maze(width, height, entrancePoint, exitPoint)
        
        # Array with only walls (where paths will 
        # be created)
        pathMap = list(list(0 for _ in range(COLS)) 
                        for _ in range(ROWS))
        
        # Auxiliary matrices to avoid cycles
        seen = list(list(False for _ in range(COLS)) 
                            for _ in range(ROWS))
        previous = list(list((-1, -1) 
        for _ in range(COLS)) for _ in range(ROWS))
    
        S = stack()
        
        # Insert initial position
        S.insert(P0) 
    
        # Keep walking on the graph using dfs
        # until we have no more paths to traverse 
        # (create)
        while S.not_empty():
    
            # Remove the position of the Stack
            # and mark it as seen
            x, y = S.pop()
            seen[x][y] = True
    
            # Check if it will create a cycle
            # if the adjacent position is valid 
            # (is in the maze) and the position 
            # is not already marked as a path 
            # (was traversed during the dfs) and 
            # this position is not the one before it
            # in the dfs path it means that 
            # the current position must not be marked.
            
            # This is to avoid cycles with adj positions
            if (x + 1 < ROWS) and pathMap[x + 1][y] == 1 and previous[x][y] != (x + 1,  y):
                continue
            if (0 < x) and pathMap[x-1][y] == 1 and previous[x][y] != (x-1,  y):
                continue
            if (y + 1 < COLS) and pathMap[x][y + 1] == 1 and previous[x][y] != (x, y + 1):
                continue
            if (y > 0) and pathMap[x][y-1] == 1 and previous[x][y] != (x, y-1):
                continue
    
            # Mark as walkable position
            pathMap[x][y] = 1
    
            # Array to shuffle neighbours before 
            # insertion
            to_stack = []
    
            # Before inserting any position,
            # check if it is in the boundaries of 
            # the maze
            # and if it were seen (to avoid cycles)
    
            # If adj position is valid and was not seen yet
            if (x + 1 < ROWS) and seen[x + 1][y] == False:
                # Mark the adj position as seen
                seen[x + 1][y] = True
                
                # Memorize the position to insert the 
                # position in the stack
                to_stack.append((x + 1,  y))
                
                # Memorize the current position as its 
                # previous position on the path
                previous[x + 1][y] = (x, y)
            
            if (0 < x) and seen[x-1][y] == False:
                # Mark the adj position as seen
                seen[x-1][y] = True
                
                # Memorize the position to insert the 
                # position in the stack
                to_stack.append((x-1,  y))
                
                # Memorize the current position as its 
                # previous position on the path
                previous[x-1][y] = (x, y)
            
            if (y + 1 < COLS) and seen[x][y + 1] == False:
                # Mark the adj position as seen
                seen[x][y + 1] = True
                
                # Memorize the position to insert the 
                # position in the stack
                to_stack.append((x, y + 1))
                
                # Memorize the current position as its
                # previous position on the path
                previous[x][y + 1] = (x, y)
            
            if (y > 0) and seen[x][y-1] == False:
                # Mark the adj position as seen
                seen[x][y-1] = True
                
                # Memorize the position to insert the 
                # position in the stack
                to_stack.append((x, y-1))
                
                # Memorize the current position as its 
                # previous position on the path
                previous[x][y-1] = (x, y)
            
            # Indicates if Pf is a neighbour position
            pf_flag = False
            while len(to_stack):
                # Remove random position
                neighbour = to_stack.pop(randint(0, len(to_stack)-1))
                
                # Is the final position, 
                # remember that by marking the flag
                if neighbour == Pf:
                    pf_flag = True
                
                # Put on the top of the stack
                else:
                    S.insert(neighbour)
            
            # This way, Pf will be on the top 
            if pf_flag:
                S.insert(Pf)
                    
        # Mark the initial position
        x0, y0 = P0
        xf, yf = Pf
        pathMap[x0][y0] = 1
        pathMap[xf][yf] = 1
        
        # Set the PathMap of the maze
        maze.SetPathMap(np.array(pathMap))

        # Count the Walls
        maze.CountWalls()

        # Setup Traps with in the maze
        maze.SetTraps()

        # Return maze formed by the traversed path
        return maze

# Driver code
if __name__ == "__main__":
    width = 30
    height = 31
    entrancePoint = (0, 0)
    exitPoint = (width-1, height-1)
    mazeGenerator = MazeGenerator()
    maze = mazeGenerator.GenerateMaze(width, height, entrancePoint, exitPoint)
    np.set_printoptions(threshold=sys.maxsize)
    print(maze.pathMap)