# This is the graphics Generator that generates the graphics based on the info
from CharacterController import *

from tkinter import Y
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
import time

class GraphicsGenerator:
    def __init__(self, maze, angle):
        self.maze = maze
        self.map = maze.pathMap
        self.wall_list = maze.walls
        self.tile_size = 0.25
        self.characterController = CharacterController(self.maze, self.tile_size)
        self.height = 0.2

        self.initial_angle = angle
        # self.rotation_angle = 180

        self.move_speed = 0.05
        self.degree_speed = 5
        self.is_BEV = False
        self.w = 1600
        self.h = 900
        print(self.initial_angle)
        self.reset_pos()
        print(self.initial_angle)
        print("outside",self.rotation_angle)

        self.win = False

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
    
    def GenerateWalls(self):
        for i, dist in enumerate(self.wall_list):
            for coord in dist:
                x = coord[1]
                z = coord[0]
                l = len(self.color_list)
                color = self.color_list[i%l]
                self.GenerateSingleBlock(x*4*self.tile_size, 2*self.tile_size-self.height, z*4*self.tile_size, 4*self.tile_size, color, 'block')
                self.GenerateSingleBlock((x*4-2)*self.tile_size, 2*self.tile_size-self.height, (z*4-2)*self.tile_size, 4*self.tile_size, 'black', 'column')
                self.GenerateSingleBlock((x*4+2)*self.tile_size, 2*self.tile_size-self.height, (z*4-2)*self.tile_size, 4*self.tile_size, 'black', 'column')
                self.GenerateSingleBlock((x*4-2)*self.tile_size, 2*self.tile_size-self.height, (z*4+2)*self.tile_size, 4*self.tile_size, 'black', 'column')
                self.GenerateSingleBlock((x*4+2)*self.tile_size, 2*self.tile_size-self.height, (z*4+2)*self.tile_size, 4*self.tile_size, 'black', 'column')

    def DrawSingleComp(self, x=0.0,y=-0.155,z=0.0, size_x=0.1, size_z = 0.1,color='bb'):
        glBegin(GL_QUADS)
        if color == 'white':
            glColor3f(0.75, 0.75, 0.75)
        elif color == 'black':
            glColor3f(0.12,0.12,0.12)
        elif color == 'red':
            glColor3f(0.95,0.1,0.1)
        elif color == 'green':
            glColor3f(0.1,0.95,0.1)
        elif color == 'blue':
            glColor3f(0.1,0.1,0.95)
        else:
            glColor3f(0.65,0.47,0.98)
        glVertex3f(-size_x+x,y,size_z+z)
        glVertex3f(size_x+x,y,size_z+z)
        glVertex3f(size_x+x,y,-size_z+z)
        glVertex3f(-size_x+x,y,-size_z+z)
        glEnd()
    def DrawFloor(self):
        H = self.map.shape[0]
        W = self.map.shape[1]
        centercoord_z = 2*(H-1)*self.tile_size
        centercoord_x = 2*(W-1)*self.tile_size
        self.DrawSingleComp(centercoord_x, -self.height, centercoord_z, size_x=2*W*self.tile_size, size_z = 2*H*self.tile_size, color='white')
        for wp in range(4*(W)+1):
            self.DrawSingleComp((wp-2)*self.tile_size,-self.height+0.001,centercoord_z,size_x = 0.00375,size_z=2*H*self.tile_size, color='black')
        for hp in range(4*(H)+1):
            self.DrawSingleComp(centercoord_x,-self.height+0.0011,(hp-2)*self.tile_size,size_x = 2*W*self.tile_size,size_z=0.00375, color='black')

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
            glColor3f(0.56,0.56,0.56)
        else:
            glColor3f(0.99,0.99,0.99)

        if mode=='column':
            sc_mat = np.eye(4)
            sc_mat[1,1]=100
            glMultMatrixf(trans_mat.T)
            glMultMatrixf(sc_mat.T)
            glutSolidCube(size/100)
            sc_mat[1,1]=1/sc_mat[1,1]
            glMultMatrixf(sc_mat.T)
            glMultMatrixf(trans_mat_i.T)
        elif mode=='block':
            glMultMatrixf(trans_mat.T)
            glutSolidCube(size)
            glColor3f(0.99,0.99,0.99)
            glutWireCube(size)
            glMultMatrixf(trans_mat_i.T)
        
        glColor3f(1.0,1.0,1.0)

    def GenerateMarks(self):
        for m in self.maze.marks:
            x = m[1] - 2*self.tile_size
            z = m[0] - 2*self.tile_size
            mark_type = m[2]
            if mark_type == 'A':
                color = 'red'
            if mark_type == 'B':
                color = 'green'
            if mark_type == 'C':
                color = 'blue'
            self.DrawSingleComp(x, -self.height+0.0012, z, self.tile_size*0.5, self.tile_size*0.5,color=color)    

    def GenerateTraps(self):
        pass

    def GenerateSavepoint(self):
        pass

    def GenerateCompass(self):
        """
        Generate a Compass Object that points towards the exit point
        1) A Wire Shpere That in capsulates the needle
        2) A needle rotating with in the capsule
        """
        rotAngle = np.degrees(self.characterController.AngleToExit(self.rotation_angle))
        print("rotAngle is ", rotAngle)
        
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        glutWireSphere(0.01, 50, 50)

        glColor4f(0, 0, 1, 0)
        # Draw the lines
        glBegin(GL_LINES)
        # Reference Line
        glColor4f(1, 0, 0, 0)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(0.0, 0.0, 0.1)
        glEnd()

        # Rot about y axis
        rotMat = np.eye(4)
        rotMat[0,0] = np.cos(np.radians(rotAngle))
        rotMat[0,2] = -np.sin(np.radians(rotAngle))
        rotMat[2,0] = np.sin(np.radians(rotAngle))
        rotMat[2,2] = np.cos(np.radians(rotAngle))
        glMultMatrixd(rotMat)
        # Rot about x axis to give some 3d like image
        rotAngle = -30
        rotMat = np.eye(4)
        rotMat[1,1] = np.cos(np.radians(rotAngle))
        rotMat[1,2] = -np.sin(np.radians(rotAngle))
        rotMat[2,1] = np.sin(np.radians(rotAngle))
        rotMat[2,2] = np.cos(np.radians(rotAngle))
        glMultMatrixd(rotMat)
        
        glBegin(GL_LINES)
        # Z Line
        glColor4f(0, 0, 1, 0)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(0.0, 0.0, 0.1)
        glEnd()

    def GenerateClock(self):
        pass

    def GenerateNotice(self):
        """
        Notify the player of the current state with a box
        ex)if red -> You are trying to walk through the walls -> not allowed
        """
        pass

    def CreateSavePoint(self):
        self.save_pos = np.copy(self.trans_mat)        
        self.characterController.CreateSavePoint()

        # Object
    
    def LoadSavePoint(self):
        self.trans_mat = np.copy(self.save_pos)
        self.characterController.LoadSavePoint()
    
    def GeneratePoint(self, object_type):
        if object_type == "EXIT_POINT":
            # self.maze.Push
            pass

    def DisplayWasted(self):
        # This part displays wasted scene when the player is caught by a trap.
        # Implement alpha blending.
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
        if self.win == False:
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            if self.is_BEV == True:
                self.camz = 1
                self.nearz = -1
                self.farz = 6.0
                glOrtho(-self.w/800,self.w/800,-self.h/800,self.h/800, self.nearz, self.farz)
                glMatrixMode(GL_MODELVIEW)
                glClear(GL_COLOR_BUFFER_BIT)
                glLoadIdentity()
                cam_up_mat = self.rotation(self.rotation_angle, False)@np.array([[0,0,1,0]]).T
                print(cam_up_mat[0,0], cam_up_mat[2,0])
                gluLookAt(0,4,0, 0,0,0, cam_up_mat[0,0],0,cam_up_mat[2,0])
                # required feature: add pointing shape on the bev character
            else:
                self.perspective(60)
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

            self.GenerateMarks()
            # self.GenerateSingleBlock(0.1,0.1,0.1,0.25,'black', 'column')

            glLoadIdentity()

            self.draw_all_axis()
            # self.GenerateCompass()
            if self.is_BEV == True:
                glColor3f(0.860,0.0625,0.0625)
                glutSolidTeapot(0.2)
        else:
            self.DisplayWin()
        glutSwapBuffers()
    def DisplayWin(self):
        pass
    def reshape(self, w, h):
        # implement here
        print(f"window size: {w} x {h}")
        self.center_x = int(w/2)
        self.center_y = int(h/2)
        self.w = w
        self.h = h
        glViewport(0,0,self.w, self.h)
        glutPostRedisplay()

    def moving(self, input_var):
        print(time.time_ns())
        glutTimerFunc(16, self.moving, 16)
        
    def Translation(self,x,z):
        """
        First Check that the position to move is not with in the wall
        """
        rotation = np.eye(4)
        print(self.rotation_angle)
        rotation[0,0] = np.cos(np.radians(-(self.rotation_angle-180)))
        rotation[0,2] = -np.sin(np.radians(-(self.rotation_angle-180)))
        rotation[2,0] = np.sin(np.radians(-(self.rotation_angle-180)))
        rotation[2,2] = np.cos(np.radians(-(self.rotation_angle-180)))
        direction = np.array([x,0,z,1])
        if self.characterController.Translation(rotation, direction):
            self.trans_mat[0,3] = self.trans_mat[0,3] + x
            self.trans_mat[2,3] = self.trans_mat[2,3] + z
        if self.characterController.WinCheck():
            self.reset_pos()
            self.win = True

    def keyboard(self, key, x, y):
        x=0
        z=0
        if key == b'w' or key == b'W':
            x = 0
            z = self.move_speed
        if key == b's' or key == b'S':
            x = 0
            z = -self.move_speed
        if key == b'a' or key == b'A':
            x = self.move_speed
            z = 0
        if key == b'd' or key == b'D':
            x = -self.move_speed
            z = 0
        
        self.Translation(x,z)
        
        if key == b'p' or key == b'P':
            self.reset_pos()

        if key == b'l' or key == b'L':
            self.LoadSavePoint()
        if key == b'c' or key == b'C':
            self.CreateSavePoint()

        if key == b'm' or key == b'M':
            self.maze.PushMarks(self.characterController.pos,'A')
            
        if key == b'b' or key == b'B':
            self.is_BEV = not self.is_BEV

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
    
    def rotation(self, degree = 10, ch_global=True):
        if ch_global == True:
            self.rotation_angle += degree
    
        temp_rot = np.eye(4)
        rad = degree * np.pi / 180
        temp_rot[0,0] = np.cos(rad)
        temp_rot[0,2] = -np.sin(rad)
        temp_rot[2,0] = np.sin(rad)
        temp_rot[2,2] = np.cos(rad)
        return temp_rot

    def reset_pos(self):
        # This function might be transferred to savepoint load function.
        # pos is the wall side where the character will be placed.
        temp_trans = np.eye(4)
        degree = self.initial_angle
        print(self.initial_angle)
        self.rotation_angle = 0
        self.characterController.Reset()
        
        self.trans_mat = self.rotation(degree)@temp_trans

        self.save_pos = np.copy(self.trans_mat)
                
    def setcoord(self, x,y,z):
        arr = np.eye(4)
        arr[0,3] = x
        arr[1,3] = y
        arr[2,3] = z
        return arr
    def scale_cuboid(self, index=0):
        x = np.eye(4)
        x[index, index] = 20
        return x

    def draw_axis(self, index=0):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-self.w/800,self.w/800,-self.h/800,self.h/800, -6, 3)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        axis_move = [0,0,0]
        axis_move[index] = 0.1
        rot_mat = np.eye(4)
        rot_mat[0:3,0:3] = self.trans_mat[0:3,0:3].T

        glMultMatrixf((self.setcoord(-0.8*self.w/800,-0.8*self.h/800,5)@rot_mat@self.setcoord(axis_move[0],axis_move[1],axis_move[2])@self.scale_cuboid(index)).T)
        glutSolidCube(0.01)
        glLoadIdentity()
    def draw_all_axis(self):
        rotAngle = np.degrees(self.characterController.AngleToExit(self.rotation_angle))
        glColor3f(1.0,0.0,0.0)
        self.draw_axis(0)
        glColor3f(0.0,1.0,0.0)
        self.draw_axis(1)
        glColor3f(0.0,0.0,1.0)
        self.draw_axis(2)
        glColor3f(1,1,1)

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
        glutTimerFunc(16, self.moving, 16)
        self.light()

        glutMainLoop()
    
if __name__ == "__main__":
    TestMaze = np.array([[2,0,0,0,0],[1,1,1,1,0],[0,1,0,1,1],[0,0,0,1,3]])
    print(TestMaze)
    print(TestMaze.shape)
    Generator = GraphicsGenerator(np.zeros((51,51)))
    Generator.Update()