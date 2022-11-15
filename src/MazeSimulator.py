# This is the MazeSimulator that integrates every thing
# Basic Modules

# import our models
import MazeGenerator # -> Create Maze, after that useless
import GraphicsGenerator

class Simulator:
    def __init__(self):
        width = 51
        height = 51
        entrancePoint = (0, 0)
        exitPoint = (width-1, height-1)
        mazeGenerator = MazeGenerator(width, height, entrancePoint, exitPoint)
        self.maze = mazeGenerator.GenerateMaze()

        self.graphicsGenerator = GraphicsGenerator(self.maze)

    def RunSimulator(self):
        self.graphicsGenerator.Update()

if __name__ == "__main__":
    simulator = Simulator()
    simulator.RunSimulator()