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
        self.map = maze.pathMap
        self.wall_list = maze.walls
        self.characterController = ()
        self.tile_size = 0.25
        self.height = 0.2

        self.move_speed = 0.05
        self.degree_speed = 5

        self.w = 1600
        self.h = 900

        self.reset_pos(8)

        # self.test_wall_list = [(1,0),(2,0),(3,0),(4,0),(4,1),(0,2),(0,3),(1,3),(2,2),(2,3)]
        self.test_wall_list = [(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0),(9,0),(10,0),(1,1), (2,2),
                                (1,4),(2,4),(3,4),(4,4),(5,4),(6,4),(7,4),(8,4),(9,4),(10,4),
                                (1,6),(2,6),(3,6),(4,6),(5,6),(6,6),(7,6),(8,6),(9,6),(10,6),
                                (1,10),(2,10),(3,10),(4,10),(5,10),(6,10),(7,10),(8,10),(9,10),(10,10),
                                (1,15),(2,15),(3,15),(4,15),(5,15),(6,15),(7,14),(8,15),(9,15),(10,15),
                                (1,20),(2,20),(3,20),(4,20),(5,20),(6,21),(7,21),(8,20),(9,20),(10,20),
                                (1,25),(2,25),(3,25),(4,25),(5,25),(6,26),(7,26),(8,25),(9,25),(10,25),
                                (1,30),(2,30),(3,30),(4,30),(5,30),(6,31),(7,31),(8,30),(9,30),(10,30),
                                (1,35),(2,35),(3,35),(4,34),(5,35),(6,35),(7,35),(8,35),(9,35),(10,35),
                                (1,50),(2,50),(3,50),(4,50),(5,50),(6,51),(7,51),(8,50),(9,50),(10,50),
                                (1,60),(2,60),(3,60),(4,60),(5,60),(6,61),(7,61),(8,60),(9,60),(10,60)]
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

    def GererateCheckerTexture(self):
        h,w = self.map.shape
        textbase = np.zeros((4*h, 4*w))
        # h is z direction and w is x direction.


        # glTexCoord2f

        pass

    def GenerateTiles_old(self):
        # y value is fixed. and then x/z vaule varies.
        # H is z and W is x
        h,w = self.map.shape
        for hp in range(4*h):
            for wp in range(4*w):
                if hp%2 != wp%2:
                    color = 'black'
                else:
                    color = 'white'
                # self.GenerateSingleBlock(self.tile_size*(wp-1.5), -self.height, self.tile_size*(hp-1.5), self.tile_size, color, 'tile')
                # print('gg')
                # self.DrawSingleComp(wp,self.height,hp)
    def GenerateTiles(self):
        h,w = self.map.shape

        for hp in range(4*h):
            if hp%2 == 1:
                color = 'black'
            else:
                color = 'white'

            print('gg')
        for wp in range(4*w):
            if wp%2 == 1:
                color = 'black'
            else:
                color = 'white'
            print(color)
        pass
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
        for i, coord in enumerate(self.wall_list):
            x = coord[0]
            z = coord[1]
            l = len(self.color_list)
            color = self.color_list[i%l]
            # self.GenerateSingleBlock(x*4*self.tile_size, self.tile_size*1.2, z*4*self.tile_size, 4*self.tile_size, color, 'block')
            self.GenerateSingleBlock(x*4*self.tile_size, 2*self.tile_size-self.height, z*4*self.tile_size, 4*self.tile_size, color, 'block')
            # print('hhhh')
    def DrawSingleComp(self, x=0,y=-0.155,z=0, size_x=0.1, size_z = 0.1,color='bb'):
        glBegin(GL_QUADS)
        if color == 'white':
            glColor3f(0.75, 0.75, 0.75)
        elif color == 'black':
            glColor3f(0.12,0.12,0.12)
        else:
            glColor3f(0.65,0.47,0.98)
        # glTexCoord2d(0.0, 0.0)
        glVertex3f(-size_x+x,y,size_z+z)
        # glTexCoord2d(1.0, 0.0)
        glVertex3f(size_x+x,y,size_z+z)
        # glTexCoord2d(1.0, 1.0)
        glVertex3f(size_x+x,y,-size_z+z)
        # glTexCoord2d(0.0, 1.0)
        glVertex3f(-size_x+x,y,-size_z+z)
        glEnd()
    def DrawFloor(self):
        H = self.map.shape[0]
        W = self.map.shape[1]
        centercoord_z = 2*(H-1)*self.tile_size
        centercoord_x = 2*(W-1)*self.tile_size
        self.DrawSingleComp(centercoord_x, -self.height, centercoord_z, size_x=2*W*self.tile_size, size_z = 2*H*self.tile_size, color='white')
        # self.DrawSingleComp(0,-self.height+0.001,centercoord_z,size_x = 0.001,size_z=centercoord_z*2, color='black')
        for wp in range(4*(W)+1):
            self.DrawSingleComp((wp-2)*self.tile_size,-self.height+0.001,centercoord_z,size_x = 0.00375,size_z=2*H*self.tile_size, color='black')
        for hp in range(4*(H)+1):
            self.DrawSingleComp(centercoord_x,-self.height+0.0011,(hp-2)*self.tile_size,size_x = 2*W*self.tile_size,size_z=0.00375, color='black')
            pass

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
        self.camz = self.h/900/np.tan((np.pi/180)*fov/2)
        self.nearz = self.camz * 0.98 # self.camz - 7/8
        self.farz = self.camz * 4.6

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
        glFrustum(-self.w/1600/10,self.w/1600/10,-self.h/900/8,self.h/900/8, self.nearz, self.farz)

        glMatrixMode(GL_MODELVIEW)
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()
        gluLookAt(0,0.2,self.camz, 0,0,0, 0,1,0)
        glMultMatrixf((self.trans_mat).T)
        # glutSolidTeapot(0.125)

        # Wall Generation test
        self.GenerateWalls()
        # Floor Generation
        self.DrawFloor()

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
            temp_trans[2,3] = -0.75
            degree = 0
            pass
        elif pos == 1:
            temp_trans[0,3] = -0.75
            degree = 90
            pass
        elif pos == 2:
            temp_trans[2,3] = 0.75
            degree = 180
            pass
        elif pos==3:
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
    print(TestMaze.shape)
    Generator = GraphicsGenerator(np.zeros((51,51)))
    Generator.Update()