from math import *
import random
import pygame
from pygame.locals import *
import mainGame2
from OpenGL.GL import *
from OpenGL.GLU import *
import levelClass
import starClass

class Object(object):
    def __init__(self,name,radius,x,y,z):
        self.taken = False
        self.yVelocity= 0
        self.name = name
        self.radius = radius
        self.x = x
        self.y = y
        self.z = z
        self.createObject()
        self.getColor()
        self.mass = random.randint(60,80)
    def getColor(self):
        if self.name == 'up':
            self.color = (0,0,1)
        elif self.name == 'down':
            self.color = (1,0,0)
        else:
            self.color = (0,1,0)
    def createObject(self):
        r,x,y,z= self.radius,self.x,self.y,self.z
        self.points = [[] for i in range(24)]
        s = 0
        increment = r/12
        for plate in range(0,12):
            radius = ((r**2)-(s**2))**.5
            for angle in range(0,360,30):
                angle = angle*pi/180
                X = x + radius*cos(angle)
                Y = y + radius*sin(angle)
                self.points[plate].append((X,Y,z+s))
                self.points[23-plate].append((X,Y,z-s))
            s+=increment
    def resetMe(self, data):
        if self.name == 'me':
            if not data.jumpBool:
                g = mainGame2.getG(self.x,self.y,data) + data.currentZ
                if data.mode == 1:
                    self.z = g + self.radius
                else: self.z = g - self.radius
            self.createObject()
            mainGame2.resetCamera(data)
        elif self.name == 'line':
            self.z = 20-data.been[-1][0]
            self.x += 1/20
            self.createObject()

    def drawObject(self,data):
        glColor3fv(self.color)
        for i in range(len(self.points)):
            plate = self.points[i]
            if self.name in ['magic','me']:
                if data.mode==1:
                    glColor3fv(data.rainbow[i//3])
                else:
                    glColor3fv(data.rainbow2[i//3])
            for i in range(len(plate)):
                point1 = plate[i-1]
                point2 = plate[i]
                glVertex3fv(point1)
                glVertex3fv(point2)
    def jump(self,data):
        bottom = mainGame2.getG(self.x,self.y,data)
        time = data.gametime - data.jumpTime
        if data.mode == 1:
            self.z = (time) - (.5*(time**2)) + self.radius
            if self.z-self.radius <= bottom and data.gametime > data.jumpTime: 
                data.jumpBool = False
                self.z = bottom + self.radius
        elif data.mode == -1:
            self.z = data.currentZ - (time) + (.5*(time**2)) - self.radius
            if self.z+self.radius >= bottom and data.gametime > data.jumpTime: 
                data.jumpBool = False
                self.z = bottom-self.radius
        data.me.resetMe(data)


    def move(self,data,keysPressed=None):
        if data.jumpBool:
            self.jump(data)
        if keysPressed == None:
            self.getYVelocity(data)
            self.yFriction()
            self.y += self.yVelocity
            self.x += 1 
            self.resetMe(data)
        elif keysPressed[K_LEFT]:
            self.yVelocity +=.1
            self.resetMe(data)
        elif keysPressed[K_RIGHT]:
            self.yVelocity -= .1
            self.resetMe(data)
    def yFriction(self):
        if self.yVelocity>0:
            self.yVelocity -= 1/30
        elif self.yVelocity<0: self.yVelocity += 1/30
    def getYVelocity(self,data):
        g1 = mainGame2.getG(self.x,self.y+.25,data)
        #g2 = mainGame2.getG(self.x,self.y,data)
        g3 = mainGame2.getG(self.x,self.y-.25,data)
        if self.y>0 and self.y<data.cols:
            if abs(g1)>abs(g3):
                self.yVelocity += -(g1-g3)/2*data.mode
            elif abs(g3)>abs(g1):
                self.yVelocity += (g3-g1)/2*data.mode
        elif self.y<=0:
            self.y=0
            self.yVelocity = -self.yVelocity
        elif self.y>=data.cols:
            self.y= data.cols
            self.yVelocity = -self.yVelocity

    def collision(self,data):
        if data.allOrbs != []:
            if data.allOrbs[0].x<self.x-(self.radius+data.allOrbs[0].radius):
                data.allOrbs.pop(0)
            nearest = data.allOrbs[0]
            #get rid of first orb
            dist = mainGame2.d(self.x,self.y,self.z,nearest.x,nearest.y,nearest.z)
            if dist<self.radius+data.allOrbs[0].radius:
                if not data.allOrbs[0].taken:  #right now cant go back to old levels
                    if data.allOrbs[0].name == 'up':
                        oldmasses = data.currentLevel.masses
                        data.currentLevel.upOrb = set()
                        data.currentLevel = data.currentLevel.parent
                        data.currentLevel.masses = oldmasses
                        data.allOrbs = []
                        data.depth -= 1
                        data.been.append((data.depth,0))
                    elif data.allOrbs[0].name == 'down':
                        oldmasses = data.currentLevel.masses
                        data.currentLevel.upOrb = set()
                        data.allOrbs[0].taken = True
                        data.allOrbs[0].color = (0,0,0)
                        data.currentLevel = levelClass.Level(data.depth+1,data,data.currentLevel)
                        data.currentLevel.masses = oldmasses
                        oldmasses = []
                        data.allOrbs = []
                        data.depth += 1
                        data.been.append((data.depth,0))
                    else:
                        data.currentLevel.magicOrb.remove(data.allOrbs[0])
                        data.allOrbs.pop(0)
                        data.points += 1
                else:
                    data.dead = True
                    
    
    