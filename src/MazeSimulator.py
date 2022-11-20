# This is the MazeSimulator that integrates every thing
# Basic Modules

# import our models
from MazeGenerator import*  # -> Create Maze, after that useless
from GraphicsGenerator import*
 
class Simulator:
    def __init__(self):
        width = 5
        height = 5
        entrancePoint = (0,0)
        exitPoint = (width-1, height-1)
        mazeGenerator = MazeGenerator()
        maze = mazeGenerator.GenerateMaze(width, height, entrancePoint, exitPoint)

        self.graphicsGenerator = GraphicsGenerator(maze)

    def RunSimulator(self):
        self.graphicsGenerator.Update()

if __name__ == "__main__":
    simulator = Simulator()
    simulator.RunSimulator()