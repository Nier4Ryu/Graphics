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

        self.fallen = 0
        self.falling = False
        self.BEV_size = np.eye(4)

        self.TrapOpen = False

        self.initial_angle = angle

        self.move_speed = 0.05
        self.degree_speed = 5
        self.is_BEV = False
        self.w = 1600
        self.h = 900
        # print(self.initial_angle)
        self.reset_pos()
        self.save_degree = angle
        self.save_pos = np.copy(self.trans_mat)
        self.SPObj_coord = None
        # print(self.initial_angle)
        # print("outside",self.rotation_angle)

        self.win = False

        self.color_list = ['red','orange','yellow','green','blue','indigo','violet']

        self.init_time = time.time()
        

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
                self.GenerateSingleObject(x*4*self.tile_size, self.height, z*4*self.tile_size, 4*self.tile_size, color, 'block')
                # self.GenerateSingleObject((x*4-2)*self.tile_size, 2*self.tile_size-self.height, (z*4-2)*self.tile_size, 4*self.tile_size, 'black', 'column')
                # self.GenerateSingleObject((x*4+2)*self.tile_size, 2*self.tile_size-self.height, (z*4-2)*self.tile_size, 4*self.tile_size, 'black', 'column')
                # self.GenerateSingleObject((x*4-2)*self.tile_size, 2*self.tile_size-self.height, (z*4+2)*self.tile_size, 4*self.tile_size, 'black', 'column')
                # self.GenerateSingleObject((x*4+2)*self.tile_size, 2*self.tile_size-self.height, (z*4+2)*self.tile_size, 4*self.tile_size, 'black', 'column')
    def GenerateExitPortal(self):
        exit_x = self.maze.exitPoint[1]
        exit_z = self.maze.exitPoint[0]

        self.GenerateSingleObject(exit_x*4*self.tile_size, self.tile_size-self.height, exit_z*4*self.tile_size, self.tile_size*0.75, color = 'sky', mode='sphere')
    
    def GenerateSPObject(self):
        if self.SPObj_coord != None:
            self.GenerateSingleObject(self.SPObj_coord[0]-2*self.tile_size, -self.height, self.SPObj_coord[1]-2*self.tile_size, 0.5*self.tile_size, color = 'sky', mode='cone')


    def DrawSingleComp(self, x=0.0,y=-0.155,z=0.0, size_x=0.1, size_z = 0.1,color='bb', mode='square'):
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
        if mode == 'square':
            glBegin(GL_QUADS)
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
    
    def DrawSingleTrap(self, x,z):
        self.DrawSingleComp(x,-self.height+0.0015, z, self.tile_size*0.5, self.tile_size*0.5, 'black', mode='square')

    def GenerateSingleObject(self, x,y,z, size=0.25, color='black', mode='block'):
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
        elif color == 'sky':
            glColor3f(0.56,0.75,0.85)
        else:
            glColor3f(0.99,0.99,0.99)

        if mode=='block':
            glMultMatrixf(trans_mat.T)
            glutSolidCube(size)
            glColor3f(0.12,0.12,0.12)
            glLineWidth(70)
            glutWireCube(size)
            glMultMatrixf(trans_mat_i.T)
        elif mode=='column':
            sc_mat = np.eye(4)
            sc_mat[1,1]=100
            glMultMatrixf(trans_mat.T)
            glMultMatrixf(sc_mat.T)
            glutSolidCube(size/100)
            sc_mat[1,1]=1/sc_mat[1,1]
            glMultMatrixf(sc_mat.T)
            glMultMatrixf(trans_mat_i.T)
        elif mode == 'sphere':
            glMultMatrixf(trans_mat.T)
            glutWireSphere(size, 20, 20)
            # glColor3f(0.99,0.99,0.99)
            glMultMatrixf(trans_mat_i.T)
        elif mode == 'cone':
            # temp_rot_mat = self.rotation(90, False)
            rot_mat = np.eye(4)
            rot_mat[1:3,1:3] = self.rotation(90, False)[0:2,0:2]
            rot_mat_i = np.eye(4)
            rot_mat_i[1:3,1:3] = self.rotation(-90, False)[0:2,0:2]
            glMultMatrixf(trans_mat.T)
            glMultMatrixf(rot_mat)
            glutWireCone(size, 2*size, 10, 10)
            glMultMatrixf(rot_mat_i)
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
        if self.TrapOpen == True:
            for t in self.maze.traps:
                self.DrawSingleTrap(t)

    def GenerateSavepoint(self):
        pass

    def GenerateCompass(self):
        """
        Generate a Compass Object that points towards the exit point
        1) A Wire Shpere That in capsulates the needle
        2) A needle rotating with in the capsule
        """
        degree = self.characterController.AngleToExit(self.rotation_angle)
        print("degree is ", np.degrees(degree))
        
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        scaleMat = np.eye(4)
        scaleMat[0,0] = 0.2
        scaleMat[1,1] = 0.2
        
        rotationMat = np.eye(4)
        rotationMat[0,0] = np.cos(degree)
        rotationMat[0,1] = np.sin(-degree)
        rotationMat[1,0] = np.sin(degree)
        rotationMat[1,1] = np.cos(degree)

        transMat = np.eye(4)
        transMat[0,3] = -0.8
        transMat[1,3] = -0.8

        glMultMatrixf(transMat.T)
        glMultMatrixf(scaleMat.T)
        glMultMatrixf(rotationMat)

        depth = -1

        glBegin(GL_TRIANGLES)
        glColor3f(1, 0.0, 0.0)
        glVertex3f(0, 0.35, depth)
        glVertex3f(-0.15, 0, depth)
        glVertex3f(0.15, 0, depth)

        glColor3f(0, 0, 1)
        glVertex3f(0, -0.35, depth)
        glVertex3f(-0.15, 0, depth)
        glVertex3f(0.15, 0, depth)
        glEnd()
        
        glBegin(GL_TRIANGLE_FAN)
        glColor3f(1, 1, 1)
        glVertex3f(0, 0.36, depth)
        glVertex3f(0.18, 0.312, depth)
        glVertex3f(0.312, 0.18, depth)

        glVertex3f(0.36, 0, depth)
        glVertex3f(0.312, -0.18, depth)
        glVertex3f(0.18, -0.312, depth)

        glVertex3f(0, -0.36, depth)
        glVertex3f(-0.18, -0.312, depth)
        glVertex3f(-0.312, -0.18, depth)

        glVertex3f(-0.36, 0, depth)
        glVertex3f(-0.312, 0.18, depth)
        glVertex3f(-0.18, 0.312, depth)
        glEnd()

        # Restor Mat Info
        glPopMatrix()

        glMatrixMode(GL_PROJECTION)
        glPopMatrix()

        glMatrixMode(GL_MODELVIEW)
        
        # glClear(GL_COLOR_BUFFER_BIT)



    def GenerateClock(self):
        pass

    def GenerateNotice(self):
        """
        Notify the player of the current state with a box
        ex)if red -> You are trying to walk through the walls -> not allowed
        """
        pass

    def GenerateText(self, text, position=(0,0), scale=1, color=(0,0,1,0)):
        """
        generate a given text on the position for the given time
        """

        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        glLineWidth(1)
        
        transMat = np.eye(4)
        transMat[0,3] = -0.95
        transMat[1,3] = -0.85
        scaleMat = np.eye(4)
        scaleMat[0,0] = 0.01 * scale
        scaleMat[1,1] = 0.016 * scale
        degree = np.radians(90)
        rotationMat = np.eye(4)
        rotationMat[0,0] = np.cos(degree)
        rotationMat[0,1] = np.sin(-degree)
        rotationMat[1,0] = np.sin(degree)
        rotationMat[1,1] = np.cos(degree)
        glMultMatrixf(transMat.T)
        glMultMatrixf(scaleMat.T)
        glMultMatrixf(rotationMat)        

        delta_x = position[0]
        delta_y = position[1]
        delta_y_scale = scaleMat[1,1] * 350
        glBegin(GL_LINES)
        glColor4f(color[0], color[1], color[2], color[3])
        len_text = len(text)
        for i in range(len_text):            
            char = text[i]

            if char == "a" or char == "A":
                lines = [
                    ((0,2),(6,0)),
                    ((0,2),(6,4)),
                    ((3,1),(3,3))
                ]
            elif char == "b" or char == "B":
                lines = [
                ]
            elif char == "c" or char == "C":
                lines = [
                    ((1,4),(0,3)),
                    ((0,3),(0,1)),
                    ((0,1),(1,0)),
                    ((1,0),(5,0)),
                    ((5,0),(6,1)),
                    ((6,1),(6,3)),
                    ((6,3),(5,4))
                ]
            elif char == "d" or char == "D":
                lines = [
                ]
            elif char == "e" or char == "E":
                lines = [
                    ((0,0),(0,4)),
                    ((3,0),(3,4)),
                    ((6,0),(6,4)),
                    ((0,0),(6,0)),
                ]
            elif char == "f" or char == "F":
                lines = [
                    ((0,0),(0,4)),
                    ((3,0),(3,4)),
                    ((0,0),(6,0)),
                ]
            elif char == "g" or char == "G":
                lines = [
                ]
            elif char == "h" or char == "H":
                lines = [
                    ((0,0),(6,0)),
                    ((0,4),(6,4)),
                    ((3,0),(3,4)),
                ]
            elif char == "i" or char == "I":
                lines = [
                    ((0,0),(0,4)),
                    ((6,0),(6,4)),
                    ((0,2),(6,2)),
                ]
            elif char == "j" or char == "J":
                lines = [
                ]
            elif char == "k" or char == "K":
                lines = [
                    ((0,0),(6,0)),
                    ((3,0),(6,0)),
                    ((3,0),(6,4)),
                ]
            elif char == "l" or char == "L":
                lines = [
                    ((0,0),(6,0)),
                    ((6,0),(6,4)),
                ]
            elif char == "m" or char == "M":
                lines = [
                    ((0,0),(6,0)),
                    ((0,0),(6,2)),
                    ((6,2),(0,4)),
                    ((0,4),(6,4)),
                ]
            elif char == "n" or char == "N":
                lines = [
                    ((0,0),(6,0)),
                    ((0,0),(6,4)),
                    ((6,4),(0,4)),
                ]
            elif char == "o" or char == "O":
                lines = [
                    ((0,1),(0,3)),
                    ((0,1),(1,0)),
                    ((0,3),(1,4)),
                    ((1,0),(5,0)),
                    ((1,4),(5,4)),
                    ((5,0),(6,1)),
                    ((5,4),(6,3)),
                    ((6,1),(6,3)),
                ]
            elif char == "p" or char == "P":
                lines = [
                    ((0,0),(6,0)),
                    ((0,0),(0,3)),
                    ((0,3),(1,4)),
                    ((1,4),(2,4)),
                    ((2,4),(3,3)),
                    ((3,3),(3,0)),
                ]
            elif char == "q" or char == "Q":
                lines = [
                    ((0,1),(0,3)),
                    ((0,1),(1,0)),
                    ((0,3),(1,4)),
                    ((1,0),(5,0)),
                    ((1,4),(5,4)),
                    ((5,0),(6,1)),
                    ((5,4),(6,3)),
                    ((6,1),(6,3)),
                    ((3,3),(6,4)),
                ]
            elif char == "r" or char == "R":
                lines = [
                    ((0,0),(6,0)),
                    ((0,0),(0,3)),
                    ((0,3),(1,4)),
                    ((1,4),(2,4)),
                    ((2,4),(3,3)),
                    ((3,3),(3,0)),
                    ((3,3),(6,4)),
                ]
            elif char == "s" or char == "S":
                lines = [
                    ((0,1),(0,3)),
                    ((0,1),(1,0)),
                    ((0,3),(1,4)),
                    ((1,0),(5,4)),
                    ((5,0),(6,1)),
                    ((5,4),(6,3)),
                    ((6,1),(6,3)),
                ]
            elif char == "t" or char == "T":
                lines = [
                    ((0,0),(0,4)),
                    ((0,2),(6,2)),
                ]
            elif char == "u" or char == "U":
                lines = [
                    ((0,0),(5,0)),
                    ((0,4),(5,4)),
                    ((5,0),(6,1)),
                    ((6,1),(6,3)),
                    ((5,4),(6,3)),
                ]
            elif char == "v" or char == "V":
                lines = [
                    ((0,0),(6,2)),
                    ((6,2),(0,4)),
                ]
            elif char == "w" or char == "W":
                lines = [
                    ((0,0),(6,1)),
                    ((6,1),(3,2)),
                    ((3,2),(6,3)),
                    ((6,3),(0,4)),
                ]
            elif char == "x" or char == "X":
                lines = [
                    ((0,0),(6,4)),
                    ((0,4),(6,0)),
                ]
            elif char == "y" or char == "Y":
                lines = [
                    ((0,0),(3,2)),
                    ((3,2),(0,4)),
                    ((3,2),(6,2)),
                ]
            elif char == "z" or char == "Z":
                lines = [
                    ((0,0),(0,4)),
                    ((0,4),(6,0)),
                    ((6,0),(6,4)),
                ]
            else:
                lines = [

                ]        
            self.GenerateLines(lines, delta_x = delta_x, delta_y = delta_y)
            delta_y += delta_y_scale
        
        glEnd()

        # Restore Original Values
        glPopMatrix()
        glLoadIdentity()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)

    def GenerateLines(self, lines, delta_x = 0, delta_y=0):
        """
        Draw the lines based on the given points
        """
        depth = -1    
        for line in lines:
            start_point = line[0]
            end_point = line[1]
            glVertex3f(start_point[0]+delta_x,start_point[1]+delta_y,depth)
            glVertex3f(end_point[0]+delta_x,end_point[1]+delta_y,depth)

    def GenerateCurve(self):
        pass

    def CreateSavePoint(self):
        self.save_pos = np.copy(self.trans_mat)  
        self.save_degree = self.rotation_angle
        self.characterController.CreateSavePoint()
        self.SPObj_coord = self.characterController.pos[0,3], self.characterController.pos[2,3]
    
    def LoadSavePoint(self):
        self.trans_mat = np.copy(self.save_pos)
        self.rotation_angle = self.save_degree
        self.characterController.LoadSavePoint()
    
    def GeneratePoint(self, object_type):
        if object_type == "EXIT_POINT":
            # self.maze.Push
            pass

    def DisplayWasted(self):
        # This part displays wasted scene when the player is caught by a trap.
        # Implement alpha blending.
        # or falling
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
                glOrtho(-self.w/1600,self.w/1600,-self.h/1600,self.h/1600, self.nearz, self.farz)
                glMatrixMode(GL_MODELVIEW)
                glClear(GL_COLOR_BUFFER_BIT)
                glLoadIdentity()

                cam_up_mat = self.rotation(self.rotation_angle, False)@np.array([[0,1,0,0]]).T
                # print(cam_up_mat[0,0], cam_up_mat[2,0])
                gluLookAt(0,4,0, 0,0,0, cam_up_mat[0,0],0,cam_up_mat[1,0])
                # required feature: add pointing shape on the bev character
            else:
                self.perspective(60)
                glFrustum(-self.w/1600/10,self.w/1600/10,-self.h/900/8,self.h/900/8, self.nearz, self.farz)

                glMatrixMode(GL_MODELVIEW)
                glClear(GL_COLOR_BUFFER_BIT)
                glLoadIdentity()
                gluLookAt(0,0.2-self.fallen,self.camz, 0,-self.fallen,0, 0,1,0)
            
            glMultMatrixf((self.trans_mat).T)

            # Wall Generation test
            self.GenerateWalls()
            # Floor Generation
            self.DrawFloor()

            self.GenerateMarks()
            self.GenerateExitPortal()
            self.GenerateSPObject()

            if self.TrapOpen == True:
                self.DrawSingleTrap(1,1)
            glLoadIdentity()

            self.draw_all_axis()
            if self.is_BEV == True:
                self.DrawCharacter()
            self.GenerateCompass()
        else:
            self.DisplayWin()

        self.GenerateText("You Exited The maze P R!")

        glutSwapBuffers()

    def DisplayWin(self):
        self.GenerateText("You Exited The maze!")

    def reshape(self, w, h):
        # implement here
        print(f"window size: {w} x {h}")
        self.center_x = int(w/2)
        self.center_y = int(h/2)
        self.w = w
        self.h = h
        glViewport(0,0,self.w, self.h)
        glutPostRedisplay()

    def TimeFunc(self, input_var):
        # **!!Falling part!!**
        if self.falling == True:
            # print(time.time_ns())
            self.fallen = self.fallen+0.02
            self.BEV_size[0:3] = self.BEV_size[0:3] * 0.95
            # print(self.fallen)
        if self.fallen > 0.85:
            self.falling = False
            self.fallen = 0.0
            self.BEV_size = np.eye(4)
            self.LoadSavePoint()
            # self.reset_pos()
            # And then somewhat life lose activation on the character

        # **!!Trap Control Part!!**
        if math.ceil(time.time()- self.init_time)%3 == 0:
            self.TrapOpen = False
        else:
            self.TrapOpen = True
        # print(self.TrapOpen)

        glutTimerFunc(16, self.TimeFunc, 16)

        glutPostRedisplay()
        
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

        if key == b'f' or key == b'F':
            self.falling = not self.falling

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

        else:
            temp_rot = np.eye(4)
            temp_rot = np.eye(4)
            rad = degree * np.pi / 180
            temp_rot[0,0] = np.cos(rad)
            temp_rot[0,1] = -np.sin(rad)
            temp_rot[1,0] = np.sin(rad)
            temp_rot[1,1] = np.cos(rad)

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

    def DrawCharacter(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-self.w/800,self.w/800,-self.h/800,self.h/800, -6, 3)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        rot_mat = self.rotation((self.rotation_angle-180), False)

        glMultMatrixf(rot_mat.T)
        glMultMatrixf(self.BEV_size)
        glBegin(GL_TRIANGLES)
        glColor3f(0.95, 0.0, 0.0)
        glVertex2f(0, 0.23)
        glColor3f(0.85, 0.85, 0.1)
        glVertex2f(-0.15, -0.15)
        glVertex2f(0.15, -0.15)
        glEnd()
        glLoadIdentity()

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
        # rotAngle = np.degrees(self.characterController.AngleToExit(self.rotation_angle))
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
        glutTimerFunc(16, self.TimeFunc, 16)
        self.light()

        glutMainLoop()
    
if __name__ == "__main__":
    TestMaze = np.array([[2,0,0,0,0],[1,1,1,1,0],[0,1,0,1,1],[0,0,0,1,3]])
    print(TestMaze)
    print(TestMaze.shape)
    Generator = GraphicsGenerator(np.zeros((51,51)))
    Generator.Update()