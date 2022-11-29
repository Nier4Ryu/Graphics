# This is the MazeSimulator that integrates every thing
# Basic Modules

# import our models
from MazeGenerator import*  # -> Create Maze, after that useless
from GraphicsGenerator import*
import argparse
 
class Simulator:
    def __init__(self, width=51, height=51):
        width = width
        height = height
        entrancePoint = (0,0)
        exitPoint = (width-1, height-1)
        mazeGenerator = MazeGenerator()
        maze = mazeGenerator.GenerateMaze(width, height, entrancePoint, exitPoint)

        initial_angle = 180
        self.graphicsGenerator = GraphicsGenerator(maze, initial_angle)

    def RunSimulator(self):
        self.graphicsGenerator.Update()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Maze Level")

    parser.add_argument('--w', type=int, default=25)
    parser.add_argument('--h', type=int, default=25)
    args = parser.parse_args()
    width = args.w
    height = args.h
    simulator = Simulator(width, height)
    simulator.RunSimulator()