# This is the Character Controller
# Every Input to the Character would be given via this script
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math

class CharacterController:
    def __init__(self, maze):
        """
        Player has 2 Pos
        01. Global => Which Tile the Player is on(movement from Global requires boundary checking)
        02. local => Location on a single Tile(movement in here has no effect on Global)
        03. localPosMax => Maximum Point on local scale
        04. localPosMin => Minimum Point on local scale
        Player has 5 life points, when it reaches 0, would create a save point and return to the init position
        05. life => 5 Points
        Player has 3 points saved
        06. GoalPoint => Destination
        07. InitPoint => StartingPoint
        08. SavePoint => CouldResume from here after loosing all one's point
        Player has Speed Factor, Direction Factor
        09. SpeedFactor => Determines the Speed of translation
        10. DirectionFactor => Determines the 2d Direction the player is looking at initialy towards (1,0)
        """
        # Maze Info
        self.maze = maze
        self.mazeWidth = maze.width
        self.mazeHeight = maze.height
        self.exitPoint = maze.exitPoint
        self.entrancePoint = maze.entrancePoint
        self.savePoint = maze.savePoint

        # PlayerInfo
        self.playerLife = 5
        
        # GlobalPos Info, Initialized to Entrance
        self.playerGlobalPos = np.eye(4)
        self.playerGlobalPos[0,3] = self.entrancePoint[0]
        self.playerGlobalPos[2,3] = self.entrancePoint[1]

        # LocalPosInfo, Initialized to 0,1,0 (y=1)
        self.playerLocalPos = np.eye(4)
        self.playerLocalPos[1,3] = 1
        self.localPosMax = 16
        self.localPosMin = 0

        # Speed Factor to indicate Speed the Player is moving, Default Speed Value is 1
        self.speedFactor = np.zeros((4,1))
        self.speedFactor[0,0] = 0.01#This Number Decides the speed
        self.speedFactor[3,0] = 1
        
        # 4 Rotation Matrixes for wasd movement
        # Forward is ? Direction
        # Backward is ? Direction
        # Left is ? Direction
        # Right is ? Direction
        self.forward = np.eye(4)

        self.backward = np.eye(4)
        self.backward[0,0] = -1
        self.backward[2,2] = -1

        self.left = np.eye(4)
        self.left[0,0] = 0
        self.left[0,2] = 1
        self.left[2,0] = -1
        self.left[2,2] = 0
        
        self.right = np.eye(4)
        self.right[0,0] = 0
        self.right[0,2] = -1
        self.right[2,0] = 1
        self.right[2,2] = 0
        
        # Rotation Degree
        self.rotation = 0

    def Translate(self, direction):
        """
        Translates the player.
        The Local Location is First Updated
        Depending on the Local Location Value, the Global location is Updated as well
        """
        # Cache Up LocalPos
        localTemp = np.copy(self.playerLocalPos)

        print("Direction is\n",direction)

        # Update LocalPos
        rotationMat = np.eye(4)
        rotationMat[0:3,0:3] = self.playerLocalPos[0:3,0:3]
        
        translation = rotationMat @ direction @ self.speedFactor
        self.playerLocalPos[0,3] += translation[0,0]
        self.playerLocalPos[2,3] += translation[2,0]

        # Check If Global Pos Needs Update
        # If Update Needed -> Try Updating Global Pos
        if self.playerLocalPos[0,3] // self.localPosMax != self.playerGlobalPos[0,3] or self.playerLocalPos[2,3] // self.localPosMax != self.playerGlobalPos[2,3]:
            print("x is ", self.playerLocalPos[0,3] // self.localPosMax)
            print("z is ", self.playerLocalPos[2,3] // self.localPosMax)

            # Cache Up GlobalPos
            globalTemp = np.copy(self.playerGlobalPos)
            # Update Global Pos
            self.playerGlobalPos[0,3] += 1 if self.playerLocalPos[0,3]//self.localPosMax>self.playerGlobalPos[0,3] else(-1 if self.playerLocalPos[0,3]//self.localPosMax<self.playerGlobalPos[0,3] else 0)
            self.playerGlobalPos[2,3] += 1 if self.playerLocalPos[2,3]//self.localPosMax>self.playerGlobalPos[2,3] else(-1 if self.playerLocalPos[2,3]//self.localPosMax<self.playerGlobalPos[2,3] else 0)

            # Check Validity of Global Pos
            # !Valid -> RollBack Local Pos, Global Pos
            if self.GlobalIsntWall() != True:
                print("Walking Toward Wall, Can't Move")
                self.playerLocalPos = localTemp
                self.playerGlobalPos = globalTemp

        # if self.playerLocalPos[0,3] >= self.localPosMax or self.playerLocalPos[0,3] < self.localPosMin or self.playerLocalPos[2,3] >= self.localPosMax or self.playerLocalPos[2,3] < self.localPosMin:
        #     # Cache Up GlobalPos
        #     globalTemp = np.copy(self.playerGlobalPos)
            
        #     # Update Global Pos
        #     self.playerGlobalPos[0,3] += 1 if self.playerLocalPos[0,3]>=self.localPosMax else(-1 if self.playerLocalPos[0,3]<self.localPosMin else 0)
        #     self.playerGlobalPos[2,3] += 1 if self.playerLocalPos[2,3]>=self.localPosMax else(-1 if self.playerLocalPos[2,3]<self.localPosMin else 0)

        #     # Check Validity of Global Pos
        #     # Valid -> Update Local Pos
        #     if self.GlobalIsntWall():
        #         print("Walk Over Edges")
        #         self.playerLocalPos[0,3] = self.playerLocalPos[0,3]%self.localPosMax
        #         self.playerLocalPos[2,3] = self.playerLocalPos[2,3]%self.localPosMax
        #     # !Valid -> RollBack Local Pos, Global Pos
        #     else:
        #         print("Walking Toward Wall, Can't Move")
        #         self.playerLocalPos = localTemp
        #         self.playerGlobalPos = globalTemp

        print("Current  Local Location is\n", self.playerLocalPos)
        print("CUrrent Global Location is\n", self.playerGlobalPos)

    def Rotate(self, rotation):
        """
        Rotate the player
        """
        self.rotation += rotation
        self.rotation %= 360
        rotationMat = np.eye(4)
        rotationMat[0,0] = np.cos(np.radians(self.rotation))
        rotationMat[0,2] = -np.sin(np.radians(self.rotation))
        rotationMat[2,0] = np.sin(np.radians(self.rotation))
        rotationMat[2,2] = np.cos(np.radians(self.rotation))
        self.playerLocalPos[0:3,0:3] = rotationMat[0:3, 0:3]

        print("Current rotation is ", self.rotation)

    def GlobalIsntWall(self):
        """
        Checks if the current global Position is a wall or not
        """
        coordinate_1 = int(self.playerGlobalPos[0,3])
        coordinate_2 = int(self.playerGlobalPos[2,3])
        print("Coordinate is ",coordinate_1, " ",coordinate_2)
        
        if coordinate_1 < 0 or coordinate_2 < 0 or coordinate_1 >= self.mazeWidth or coordinate_2 >= self.mazeHeight:
            print("Global Location ", self.playerGlobalPos[0,3], " ", self.playerGlobalPos[2,3], " Is the Outside the Maze")
            return False
        elif self.maze.pathMap[coordinate_1, coordinate_2] == 0:
            print("Global Location ", self.playerGlobalPos[0,3], " ", self.playerGlobalPos[2,3], " Is the Maze Wall")
            return False
        else:
            return True

    def UpdateState(self):
        """
        Updates the state of the player
        1. Life
        """
        pass

    def InputKeyboard(self, key, x, y):
        """
        wasd movement
        """
        print(f"Keyboard event: key={key}")
        #Required
        if key == b'w' or key == b'W':
            print("W pressed -> Translate Forward")
            self.Translate(self.forward)
        if key == b'a' or key == b'A':
            print("A pressed -> Translate Left")
            self.Translate(self.left)
        if key == b's' or key == b'S':
            print("S pressed -> Translate Back")
            self.Translate(self.backward)
        if key == b'd' or key == b'D':
            print("D pressed -> Translate Right")
            self.Translate(self.right)

        if key == b'\x1b':
            print("ESC pressed -> Exit Program")
            glutLeaveMainLoop()

        glutPostRedisplay()

    def InputSpecial(self, key, x, y):
        """
        Camera Rotation Via Left Right Arrow
        """
        print(f"special Key event: key={key}")
        #Required
        if key == 100:#LeftArrow
            print("Left Arrow Pressed")
            self.Rotate(-5)    
        if key == 102:#RightArrow
            print("Right Arrow Pressed")
            self.Rotate(5)

        glutPostRedisplay()

    # Temp Functions for Testing Purpose Only
    def GenerateGraphics(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0, 0, 0, 1)
        glMatrixMode(GL_PROJECTION)
        glMatrixMode(GL_MODELVIEW)
        glutSwapBuffers()
    def Update(self):
        glutInit()
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glutInitWindowSize(100, 100) #-> Sys get full height width
        glutInitWindowPosition(0, 0)
        glutCreateWindow(b"Maze Simulator")
        glutDisplayFunc(self.GenerateGraphics)
        glutKeyboardFunc(self.InputKeyboard)#wasd movement
        glutSpecialFunc(self.InputSpecial)#Left Right Arrow
        glutMainLoop()

if __name__ == "__main__":
    from MazeGenerator import *
    width = 30
    height = 31
    entrancePoint = (0, 0)
    exitPoint = (width-1, height-1)
    mazeGenerator = MazeGenerator()
    maze = mazeGenerator.GenerateMaze(width, height, entrancePoint, exitPoint)

    characterController = CharacterController(maze)
    characterController.Update()