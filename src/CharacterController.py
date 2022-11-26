# This is the Character Controller
# Every Input to the Character would be given via this script
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math

class CharacterController:
    def __init__(self, maze, tile_size=0.25):
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
        # Tile Size info 
        self.tile_size = tile_size
        self.room_size = 4 * self.tile_size

        # Maze Info
        self.maze = maze
        self.mazeWidth = maze.width
        self.mazeHeight = maze.height
        self.entrancePoint = maze.entrancePoint
        self.exitPoint = maze.exitPoint
        self.savePoint = maze.savePoint

        # PlayerInfo
        self.playerLife = 5

        # Pos Info, Initialized to Entrance
        self.pos = np.eye(4)
        self.pos[0,3] = (maze.entrancePoint[0] * 4 + 2) * self.tile_size 
        self.pos[2,3] = (maze.entrancePoint[1] * 4 + 2) * self.tile_size
        print("init\n", self.pos)
    def Translation(self, rotation, direction):
        """
        Translates the player.
        The Local Location is First Updated
        Depending on the Local Location Value, the Global location is Updated as well
        """
        # Make Temp Points
        translation = rotation @ direction
        temp_x = self.pos[0,3] + translation[0]
        temp_z = self.pos[2,3] + translation[2]
        print("at the beginning\n",self.pos)

        half_size = 0.1

        temp_coords = [(temp_x-half_size, temp_z-half_size),
                        (temp_x-half_size, temp_z+half_size),
                        (temp_x+half_size, temp_z-half_size),
                        (temp_x+half_size, temp_z+half_size)]

        for coord in temp_coords:
            coord_x = coord[0]
            coord_z = coord[1]
            
            check_x = math.floor(coord_x / self.room_size)
            check_z = math.floor(coord_z / self.room_size)

            # Check If pos is updatable
            # Out of Maze Check
            if check_x>self.mazeHeight-1 or check_x<0 or check_z>self.mazeWidth-1 or check_z<0:
                print("maze is\n",self.maze.pathMap)
                print("rotation is\n", rotation[0:3, 0:3])
                print("pos is\n", self.pos[0:3,3])
                print("You Can't get Out of the maze: pos ", temp_z, " ", temp_x)
                return False
            # Wall Colision check
            elif self.maze.pathMap[check_z, check_x] == 0:
                print("maze is\n",self.maze.pathMap)
                print("rotation is\n", rotation[0:3, 0:3])
                print("pos is\n", self.pos[0:3,3])
                print("You can't walk into walls: pos ", temp_z, " ", temp_x)
                return False
            # Maybe we can add sliding along the

        self.pos[0,3] = temp_x
        self.pos[2,3] = temp_z
        print("maze is\n",self.maze.pathMap)
        print("rotation is\n", rotation[0:3, 0:3])
        print("pos is\n", self.pos[0:3,3])
        return True
    
    def Translation2(self, rotation, direction):
        """
        Translates the player.
        The Local Location is First Updated
        Depending on the Local Location Value, the Global location is Updated as well

        For Wall Collision, recalculate the slideable location, slide toward that location
        """
        # Make Temp Points
        translation = rotation @ direction
        temp_x = self.pos[0,3] + translation[0]
        temp_z = self.pos[2,3] + translation[2]
        
        half_size = 0.1

        temp_coords = [(temp_x-half_size, temp_z-half_size),
                        (temp_x-half_size, temp_z+half_size),
                        (temp_x+half_size, temp_z-half_size),
                        (temp_x+half_size, temp_z+half_size)]

        slide = False
        for coord in temp_coords:
            coord_x = coord[0]
            coord_z = coord[1]
            
            check_x = math.floor(coord_x / self.room_size)
            check_z = math.floor(coord_z / self.room_size)

            # Check If pos is updatable
            # Out of Maze Check || Wall Colision check
            if self.NotPossiblePos(check_x, check_z):
                slide = True
                break
            
        if slide == False:
            self.pos[0,3] = temp_x
            self.pos[2,3] = temp_z
            print("maze is\n",self.maze.pathMap)
            print("rotation is\n", rotation[0:3, 0:3])
            print("pos is\n", self.pos[0:3,3])
            return direction
        # Need to calculate sliding direction
        # As only diagonal movements are possible for sliding only think of them
        else:
            # +z or +x possible
            if translation[0] > 0 and translation[1] > 0:
                # +z move
                if self.NotPossiblePos(check_x + 1, check_z)==False:
                    pass
                # +x move
                if self.NotPossiblePos(check_x, check_z + 1)==False:
                    pass
            # -z or +x possible
            elif translation[0] > 0 and translation[1] < 0:
                # -z move
                if self.NotPossiblePos(check_x + 1, check_z)==False:
                    pass
                # +x move
                if self.NotPossiblePos(check_x, check_z - 1)==False:
                    pass
            # +z or -x possible
            elif translation[0] < 0 and translation[1] > 0:
                # +z move
                if self.NotPossiblePos(check_x - 1, check_z)==False:
                    pass
                # -x move
                if self.NotPossiblePos(check_x, check_z + 1)==False:
                    pass
            #  -z or -x possible
            elif translation[0] < 0 and translation[1] < 0:
                # -z move
                if self.NotPossiblePos(check_x - 1, check_z)==False:
                    pass
                # -x move
                if self.NotPossiblePos(check_x, check_z - 1)==False:
                    pass
            else:
                print("Directly Going Towards un unreachable point, can't move")
                return 0, 0

    def Translation3(self, rotation, direction):
        """
        
        """
        directions = [7,8,9,4,5,6,1,2,3]

        half_size = 0.1
        
        translation = rotation @ direction
        delta_x = translation[0]
        delta_z = translation[2]
        temp_x = self.pos[0,3] + translation[0]
        temp_z = self.pos[2,3] + translation[2]
        
        possible = []

        if delta_z>0 and delta_x>0:
            possible = [8,9,6]
        elif delta_z>0 and delta_x<0:
            possible = [8,7,4]
        elif delta_z<0 and delta_x>0:
            possible = [6,3,2]
        elif delta_z<0 and delta_x<0:
            possible = [4,1,2]

        for num in possible:
            if num == 7:
                pass
            if num == 8:
                pass
            if num == 9:
                pass
            if num == 4:
                pass
            if num == 5:
                pass
            if num == 6:
                pass
            if num == 1:
                pass
            if num == 2:
                pass
            if num == 3:
                pass

        temp_coords = [(temp_x-half_size, temp_z-half_size),
                        (temp_x-half_size, temp_z+half_size),
                        (temp_x+half_size, temp_z-half_size),
                        (temp_x+half_size, temp_z+half_size)]

    def NotPossiblePos(self, x, z):
        # Check Out of Maze
        if x>self.mazeHeight-1 or x<0 or z>self.mazeWidth-1 or z<0:
            return True
        # Check Wall
        elif self.maze.pathMap[z, x] == 0:
            return True
        # Pass all Error Detections
        else:
            return False

    def Reset(self):
        self.pos = np.eye(4)
        self.pos[0,3] = (self.entrancePoint[0] * 4 + 2) * self.tile_size 
        self.pos[2,3] = (self.entrancePoint[1] * 4 + 2) * self.tile_size
        print("Controller Position Reset")

    def AngleToExit(self, rotationAngle):
        """
        Return Angle to Exit point, x/z coordinate

        Prob -> This equation is based on the Fact that character is looking towards (0, -1) on x/z coordinate.
        If the above assumption is broken, different results would be required
        """
        deltaX = (self.exitPoint[0]*4+2)*self.tile_size - self.pos[0,3]
        deltaZ = (self.exitPoint[1]*4+2)*self.tile_size - self.pos[2,3]
        angleToExit = np.arctan2(deltaZ, deltaX)
        
        lookingAngle = np.radians((270 -rotationAngle)%360)
        
        angle = angleToExit - lookingAngle 
        return angle

    def UpdateState(self):
        """
        Updates the state of the player
        1. Life
        """
        pass


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