# This is the graphics Generator that generates the graphics based on the info
from CharacterController import *

from tkinter import Y
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np

class GraphicsGenerator:
    def __init__(self, maze):
        self.maze = maze
        self.characterController = CharacterController()
        self.tile_size = 2.0
        self.height = -1.25

        self.move_speed = 0.05

        self.w = 800
        self.h = 800

        self.trans_mat = np.eye(4)
        self.scale_mat = np.eye(4)
        self.rot_mat = np.eye(4)
        self.nearz = -4.0
        self.farz = 4.0
    def light(self):
        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_LIGHTING)
        glEnable(GL_DEPTH_TEST)

        # feel free to adjust light colors
        lightAmbient = [0.5, 0.5, 0.5, 1.0]
        lightDiffuse = [0.5, 0.5, 0.5, 1.0]
        lightSpecular = [0.5, 0.5, 0.5, 1.0]
        lightPosition = [1, 1, -1, 0]    # vector: point at infinity
        glLightfv(GL_LIGHT0, GL_AMBIENT, lightAmbient)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, lightDiffuse)
        glLightfv(GL_LIGHT0, GL_SPECULAR, lightSpecular)
        glLightfv(GL_LIGHT0, GL_POSITION, lightPosition)
        glEnable(GL_LIGHT0)

    def GenerateTiles(self):
        # y value is fixed. and then x/z vaule varies.
        for i in range(4):
            for j in range(4):
                if i%2==j%2:
                    color = 'black'
                else:
                    color = 'white'
                    # checker shape
                self.GenerateSingleBlock((-1.5+i)*self.tile_size,self.height,(-1.5+j)*self.tile_size,self.tile_size,color)

    def GenerateWalls(self, test: bool=False):
        size = self.tile_size/4
        color = 'white'
        threshold = 0
        edge_location=1.875*self.tile_size
        
        for i in range(16):
            for j in range(9):
                if i%2 == j%2:
                    color = 'black'
                else:
                    color = 'white'
                    # checker shape
                if test == True:
                    self.GenerateSingleBlock(edge_location, j*size + threshold, -edge_location + size * i, size, color)
                else:
                    self.GenerateSingleBlock(-edge_location + size * i, j*size + threshold, -edge_location, size, color)
                    # ** Notice: -edge_location+size*i or +edge_location+size*i will give opposite side of edges
                    # ** Notice: Changing x and z coordinate will give wall at other axis

    def GenerateSingleBlock(self, x,y,z, size=0.25, color='black'):
        # **!! This function must be just under the cam setting and transformation matrix !!**
        # **!! Not followed by glLoadIdentity() !!**
        # **!! glLoadIdentity() must be followed after every single block has been generated !!**
        trans_mat = np.eye(4)
        trans_mat[0,3] = x
        trans_mat[1,3] = y
        trans_mat[2,3] = z
        trans_mat_i = np.eye(4)
        trans_mat_i[0,3] = -x
        trans_mat_i[1,3] = -y
        trans_mat_i[2,3] = -z
        if color == 'black':
            glColor3f(0.2,0.2,0.2)
        elif color == 'white':
            glColor3f(1.0,1.0,1.0)
        else:
            glColor3f(0.75,0.125,0.25)

        glMultMatrixf(trans_mat.T) #define matrices
        glutSolidCube(size)
        glMultMatrixf(trans_mat_i.T)
        glColor3f(1.0,1.0,1.0)

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
    
    def perspective(self, fov):
        self.camz = self.h/800/np.tan((np.pi/180)*fov/2)
        self.nearz = self.camz / 8 # self.camz - 7/8
        self.farz = self.camz * 4.5

    def GenerateGraphics(self):
        """
        camera view
        tile
        wall
        """
        # Camera view
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0, 0, 0, 1)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        self.perspective(45)
        glFrustum(-self.w/800/8,self.w/800/8,-self.h/800/8,self.h/800/8, self.nearz, self.farz)

        glMatrixMode(GL_MODELVIEW)
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()
        gluLookAt(0,0,self.camz, 0,0,0, 0,1,0)
        glMultMatrixf((self.trans_mat@self.scale_mat@self.rot_mat).T)
        glutSolidTeapot(0.25)

        # tile Generation
        self.GenerateTiles()
        # Wall Generation (for test)
        self.GenerateWalls(True)
        self.GenerateWalls(False)
        glLoadIdentity()


        glutSwapBuffers()

    def reshape(self, w, h):
        # implement here
        print(f"window size: {w} x {h}")
        self.center_x = int(w/2)
        self.center_y = int(h/2)
        self.w = w
        self.h = h
        glViewport(0,0,self.w, self.h)
        glutPostRedisplay()
    def keyboard(self, key, x, y):
        # self.characterController.InputKeyboard(key)
        if key == b'w' or key == b'W':
            self.trans_mat[2,3] = self.trans_mat[2,3] + self.move_speed
        if key == b's' or key == b'S':
            self.trans_mat[2,3] = self.trans_mat[2,3] - self.move_speed
        if key == b'a' or key == b'A':
            self.trans_mat[0,3] = self.trans_mat[0,3] + self.move_speed
        if key == b'd' or key == b'D':
            self.trans_mat[0,3] = self.trans_mat[0,3] - self.move_speed
        
        if key == b'\x1b':
            print('Good bye')
            glutLeaveMainLoop()
        glutPostRedisplay()
    def special(self, key, x, y):
        # self.characterController.InputSpecial(key)
        glutPostRedisplay()
    def Update(self):
        glutInit()
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glutInitWindowSize(800, 800) #-> Sys get full height width
        glutInitWindowPosition(0, 0)
        glutCreateWindow(b"Maze Simulator")

        glutDisplayFunc(self.GenerateGraphics)
        glutKeyboardFunc(self.keyboard)#wasd movement
        glutSpecialFunc(self.special)#Left Right Arrow
        # glutMouseFunc(self.mouse)
        # glutMotionFunc(self.motion)
        glutReshapeFunc(self.reshape)

        self.light()

        glutMainLoop()
    
if __name__ == "__main__":
    Generator = GraphicsGenerator(np.zeros((4,4)))
    Generator.Update()