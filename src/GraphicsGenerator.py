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
        self.characterController = ()
        self.tile_size = 0.25
        self.height = 0.2

        self.move_speed = 0.05
        self.degree_speed = 5

        self.w = 800
        self.h = 800

        self.reset_pos(8)

        self.test_wall_list = [(1,0),(2,0),(3,0),(4,0),(4,1),(0,2),(0,3),(1,3),(2,2),(2,3)]
        # self.test_wall_list = [(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0),(9,0),(10,0)]
        self.color_list = ['red','orange','yellow','green','blue','indigo','violet']
        

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
        # H is z and W is x
        h,w = self.maze.shape
        for hp in range(4*h):
            for wp in range(4*w):
                if hp%2 != wp%2:
                    color = 'black'
                else:
                    color = 'white'
                self.GenerateSingleBlock(self.tile_size*(wp-1.5), -self.height, self.tile_size*(hp-1.5), self.tile_size, color, 'tile')

    def GenerateWalls_old(self, test: int=0):
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
                # ** Notice: -edge_location+size*i or +edge_location+size*i will give opposite side of edges
                # ** Notice: Changing x and z coordinate will give wall at other axis
                if test == 0:
                    self.GenerateSingleBlock(edge_location, j*size + threshold, -edge_location + size * i, size, color)
                elif test == 1:
                    self.GenerateSingleBlock(-edge_location + size * i, j*size + threshold, -edge_location, size, color)
                elif test == 2:
                    self.GenerateSingleBlock(-edge_location, j*size + threshold, -edge_location + size * i, size, color)
                elif test == 3:
                    self.GenerateSingleBlock(-edge_location + size * i, j*size + threshold, edge_location, size, color)

    def GenerateWalls(self):
        for i, coord in enumerate(self.test_wall_list):
            x = coord[0]
            z = coord[1]
            l = len(self.color_list)
            color = self.color_list[i%l]
            self.GenerateSingleBlock(x*4*self.tile_size, self.tile_size*1.0125, z*4*self.tile_size, 4*self.tile_size, color, 'block')

    def GenerateSingleBlock(self, x,y,z, size=0.25, color='black', mode='block'):
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
            glColor3f(0.175,0.175,0.175)
        elif color == 'white':
            glColor3f(1.0,1.0,1.0)

        # rainbow SPECTRUM
        elif color == 'red':
            glColor3f(0.860,0.0625,0.0625)
        elif color == 'orange':
            glColor3f(0.860,0.420,0.01)
        elif color == 'yellow':
            glColor3f(0.75,0.75,0.06)
        elif color == 'green':
            glColor3f(0.125,0.750,0.125)
        elif color == 'blue':
            glColor3f(0.125,0.125,0.860)
        elif color == 'indigo':
            glColor3f(0.350,0.06,0.575)
        elif color == 'violet':
            glColor3f(0.350,0.12,0.750)

        elif color == 'magenta':
            glColor3f(0.750,0.250,0.625)
        elif color == 'gray':
            glColor3f(0.75,0.75,0.75)
        else:
            glColor3f(0.35,0.84,0.42)

        if mode=='tile':
            sc_mat = np.eye(4)
            sc_mat[1,1]=0.1
            glMultMatrixf(trans_mat.T)
            glMultMatrixf(sc_mat.T)
            glutSolidCube(size)
            sc_mat[1,1]=1/sc_mat[1,1]
            glMultMatrixf(sc_mat.T)
            glMultMatrixf(trans_mat_i.T)
        elif mode=='block':
            glMultMatrixf(trans_mat.T)
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
        self.nearz = self.camz * 1.0125 # self.camz - 7/8
        self.farz = self.camz * 3

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
        gluLookAt(0,0.3,self.camz, 0,0,0, 0,1,0)
        glMultMatrixf((self.trans_mat).T)
        # glutSolidTeapot(0.125)

        # tile Generation
        self.GenerateTiles()

        # Wall Generation test
        self.GenerateWalls()

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
        if key == b'w' or key == b'W':
            self.trans_mat[2,3] = self.trans_mat[2,3] + self.move_speed
        if key == b's' or key == b'S':
            self.trans_mat[2,3] = self.trans_mat[2,3] - self.move_speed
        if key == b'a' or key == b'A':
            self.trans_mat[0,3] = self.trans_mat[0,3] + self.move_speed
        if key == b'd' or key == b'D':
            self.trans_mat[0,3] = self.trans_mat[0,3] - self.move_speed
        
        if key == b'u' or key == b'U':
            self.reset_pos(0)
        if key == b'i' or key == b'I':
            self.reset_pos(1)
        if key == b'o' or key == b'O':
            self.reset_pos(2)
        if key == b'p' or key == b'P':
            self.reset_pos(3)
        if key == b'l' or key == b'L':
            self.reset_pos(8)
        
        if key == b'\x1b':
            print('Good bye')
            glutLeaveMainLoop()

        glutPostRedisplay()
    def special(self, key, x, y):
        # 100 is left and 102 is right
        if key == 100:
            temp_rot = self.rotation(self.degree_speed)

            self.trans_mat = temp_rot @ self.trans_mat
        if key == 102:
            temp_rot = self.rotation(-self.degree_speed)
            self.trans_mat = temp_rot @ self.trans_mat
        # self.characterController.InputSpecial(key)
        glutPostRedisplay()
    
    def rotation(self, degree = 10):
        temp_rot = np.eye(4)
        rad = degree * np.pi / 180
        temp_rot[0,0] = np.cos(rad)
        temp_rot[0,2] = -np.sin(rad)
        temp_rot[2,0] = np.sin(rad)
        temp_rot[2,2] = np.cos(rad)
        return temp_rot

    def reset_pos(self, pos:int = 0):
        # This function might be transferred to savepoint load function.
        # pos is the wall side where the character will be placed.
        temp_trans = np.eye(4)
        if pos == 0:
            temp_trans[1,3] = -0.1
            temp_trans[2,3] = -0.75
            degree = 0
            pass
        elif pos == 1:
            temp_trans[1,3] = -0.1
            temp_trans[0,3] = -0.75
            degree = 90
            pass
        elif pos == 2:
            temp_trans[1,3] = -0.1
            temp_trans[2,3] = 0.75
            degree = 180
            pass
        elif pos==3:
            temp_trans[1,3] = 0.1
            temp_trans[0,3] = 0.75
            degree = 270
        else:
            degree = 225
        
        self.trans_mat = self.rotation(degree)@temp_trans
    def Update(self):
        glutInit()
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glutInitWindowSize(1600, 900) #-> Sys get full height width
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
    TestMaze = np.array([[2,0,0,0,0],[1,1,1,1,0],[0,1,0,1,1],[0,0,0,1,3]])
    print(TestMaze)
    Generator = GraphicsGenerator(TestMaze)
    Generator.Update()