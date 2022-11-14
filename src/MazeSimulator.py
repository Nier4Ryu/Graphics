# This is the MazeSimulator that integrates every thing
# Basic Modules

# import our models
import MazeGenerator # -> Create Maze, after that useless
import CharacterController
import GraphicsGenerator

class Simulator:
    def __init__(self):
        width = 51
        height = 51
        entrancePoint = (0, 0)
        exitPoint = (width-1, height-1)
        mazeGenerator = MazeGenerator(width, height, entrancePoint, exitPoint)
        self.maze = mazeGenerator.GenerateMaze()

        characterController = CharacterController()
        self.controller = characterController.GenerateContorller()
        
        self.graphicsGenerator = GraphicsGenerator()

    def RunSimulator(self):
        while True:
            input = self.contoller.GetInputs()
            self.graphicsGenerator.Update(self.maze, input)

if __name__ == "__main__":
    simulator = Simulator()
    simulator.RunSimulator()