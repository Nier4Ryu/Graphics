# This is the MazeSimulator that integrates every thing
# Basic Modules

# import our models
from MazeGenerator import*  # -> Create Maze, after that useless
from GraphicsGenerator import*
 
class Simulator:
    def __init__(self):
        width = 6
        height = 6
        entrancePoint = (0,0)
        exitPoint = (width-1, height-1)
        mazeGenerator = MazeGenerator()
        maze = mazeGenerator.GenerateMaze(width, height, entrancePoint, exitPoint)

        initial_angle = 180
        self.graphicsGenerator = GraphicsGenerator(maze, initial_angle)

    def RunSimulator(self):
        self.graphicsGenerator.Update()

if __name__ == "__main__":
    simulator = Simulator()
    simulator.RunSimulator()