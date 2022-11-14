# This is the Character Controller
# Every Input to the Character would be given via this script
import numpy as np

class CharacterController:
    def __init__(self):
        """
        Player has 2 Pos
        1. Global => Which Tile the Player is on(movement from Global requires boundary checking)
        2. local => Location on a single Tile(movement in here has no effect on Global)
        Player has 5 life points, when it reaches 0, would create a save point and return to the init position
        3. life => 5 Points
        Player has 3 points saved
        4. GoalPoint => Destination
        5. InitPoint => StartingPoint
        6. SavePoint => CouldResume from here after loosing all one's point
        """
        self.playerGlobalPos = np.zeros(2)
        self.playerLocalPos = np.zeros(2)

        self.playerLife = 5

        self.goalPoint = np.zeros(2)
        self.initPoint = np.zeros(2)
        self.savePoint = np.zeros(2)
    def Input(self):
        pass

    def UpdateState(self):
        """
        Updates the state of the player
        1. Position
        2. Life
        """
        pass

    def GenerateController(self):
        pass

if __name__ == "__main__":
    pass