import objectClass
import levelClass
from math import *
from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *
import sys, os, traceback
screen_size = [800,600]
def displayInit():
    pygame.display.init()
    #pygame.font.init()
    
    #screen_size = [1280,680]
    multisample = 0
    icon = pygame.Surface((1,1)); icon.set_alpha(0); pygame.display.set_icon(icon)
    if multisample:
        pygame.display.gl_set_attribute(GL_MULTISAMPLEBUFFERS,1)
        pygame.display.gl_set_attribute(GL_MULTISAMPLESAMPLES,multisample)
    pygame.display.set_mode(screen_size,OPENGL|DOUBLEBUF)
    fpsClock = pygame.time.Clock()
    glHint(GL_PERSPECTIVE_CORRECTION_HINT,GL_NICEST)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()


def GravInit(data):
    data.levels=[]
    data.allOrbs = []
    data.been = [(0,0)]
    data.rainbow = [(1,1,0),(1,.49,0),(1,0,0),(.58,0,.82),(.58,0,.82),(.29,0,.86),(0,0,1),(0,1,0)]
    data.rainbow2 = [(.8,.8,0),(.8,.4,0),(.8,0,0),(.45,0,.72),(.48,0,.72),(.2,0,.76),(0,0,.8),(0,.8,0)]
    data.pause = False
    data.rows = 30
    data.cols = 30
    data.masses = []
    createGrid(data)
    data.edgex,data.edgey = createLines(data)
    data.currentZ = 0
    data.me = objectClass.Object('me',.5,data.rows/4,data.cols/2,.5)
    #data.me.yVelocity = 0
    data.lineBall = objectClass.Object('line',.5,data.me.x - 20 , 50, 20)
    data.direction = 1
    data.camera_center = [data.me.x,data.me.y,data.me.z]
    data.cameraAngle = 0 
    data.vertCamAngle = 0     
    data.camera_radius = 5
    data.cameraPos = [data.camera_center[0]+data.camera_radius*cos(data.cameraAngle), 
    data.camera_center[1]+ data.camera_radius * sin(data.cameraAngle), data.camera_center[2]]
    data.moveMass=None
    data.stars = []
    data.mode = 1
    #data.starDirs = [(-1,1),(-1,-1),(1,-1),(1,1)]
    data.cameramode = 'first'
    data.cameraradius2 = 40
    data.jumpHeight = 0
    data.jumpTime = None
    data.jumpBool = False
    data.depth = 0
    data.currentLevel = levelClass.Level(0,data)
    data.points = 0
    data.dead = False

#only on init
def createGrid(data):
    data.points = [[0 for i in range(data.rows)] for j in range(data.rows)]
    #i = 0
    for row in range(len(data.points)):
      for col in range(len(data.points[0])):
        #i+=1
        x = row
        y = col
        data.points[row][col] = (x,y,0)
#only on init
def createLines(data):
    data.edgex = []
    data.edgey = []
    for i in range(data.rows):
        for j in range(data.cols-1):
            data.edgex.append((data.points[i][j],data.points[i][j+1]))
    for i in range(data.rows-1):
        for j in range(data.cols):
            data.edgey.append((data.points[i][j],data.points[i+1][j]))
    return data.edgex,data.edgey