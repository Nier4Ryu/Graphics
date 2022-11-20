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
        self.savePoint = None

        self.walls = []

        self.pathMap = None
        self.objectsMap = None

    def SetPathMap(self, pathMap):
        """
        Create Map of Paths
        """
        self.pathMap = pathMap

    def SetObjectsMap(self):
        """
        Create Map of Objects, the pathMap should be ready for this to run
        """
        self.objectsMap = np.copy(self.pathMap)

    def CountWalls(self):
        """
        Create A list of walls
        """
        for i in range(self.width):
            for j in range(self.height):
                if self.pathMap[i,j]==0:
                    self.walls.append((i,j))
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

        # Set the ObjectMap of the maze
        maze.SetObjectsMap()

        # Count the Walls
        maze.CountWalls()

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