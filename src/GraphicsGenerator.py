# This is the graphics Generator that generates the graphics based on the info
from CharacterController import *

class GraphicsGenerator:
    def __init__(self, maze):
        self.maze = maze
        self.characterController = CharacterController()

    def GenerateGraphics(self):
        pass

    def GenerateTiles(self):
        """
        Single Local Tile is 4 * 4 cube
        """
        pass

    def GenerateWalls(self):
        for ~~ :
            self.generate_single_block(~~)
        pass
    def generate_single_block(self, x,y,z):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        trans_mat = np.eye(4)
        glMultMatrixf((trans_mat).T) #define matrices
        glutSolidCube(0.25)
        glLoadIdentity()

    def GenerateMarks(self):
        pass

    def GenerateTraps(self):
        pass

    def GenerateSavepoint(self):
        pass

    def GenerateCompass(self):
        pass

    def GenerateClock(self):
        pass

    def display(self):
        """
        camera view
        tile
        wall
        """

        pass
    def keyboard(self, key, x, y):
        self.characterController.InputKeyboard(key)
        glutPostRedisplay()
    def special(self, key, x, y):
        self.characterController.InputSpecial(key)
        glutPostRedisplay()
    def Update(self):
        glutInit()
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glutInitWindowSize(800, 800) #-> Sys get full height width
        glutInitWindowPosition(0, 0)
        glutCreateWindow(b"Maze Simulator")

        glutDisplayFunc(self.display)
        glutKeyboardFunc(self.keyboard)#wasd movement
        glutSpecialFunc(self.special)#Left Right Arrow
        # glutMouseFunc(self.mouse)
        # glutMotionFunc(self.motion)
        # glutReshapeFunc(self.reshape)

        self.light()

        glutMainLoop()
    
if __name__ == "__main__":
    pass