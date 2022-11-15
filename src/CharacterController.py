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
    def InputKeyboard(self, key, x, y):
        """
        wasd movement
        """
        #Conversion from Mouse coordinates to World coordinates
        x_world, y_world = self.GetMouseCoordinates(x, y)
        print(f"keyboard event: key={key}, x={x_world}, y={y_world}")

        #Required
        if key == b'd' or key == b'D':
            print("D pressed -> Default Transform")
            self.camera.InitTransform()
        if key == b'0':
            print("0 pressed -> Reset Projection")
            self.camera.InitProjection()
        if key == b'\x1b':
            print("ESC pressed -> Exit Program")
            glutLeaveMainLoop()
        glutPostRedisplay()

        pass

    def InputSpecial(self, key, x, y):
        """
        Camera Rotation Via Left Right Arrow
        """
        x_world, y_world = self.GetMouseCoordinates(x, y)
        print(f"special Key event: key={key}, x={x_world}, y={y_world}")
        #Fov Change goes Here -> Arrow Keys   
        if key == 101:#UpArrow
            #Increase Fov by 5
            self.camera.FovChange(5)#->Don't use UpdateProjection here due to Projection init with in
        if key == 103:#DownArrow
            #Decrease Fov by 5
            self.camera.FovChange(-5)        
        glutPostRedisplay()

        pass

    def UpdateState(self):
        """
        Updates the state of the player
        1. Position
        2. Life
        """
        pass

if __name__ == "__main__":
    pass